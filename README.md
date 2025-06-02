# InventoryHub
# Inventory Management System

A comprehensive web-based inventory management system built with Flask that helps businesses track their products, manage orders, monitor stock levels, and analyze sales performance through an intuitive dashboard.

## 🚀 Features

### 🔐 Authentication System
- **User Registration & Login**: Create your own account with secure authentication
- **Session Management**: Secure user sessions and account protection
- **Profile Management**: Update login credentials and account details in settings

### 📊 Interactive Dashboard
- **Monthly Sales Charts**: Visual representation of sales performance over time
- **Stock Level Charts**: Real-time monitoring of inventory levels
- **Recent Orders Overview**: Quick access to latest order information
- **Revenue Analytics**: Track income and financial performance
- **Stock Alerts**: Monitor low stock levels and inventory status

### 📦 Product Management
- **Add New Products**: Easily add products to your inventory
- **Edit Products**: Update product information, pricing, and details
- **Product Categories**: Organize products efficiently
- **Stock Tracking**: Monitor product availability and quantities

### 🛒 Order Management
- **Order Creation**: Process new orders seamlessly
- **Edit Orders**: Modify existing orders as needed
- **Order History**: Access complete order records
- **Order Status Tracking**: Monitor order fulfillment progress

### 📈 Stock Management
- **Real-time Stock Levels**: Track current inventory quantities
- **Stock Adjustments**: Update stock levels manually
- **Low Stock Alerts**: Get notified when items run low
- **Stock Reports**: Generate detailed inventory reports

### ⚙️ Settings & Configuration
- **Account Settings**: Update personal information and login credentials
- **System Preferences**: Customize application behavior
- **Security Settings**: Manage password and security options

### 🎨 User Experience
- **Modern UI Design**: Clean, intuitive, and responsive interface
- **Mobile Friendly**: Optimized for all device sizes
- **Fast Performance**: Efficient loading and smooth navigation
- **User-Friendly**: Designed for ease of use and productivity

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite/PostgreSQL (configurable)
- **Charts**: Chart.js for data visualization
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- Git
- pip (Python package installer)

## 🚀 Installation & Setup

### Option 1: Clone from GitHub

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/inventory-management-system.git
   cd inventory-management-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create a .env file in the root directory
   touch .env
   
   # Add the following to .env file:
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///inventory.db
   ```

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   flask run
   ```

7. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

### Option 2: Download ZIP

1. **Download the ZIP file** from the GitHub repository
2. **Extract** the files to your desired location
3. **Follow steps 2-7** from Option 1 above

## 🖥️ Usage

1. **Create Account**: Register a new account on the login page
2. **Login**: Access your dashboard with your credentials
3. **Dashboard**: View your sales charts, stock levels, and recent orders
4. **Add Products**: Navigate to Products page to add your inventory items
5. **Manage Orders**: Use the Orders page to process and track orders
6. **Monitor Stock**: Check stock levels and adjust quantities as needed
7. **Settings**: Update your account information and preferences

## 📁 Project Structure

```
inventory-management-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── config.py             # Configuration settings
├── models.py             # Database models
├── forms.py              # Flask-WTF forms
├── routes/               # Route handlers
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   ├── products.py      # Product management routes
│   ├── orders.py        # Order management routes
│   └── settings.py      # Settings routes
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── dashboard.html   # Dashboard page
│   ├── products.html    # Products page
│   ├── orders.html      # Orders page
│   └── settings.html    # Settings page
├── static/              # Static files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Image assets
└── migrations/          # Database migrations
```

## 🔧 Configuration

### Database Configuration
- **SQLite** (default): For development and small-scale deployment
- **PostgreSQL**: For production environments

### Environment Variables
```env
FLASK_APP=app.py
FLASK_ENV=production  # Change to 'development' for development
SECRET_KEY=your-very-secret-key
DATABASE_URL=your-database-url
```

## 🚀 Deployment

### Local Development
```bash
flask run --debug
```

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use a proper WSGI server like Gunicorn
3. Configure a reverse proxy (Nginx)
4. Set up a production database (PostgreSQL)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Bug Reports & Feature Requests

If you encounter any bugs or have feature requests, please create an issue on the GitHub repository.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review existing issues for solutions

## 🎉 Acknowledgments

- Flask community for the excellent framework
- Contributors who helped improve this project
- Open source libraries that made this project possible

---

**Made with ❤️ for efficient inventory management**
