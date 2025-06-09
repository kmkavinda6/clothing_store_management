# Clothing Store Inventory Management System - User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [User Roles and Access](#user-roles-and-access)
3. [Dashboard Overview](#dashboard-overview)
4. [Style Management](#style-management)
5. [Inventory Management](#inventory-management)
6. [Search and Retrieval](#search-and-retrieval)
7. [Rack Management](#rack-management)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements
- Python 3.6 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Minimum 4GB RAM
- 1GB available disk space

### Starting the Application
1. Navigate to the application folder
2. Run: `python3 main.py` or `./start.sh`
3. The application will open in your default browser at `http://localhost:8080`

### First Login
Use the default administrator credentials:
- **Username**: admin
- **Password**: admin123

## User Roles and Access

### Store Manager (Full Access)
**Capabilities:**
- Add and manage clothing styles
- View comprehensive dashboard
- Access all inventory functions
- Generate reports and analytics
- Manage user accounts (future feature)

**Primary Tasks:**
- Define new product styles
- Monitor overall inventory performance
- Analyze sales and stock data
- Make strategic inventory decisions

### Store Worker (Operational Access)
**Capabilities:**
- Add inventory items to racks
- Search for items by various criteria
- Update inventory quantities
- Get rack placement suggestions

**Primary Tasks:**
- Receive new inventory shipments
- Place items in optimal rack locations
- Fulfill customer orders
- Maintain accurate stock counts

### Dispatcher (Order Processing)
**Capabilities:**
- Search inventory for order fulfillment
- View rack locations for picking
- Process order verification (future feature)
- Update order status (future feature)

**Primary Tasks:**
- Pick items for orders
- Verify order accuracy
- Manage shipping processes
- Handle returns and exchanges

## Dashboard Overview

The dashboard provides real-time insights into your inventory system:

### Key Metrics Cards
- **Total Styles**: Number of different clothing styles in system
- **Total Items**: Sum of all inventory quantities
- **Total Racks**: Number of storage locations
- **Low Stock Items**: Items with quantity below 5 units

### Recent Transactions
- Real-time activity feed
- Shows user actions and timestamps
- Tracks inventory movements
- Monitors system usage

### Rack Utilization
- Average percentage of rack space used
- Visual indicator of storage efficiency
- Helps identify over/under-utilized areas

## Style Management

### Adding New Styles (Store Manager Only)

1. **Navigate to Style Management tab**
2. **Fill in required information:**
   - **Style Number**: Unique identifier (e.g., ST001, JEANS001)
   - **Style Name**: Descriptive name (e.g., "Classic Blue Jeans")
   - **Category**: Product category (Mens, Womens, Jeans, etc.)
   - **Vendor**: Supplier information
   - **Description**: Detailed product description

3. **Specify Variations:**
   - **Available Sizes**: Comma-separated list (S,M,L,XL)
   - **Available Colors**: Comma-separated list (Blue,Black,White)

4. **Click "Add Style"** to save

### Style Information Guidelines
- Use consistent naming conventions
- Include comprehensive size ranges
- Specify all available color variations
- Add detailed descriptions for clarity

## Inventory Management

### Adding Inventory Items

1. **Select the Inventory tab**
2. **Choose from existing styles** or add new ones
3. **Specify item details:**
   - Size (must match available sizes)
   - Color (must match available colors)
   - Quantity (number of items)

4. **Rack Placement:**
   - Select from available racks
   - Use "Suggest Optimal Rack" for recommendations
   - System considers current utilization

### Rack Optimization Algorithm

The system automatically suggests optimal rack placement based on:
- **Current utilization**: Prefers less crowded racks
- **Available capacity**: Ensures sufficient space
- **Style grouping**: Attempts to group similar items
- **Accessibility**: Considers ease of retrieval

### Best Practices for Inventory
- Group similar styles together
- Maintain consistent organization
- Regular stock level monitoring
- Use suggested rack placements

## Search and Retrieval

### Search Functionality

**Search by multiple criteria:**
- **Style Number**: Exact or partial match
- **Color**: Filter by specific colors
- **Size**: Find specific size availability

**Search Results Include:**
- Style number and name
- Size and color information
- Current quantity available
- Exact rack location
- Rack physical location description

### Order Fulfillment Process

1. **Search for required items**
2. **Note rack locations** for efficient picking
3. **Verify quantities** before retrieval
4. **Update inventory** after picking (future feature)

## Rack Management

### Understanding Rack Information

**Rack Display Shows:**
- Rack ID (e.g., A-1-1, B-2-3)
- Physical location description
- Current utilization count
- Total capacity
- Utilization percentage

### Utilization Color Coding
- **Green (0-50%)**: Low utilization, good availability
- **Yellow (50-80%)**: Medium utilization, moderate space
- **Red (80-100%)**: High utilization, limited space

### Rack Organization Strategy
- Distribute inventory evenly
- Avoid overloading single racks
- Group related items when possible
- Maintain accessibility paths

## Best Practices

### Daily Operations
1. **Morning**: Check dashboard for low stock alerts
2. **Receiving**: Use optimal rack suggestions for new inventory
3. **Fulfillment**: Use search function for efficient picking
4. **Evening**: Review utilization and reorganize if needed

### Data Quality
- Use consistent naming conventions
- Maintain accurate quantity counts
- Regular inventory audits
- Proper category assignment

### System Maintenance
- Regular database backups
- Monitor system performance
- Keep transaction logs for auditing
- Update user access as needed

## Sample Data Overview

The system includes sample data for demonstration:

### Sample Styles
- **ST001**: Classic Denim Jeans (Levi Strauss)
- **ST002**: Cotton T-Shirt (Hanes)
- **ST003**: Summer Dress (H&M)
- **ST004**: Casual Shirt (Van Heusen)
- **ST005**: Leather Jacket (Wilson Leather)
- **ST006**: Sports Bra (Nike)
- **ST007**: Cargo Pants (Dickies)
- **ST008**: Blouse (Ann Taylor)

### Sample User Accounts
- **admin** / admin123 (Store Manager)
- **store_worker** / worker123 (Store Worker)
- **dispatcher** / dispatch123 (Dispatcher)

## Troubleshooting

### Common Issues

**Login Problems:**
- Verify username and password
- Check if database file exists
- Restart application if needed

**Search Not Working:**
- Check search criteria spelling
- Verify items exist in inventory
- Clear search filters and retry

**Rack Suggestions Unavailable:**
- Ensure racks have available capacity
- Check if quantity exceeds available space
- Add more racks if needed

**Performance Issues:**
- Close unnecessary browser tabs
- Restart the application
- Check system resources

### Error Messages

**"Style number already exists"**
- Use a unique style number
- Check existing styles first

**"No available rack space"**
- Reduce quantity or choose different rack
- Add more racks to system

**"Unauthorized"**
- Check user role permissions
- Login with appropriate account

### Getting Help

For technical support:
1. Check this user manual
2. Review error messages carefully
3. Restart the application
4. Contact system administrator

## Future Enhancements

Planned features for future versions:
- Order processing workflow
- Barcode scanner integration
- Advanced reporting
- Email notifications
- Multi-store support
- Mobile app companion

---

**Version**: 1.0  
**Last Updated**: June 9, 2025  
**For Technical Support**: Contact System Administrator
