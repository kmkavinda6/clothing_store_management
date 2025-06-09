# Clothing Store Inventory Management System

A Python Eel-based desktop application for managing clothing store inventory with an intuitive web interface.

## Features

- **User Management**: Role-based access control (Store Manager, Store Worker, Dispatcher)
- **Style Management**: Add, edit, and manage clothing styles with detailed information
- **Inventory Management**: Track inventory items with rack placement optimization
- **Search Functionality**: Search inventory by style, color, size with real-time results
- **Rack Management**: Visual rack utilization tracking and optimization
- **Dashboard**: Real-time statistics and recent transactions
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Technology Stack

- **Backend**: Python with Eel framework
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite
- **UI Framework**: Bootstrap 5 with Font Awesome icons

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

The application will start and open in your default web browser at `http://localhost:8080`.

## Default Login Credentials

- **Username**: admin
- **Password**: admin123
- **Role**: Store Manager

## User Roles and Permissions

### Store Manager
- Add new clothing styles
- Generate reports
- Access all system features
- View dashboard and analytics

### Store Worker
- Add inventory items
- Search inventory
- Retrieve items for orders
- Update inventory quantities

### Dispatcher
- Verify and process orders
- View order details
- Update order status

## Key Features Guide

### Dashboard
- View real-time inventory statistics
- Monitor rack utilization
- Track recent system activities
- Low stock alerts

### Style Management (Store Manager Only)
- Add new clothing styles with detailed information
- Specify available sizes and colors
- Set vendor information and descriptions
- View all existing styles

### Inventory Management
- Add new inventory items to racks
- Get optimal rack placement suggestions
- Track quantities by style, size, and color
- Monitor rack utilization

### Search Functionality
- Search by style number, color, and size
- View exact rack locations
- Real-time search results
- Quantity and availability status

### Rack Management
- Visual representation of all racks
- Utilization percentage tracking
- Capacity management
- Location tracking

## Database Schema

The application uses SQLite with the following main tables:

- **users**: User accounts and roles
- **styles**: Clothing style information
- **racks**: Storage rack details
- **inventory**: Item inventory with location tracking
- **orders**: Order management (for future enhancement)
- **transactions**: Activity logging

## Project Structure

```
clothing_store_inventory/
├── main.py                 # Main Python application
├── requirements.txt        # Python dependencies
├── inventory.db           # SQLite database (created automatically)
├── web/                   # Frontend files
│   ├── index.html         # Main HTML interface
│   ├── css/
│   │   └── styles.css     # Custom CSS styles
│   └── js/
│       └── app.js         # Frontend JavaScript
└── README.md              # This file
```

## API Functions

The Python backend exposes these functions to the frontend:

- `login(username, password)`: User authentication
- `logout()`: User logout
- `get_current_user()`: Get current user info
- `get_styles()`: Retrieve all styles
- `add_style(style_data)`: Add new style
- `get_racks()`: Retrieve all racks
- `get_optimal_rack(style_id, quantity)`: Get rack suggestion
- `add_inventory(inventory_data)`: Add inventory item
- `search_inventory(search_params)`: Search inventory
- `get_dashboard_stats()`: Get dashboard statistics

## Future Enhancements

- Order processing workflow
- Barcode scanner integration
- Excel import/export functionality
- Advanced reporting features
- Email notifications
- Backup and restore functionality
- Multi-store support

## Troubleshooting

### Common Issues

1. **Application won't start**:
   - Ensure Python 3.6+ is installed
   - Check that all dependencies are installed: `pip install -r requirements.txt`

2. **Database errors**:
   - Delete `inventory.db` file to reset the database
   - Restart the application to recreate tables

3. **Login issues**:
   - Use default credentials: admin/admin123
   - Database is recreated with default user on startup

4. **Port conflicts**:
   - If port 8080 is in use, modify the port in `main.py`
   - Change `eel.start('index.html', size=(1200, 800), port=8080)`

### Support

For issues or questions, please refer to the requirements document or check the code comments for detailed functionality information.

## Development Notes

- The application uses a single-file SQLite database for simplicity
- All frontend assets are served by the Eel framework
- The interface is fully responsive and works on mobile devices
- Role-based access control is implemented on both frontend and backend
- Transaction logging is implemented for audit purposes

## Security Considerations

- Passwords are hashed using MD5 (for demo purposes - use stronger hashing in production)
- Role-based access control prevents unauthorized actions
- All database operations use parameterized queries to prevent SQL injection
- Frontend validation is backed by server-side validation
