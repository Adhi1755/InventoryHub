from flask import Flask, flash, render_template, request, redirect, url_for, session, abort
from config import Config
from models import db, Product, Order, Transaction, OrderItem, Supplier, User
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import LoginManager, login_required, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import logout_user
import re

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Password validation function
    def is_password_valid(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search("[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search("[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search("[0-9]", password):
            return False, "Password must contain at least one number."
        return True, "Password is valid."

    @app.route('/register', methods=['GET', 'POST'])
    def register():     
        if request.method == 'POST':
            username = request.form.get('username') or request.form.get('fullName')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirmPassword')

            # Check if user already exists
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                if existing_user.username == username:
                    flash('Username already exists.', 'danger')
                else:
                    flash('Email already registered.', 'danger')
                return render_template('register.html')

            # Validate password
            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return render_template('register.html')
            
            is_valid, msg = is_password_valid(password)
            if not is_valid:
                flash(msg, 'danger')
                return render_template('register.html')

            # Create new user with hashed password
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully! Please login.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating your account: {str(e)}', 'danger')
                return render_template('register.html')

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        if request.method == 'POST':
            username_or_email = request.form.get('username')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

            # Try to find user by username or email
            user = User.query.filter(
                (User.username == username_or_email) | 
                (User.email == username_or_email)
            ).first()

            if user and check_password_hash(user.password, password):
                login_user(user, remember=remember)
                flash('Login successful!', 'success')
                
                # If user was trying to access a protected page before login
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username/email or password.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out successfully.', 'info')
        return redirect(url_for('login'))

    @app.route('/')
    def landing():
        return render_template('landing.html')
   
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        total_products = Product.query.filter_by(user_id=current_user.id).count()
        out_of_stock = Product.query.filter_by(user_id=current_user.id).filter(Product.quantity_in_stock == 0).count()
        total_orders = Order.query.filter_by(user_id=current_user.id).count() or 1
        total_revenue = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=current_user.id).scalar() or 0.0
        latest_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date_ordered.desc()).limit(4).all()
        overall_stock = db.session.query(func.sum(Product.quantity_in_stock)).filter_by(user_id=current_user.id).scalar() or 0
        total_capacity = 100000
        stock_percentage = (overall_stock / total_capacity) * 100 if total_capacity > 0 else 0
        stock_percentage_capped = min(stock_percentage, 100)
        orders_to_process = Order.query.filter_by(user_id=current_user.id).filter(Order.status == 'processing').count()
        ready_for_shipping = Order.query.filter_by(user_id=current_user.id).filter(Order.status == 'pending').count()
        awaiting_delivery = Order.query.filter_by(user_id=current_user.id).filter(Order.status == 'shipped').count()
        avg_order_value = total_revenue / total_orders
        today = datetime.today() 
        start_of_month = today.replace(day=1)
        last_month = (start_of_month - timedelta(days=1)).replace(day=1)
        orders_this_month = Order.query.filter(
            Order.user_id == current_user.id,
            Order.date_ordered >= start_of_month
        ).count()

        orders_last_month = Order.query.filter(
            Order.date_ordered >= last_month,
            Order.date_ordered < start_of_month
        ).count()
        if orders_last_month > 0:
            monthly_growth = ((orders_this_month - orders_last_month) / orders_last_month) * 100
        else:
            monthly_growth = 0 
        

        top_category = (
        db.session.query(
            Product.category, 
            func.sum(OrderItem.quantity).label('total_quantity')
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .filter(Product.user_id == current_user.id)  # 🔹 Filter by current user
        .group_by(Product.category)
        .order_by(func.sum(OrderItem.quantity).desc())
        .first()
        )

        top_category_name = top_category[0] if top_category else "No data"

        # --- Monthly Sales for Last 6 Months ---
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)

        # Query to aggregate monthly 'Purchase' totals for the current user
        sales = (
            db.session.query(
                func.extract('year', Transaction.transaction_date).label('year'),
                func.extract('month', Transaction.transaction_date).label('month'),
                func.sum(Transaction.amount).label('total_sales')
            )
            .filter(Transaction.transaction_type == 'Purchase')  # ✅ Match your actual type
            .filter(Transaction.amount > 0)                      # ✅ Exclude refunds and negatives
            .filter(Transaction.transaction_date >= twelve_months_ago)
            .filter(Transaction.user_id == current_user.id)      # 🔐 User-specific filter
            .group_by('year', 'month')
            .order_by('year', 'month')
            .all()
        )

        # Format for charting
        monthly_labels = [f"{int(row.month):02d}-{int(row.year)}" for row in sales]
        monthly_sales = [float(row.total_sales) for row in sales]

        
        # Stock Trend (Stock levels by category)
        stock_by_category = db.session.query(
            Product.category,
            func.sum(Product.quantity_in_stock).label('total_stock')
        ).filter(
            Product.user_id == current_user.id
        ).group_by(
            Product.category
        ).all()

        stock_labels = [row[0] for row in stock_by_category]
        stock_values = [row[1] for row in stock_by_category]

        return render_template(
            'dashboard.html', 
            total_products=total_products,
            out_of_stock=out_of_stock,
            total_orders=total_orders,
            total_revenue=total_revenue,
            overall_stock=overall_stock,
            stock_percentage=stock_percentage,
            latest_orders=latest_orders,
            orders_to_process=orders_to_process,    
            ready_for_shipping=ready_for_shipping,  
            awaiting_delivery=awaiting_delivery,
            avg_order_value=avg_order_value,
            monthly_growth=monthly_growth,
            top_category_name=top_category_name,
            monthly_labels=monthly_labels,  
            monthly_sales=monthly_sales,
            stock_labels=stock_labels,
            stock_values=stock_values,
            stock_percentage_capped=stock_percentage_capped
        )

    # Other routes remain the same...
    @app.route('/product')
    def product():
        search_query = request.args.get('search_query', '')
        category = request.args.get('category', '')

        # Filter products based on search query and category
        products_query = Product.query.filter_by(user_id=current_user.id)

        if search_query:
            products_query = products_query.filter(Product.name.contains(search_query) |
                                                Product.sku.contains(search_query) |
                                                Product.category.contains(search_query))

        if category:
            products_query = products_query.filter(Product.category == category)

        # Fetch the filtered products
        products = products_query.all()

        # Fetch distinct categories to populate the dropdown
        categories = db.session.query(Product.category).distinct().all()

        # Convert list of tuples to list of strings
        categories = [category[0] for category in categories]
        suppliers = Supplier.query.all()
        return render_template('product.html', 
                               products=products, 
                               search_query=search_query, 
                               category=category, 
                               categories=categories,
                               suppliers=suppliers)
    
    @app.route('/add_product', methods=['GET', 'POST'])
    def add_product():
        if request.method == 'POST':
        # Get form data
            name = request.form['name']
            description = request.form['description']
            quantity = request.form['quantity']
            price = request.form['price']
            supplier_id = request.form['supplier_id']
            category = request.form['category']

        # Create a new product instance
        new_product = Product(
            name=name,
            description=description,
            quantity_in_stock=quantity,
            price_per_unit=price,
            supplier_id=supplier_id,  # Link to supplier
            category=category,
            user_id=current_user.id
        )

        # Add product to the database
        db.session.add(new_product)
        db.session.commit()

        # Redirect to the products page
        return redirect(url_for('product'))

    @app.route('/edit_product/<int:product_id>', methods=['POST'])
    def edit_product(product_id):
        product = Product.query.get_or_404(product_id)
        product.name = request.form['name']
        product.description = request.form['description']
        product.quantity_in_stock = request.form['quantity']
        product.price_per_unit = request.form['price']
        product.supplier_id = request.form['supplier_id']
        product.category = request.form['category']
    
        db.session.commit()
        return redirect(url_for('product'))

    @app.route('/delete_product/<int:product_id>', methods=['POST'])
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('product'))
    
    @app.route('/edit_order/<int:order_id>', methods=['POST'])
    def edit_order(order_id):
        order = Order.query.get_or_404(order_id)

        if order.user_id != current_user.id:
            abort(403)

        order.customer_name = request.form['customer_name']
        order.status = request.form['status']

        db.session.commit()
        return redirect(url_for('orders'))  # or wherever your order list is rendered
    
    @app.route('/delete_order/<int:order_id>', methods=['POST'])
    def delete_order(order_id):
        order = Order.query.get_or_404(order_id)
    
        if order.user_id != current_user.id:
            abort(403)
    
        db.session.delete(order)
        db.session.commit()
        return redirect(url_for('orders'))

    @app.route('/stock')
    def stock():
        products = Product.query.filter_by(user_id=current_user.id).order_by(Product.quantity_in_stock.asc()).all()
        return render_template('stock.html', products=products)

    @app.route('/update_stock', methods=['POST'])
    def update_stock():
        product_id = request.form.get('product_id')
        new_quantity = request.form.get('new_quantity')

        if not product_id or not new_quantity:
            return "Missing product ID or quantity", 400

        try:
            product = Product.query.get(int(product_id))
            product.quantity_in_stock = int(new_quantity)
            db.session.commit()
            return redirect(url_for('stock'))  # or 'dashboard', or wherever you want
        except Exception as e:
            return f"Error: {e}", 500
    
    @app.route('/orders')
    def orders():
        all_orders = Order.query.filter_by(user_id=current_user.id)
        search_query = request.args.get('search', '').strip()

        return render_template('orders.html',
                               orders=all_orders)
    
    
    @app.route('/settings', methods=['GET', 'POST'])
    @app.route('/settings/<tab>', methods=['GET', 'POST'])
    @login_required
    def settings(tab='profile'):
        if tab not in ['profile', 'categories', 'suppliers']:
            tab = 'profile'

        # Handle profile update
        if request.method == 'POST' and tab == 'profile':
            email = request.form.get('email')
            display_name = request.form.get('display_name')
            password = request.form.get('password')

            if email:
                current_user.email = email
            if display_name:
                current_user.username = display_name
                if password and password != '••••••••':
                    is_valid, msg = is_password_valid(password)
                if not is_valid:
                    flash(msg, 'danger')
                    return redirect(url_for('settings', tab=tab))
                current_user.set_password(password)

            try:
                db.session.commit()
                flash('Profile updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating profile: {str(e)}', 'danger')

            return redirect(url_for('settings', tab=tab))

        # Load suppliers only if that tab is active
        suppliers = []
        if tab == 'suppliers':
            suppliers = Supplier.query.filter_by(user_id=current_user.id).all()

        return render_template(
            'settings.html',
            user=current_user,
            active_tab=tab,
            suppliers=suppliers  # Always safe to pass (empty if not tab)
        )




    return app