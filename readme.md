# Canteen Ordering System

A Django-based canteen ordering system that allows users to browse menus, place orders, and manage food items.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Setup Instructions

1. **Clone the repository** (if not already done)
   ```bash
   git clone <repository-url>
   cd canteen_ordering
   ```

2. **Set up a virtual environment** (recommended)
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   # python -m venv venv
   # venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

## Running the Development Server

1. **Activate the virtual environment** (if not already activated)
   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   # venv\Scripts\activate
   ```

2. **Start the development server**
   ```bash
   python manage.py runserver
   ```

3. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Stopping the Server

To stop the development server, press `Ctrl+C` in the terminal where it's running.

## Project Structure

- `/canteen_ordering/` - Main project configuration
- `/menu/` - Menu-related functionality
- `/orders/` - Order management
- `/qrcode/` - QR code generation and handling
- `/templates/` - HTML templates
- `/users/` - User authentication and management

## Troubleshooting

- If you encounter dependency issues, try:
  ```bash
  pip install --upgrade -r requirements.txt
  ```
- If the database has issues, you can reset it with:
  ```bash
  rm db.sqlite3
  python manage.py migrate
  python manage.py createsuperuser
  ```

## License

[Specify your license here]

# e-dine # e-dine