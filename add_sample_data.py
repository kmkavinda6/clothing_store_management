#!/usr/bin/env python3
"""
Sample data generator for Clothing Store Inventory Management System
"""

import sqlite3
import hashlib
from datetime import datetime

DB_PATH = 'inventory.db'

def add_sample_data():
    """Add sample data to the database for demonstration"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Add sample users
    sample_users = [
        ('store_worker', hashlib.md5('worker123'.encode()).hexdigest(), 'Store Worker', 'worker@store.com'),
        ('dispatcher', hashlib.md5('dispatch123'.encode()).hexdigest(), 'Dispatcher', 'dispatcher@store.com'),
    ]
    
    for username, password_hash, role, email in sample_users:
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, role, email)
            VALUES (?, ?, ?, ?)
        ''', (username, password_hash, role, email))
    
    # Add sample styles
    sample_styles = [
        ('ST001', 'Classic Denim Jeans', 'Jeans', 'Premium quality denim jeans', 'Levi Strauss', 'S,M,L,XL,XXL', 'Blue,Black,Dark Blue'),
        ('ST002', 'Cotton T-Shirt', 'Mens', 'Comfortable cotton t-shirt', 'Hanes', 'S,M,L,XL', 'White,Black,Red,Blue'),
        ('ST003', 'Summer Dress', 'Womens', 'Light summer dress', 'H&M', 'XS,S,M,L', 'Yellow,Pink,White,Floral'),
        ('ST004', 'Casual Shirt', 'Mens', 'Business casual shirt', 'Van Heusen', 'S,M,L,XL', 'White,Blue,Gray'),
        ('ST005', 'Leather Jacket', 'Mens', 'Genuine leather jacket', 'Wilson Leather', 'M,L,XL', 'Black,Brown'),
        ('ST006', 'Sports Bra', 'Womens', 'Athletic sports bra', 'Nike', 'XS,S,M,L', 'Black,White,Pink'),
        ('ST007', 'Cargo Pants', 'Mens', 'Multi-pocket cargo pants', 'Dickies', 'S,M,L,XL', 'Khaki,Black,Navy'),
        ('ST008', 'Blouse', 'Womens', 'Professional blouse', 'Ann Taylor', 'XS,S,M,L,XL', 'White,Black,Navy,Pink'),
    ]
    
    style_ids = []
    for style_number, style_name, category, description, vendor, sizes, colors in sample_styles:
        cursor.execute('''
            INSERT OR IGNORE INTO styles (style_number, style_name, category, description, 
                                        vendor, available_sizes, available_colors)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (style_number, style_name, category, description, vendor, sizes, colors))
        
        # Get the style ID
        cursor.execute('SELECT id FROM styles WHERE style_number = ?', (style_number,))
        result = cursor.fetchone()
        if result:
            style_ids.append(result[0])
    
    # Get rack IDs
    cursor.execute('SELECT id FROM racks')
    rack_ids = [row[0] for row in cursor.fetchall()]
    
    # Add sample inventory
    sample_inventory = [
        (style_ids[0] if len(style_ids) > 0 else 1, 'M', 'Blue', 25, rack_ids[0] if len(rack_ids) > 0 else 1),
        (style_ids[0] if len(style_ids) > 0 else 1, 'L', 'Blue', 30, rack_ids[0] if len(rack_ids) > 0 else 1),
        (style_ids[0] if len(style_ids) > 0 else 1, 'M', 'Black', 20, rack_ids[1] if len(rack_ids) > 1 else 1),
        (style_ids[1] if len(style_ids) > 1 else 1, 'M', 'White', 50, rack_ids[1] if len(rack_ids) > 1 else 1),
        (style_ids[1] if len(style_ids) > 1 else 1, 'L', 'Black', 35, rack_ids[2] if len(rack_ids) > 2 else 1),
        (style_ids[2] if len(style_ids) > 2 else 1, 'S', 'Yellow', 15, rack_ids[2] if len(rack_ids) > 2 else 1),
        (style_ids[2] if len(style_ids) > 2 else 1, 'M', 'Pink', 20, rack_ids[3] if len(rack_ids) > 3 else 1),
        (style_ids[3] if len(style_ids) > 3 else 1, 'M', 'White', 40, rack_ids[3] if len(rack_ids) > 3 else 1),
        (style_ids[3] if len(style_ids) > 3 else 1, 'L', 'Blue', 25, rack_ids[4] if len(rack_ids) > 4 else 1),
        (style_ids[4] if len(style_ids) > 4 else 1, 'L', 'Black', 8, rack_ids[4] if len(rack_ids) > 4 else 1),
        (style_ids[5] if len(style_ids) > 5 else 1, 'M', 'Black', 30, rack_ids[5] if len(rack_ids) > 5 else 1),
        (style_ids[6] if len(style_ids) > 6 else 1, 'L', 'Khaki', 18, rack_ids[5] if len(rack_ids) > 5 else 1),
        (style_ids[7] if len(style_ids) > 7 else 1, 'M', 'White', 22, rack_ids[6] if len(rack_ids) > 6 else 1),
    ]
    
    for style_id, size, color, quantity, rack_id in sample_inventory:
        cursor.execute('''
            INSERT OR IGNORE INTO inventory (style_id, size, color, quantity, rack_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (style_id, size, color, quantity, rack_id))
    
    # Update rack utilization
    cursor.execute('''
        UPDATE racks SET current_utilization = (
            SELECT COALESCE(SUM(quantity), 0) 
            FROM inventory 
            WHERE rack_id = racks.id AND status = 'active'
        )
    ''')
    
    # Add sample transactions
    cursor.execute('SELECT id FROM users WHERE username = "admin"')
    admin_id = cursor.fetchone()[0]
    
    sample_transactions = [
        ('ADD_STYLE', admin_id, 'Added style: Classic Denim Jeans'),
        ('ADD_STYLE', admin_id, 'Added style: Cotton T-Shirt'),
        ('ADD_INVENTORY', admin_id, 'Added 25 items to rack A-1-1'),
        ('ADD_INVENTORY', admin_id, 'Added 30 items to rack A-1-1'),
        ('ADD_INVENTORY', admin_id, 'Added 50 items to rack A-1-2'),
    ]
    
    for transaction_type, user_id, details in sample_transactions:
        cursor.execute('''
            INSERT INTO transactions (transaction_type, user_id, details)
            VALUES (?, ?, ?)
        ''', (transaction_type, user_id, details))
    
    conn.commit()
    conn.close()
    
    print("Sample data added successfully!")
    print("\nAdditional user accounts created:")
    print("Username: store_worker, Password: worker123, Role: Store Worker")
    print("Username: dispatcher, Password: dispatch123, Role: Dispatcher")

if __name__ == '__main__':
    add_sample_data()
