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
   git clone https://github.com/Adhi1755/inventoryHubgit
   cd inventoryHub
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
