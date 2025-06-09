#!/usr/bin/env python3
"""
Clothing Store Inventory Management System
Main application entry point using Python Eel
"""

import eel
import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import hashlib

# Initialize Eel
eel.init('web')

# Database setup
DB_PATH = 'inventory.db'

class InventoryDatabase:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Styles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS styles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                style_number TEXT UNIQUE NOT NULL,
                style_name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                vendor TEXT,
                available_sizes TEXT,
                available_colors TEXT,
                images TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Racks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS racks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rack_id TEXT UNIQUE NOT NULL,
                location TEXT NOT NULL,
                capacity INTEGER DEFAULT 100,
                current_utilization INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                style_id INTEGER,
                size TEXT NOT NULL,
                color TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                rack_id INTEGER,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (style_id) REFERENCES styles (id),
                FOREIGN KEY (rack_id) REFERENCES racks (id)
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT UNIQUE NOT NULL,
                customer_name TEXT,
                customer_email TEXT,
                customer_phone TEXT,
                status TEXT DEFAULT 'pending',
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                inventory_id INTEGER,
                quantity INTEGER NOT NULL,
                picked BOOLEAN DEFAULT 0,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (inventory_id) REFERENCES inventory (id)
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                user_id INTEGER,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Insert default admin user
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, role, email)
            VALUES (?, ?, ?, ?)
        ''', ('admin', hashlib.md5('admin123'.encode()).hexdigest(), 'Store Manager', 'admin@store.com'))
        
        # Insert sample racks
        sample_racks = [
            ('A-1-1', 'Section A, Row 1, Position 1'),
            ('A-1-2', 'Section A, Row 1, Position 2'),
            ('A-1-3', 'Section A, Row 1, Position 3'),
            ('A-2-1', 'Section A, Row 2, Position 1'),
            ('A-2-2', 'Section A, Row 2, Position 2'),
            ('B-1-1', 'Section B, Row 1, Position 1'),
            ('B-1-2', 'Section B, Row 1, Position 2'),
        ]
        
        for rack_id, location in sample_racks:
            cursor.execute('''
                INSERT OR IGNORE INTO racks (rack_id, location)
                VALUES (?, ?)
            ''', (rack_id, location))
        
        conn.commit()
        conn.close()

# Initialize database
db = InventoryDatabase()

# Session management
current_user = None

@eel.expose
def login(username: str, password: str) -> Dict:
    """User login function"""
    global current_user
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    password_hash = hashlib.md5(password.encode()).hexdigest()
    cursor.execute('''
        SELECT id, username, role, email FROM users 
        WHERE username = ? AND password_hash = ?
    ''', (username, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        current_user = {
            'id': user[0],
            'username': user[1],
            'role': user[2],
            'email': user[3]
        }
        return {'success': True, 'user': current_user}
    else:
        return {'success': False, 'message': 'Invalid credentials'}

@eel.expose
def logout() -> Dict:
    """User logout function"""
    global current_user
    current_user = None
    return {'success': True}

@eel.expose
def get_current_user() -> Optional[Dict]:
    """Get current logged in user"""
    return current_user

@eel.expose
def get_styles() -> List[Dict]:
    """Get all active styles"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, style_number, style_name, category, description, 
               vendor, available_sizes, available_colors, images
        FROM styles 
        WHERE is_active = 1
        ORDER BY style_name
    ''')
    
    styles = []
    for row in cursor.fetchall():
        styles.append({
            'id': row[0],
            'style_number': row[1],
            'style_name': row[2],
            'category': row[3],
            'description': row[4],
            'vendor': row[5],
            'available_sizes': row[6].split(',') if row[6] else [],
            'available_colors': row[7].split(',') if row[7] else [],
            'images': row[8].split(',') if row[8] else []
        })
    
    conn.close()
    return styles

@eel.expose
def add_style(style_data: Dict) -> Dict:
    """Add a new style"""
    if not current_user or current_user['role'] != 'Store Manager':
        return {'success': False, 'message': 'Unauthorized'}
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO styles (style_number, style_name, category, description, 
                              vendor, available_sizes, available_colors)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            style_data['style_number'],
            style_data['style_name'],
            style_data['category'],
            style_data.get('description', ''),
            style_data.get('vendor', ''),
            ','.join(style_data.get('available_sizes', [])),
            ','.join(style_data.get('available_colors', []))
        ))
        
        conn.commit()
        
        # Log transaction
        cursor.execute('''
            INSERT INTO transactions (transaction_type, user_id, details)
            VALUES (?, ?, ?)
        ''', ('ADD_STYLE', current_user['id'], f"Added style: {style_data['style_name']}"))
        
        conn.commit()
        conn.close()
        
        return {'success': True, 'message': 'Style added successfully'}
    except sqlite3.IntegrityError:
        conn.close()
        return {'success': False, 'message': 'Style number already exists'}
    except Exception as e:
        conn.close()
        return {'success': False, 'message': str(e)}

@eel.expose
def get_racks() -> List[Dict]:
    """Get all racks"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, rack_id, location, capacity, current_utilization
        FROM racks
        ORDER BY rack_id
    ''')
    
    racks = []
    for row in cursor.fetchall():
        utilization_percent = (row[4] / row[3]) * 100 if row[3] > 0 else 0
        racks.append({
            'id': row[0],
            'rack_id': row[1],
            'location': row[2],
            'capacity': row[3],
            'current_utilization': row[4],
            'utilization_percent': round(utilization_percent, 1)
        })
    
    conn.close()
    return racks

@eel.expose
def get_optimal_rack(style_id: int, quantity: int) -> Dict:
    """Get optimal rack suggestion for inventory placement"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Find racks with lowest utilization that can accommodate the quantity
    cursor.execute('''
        SELECT id, rack_id, location, capacity, current_utilization
        FROM racks
        WHERE (capacity - current_utilization) >= ?
        ORDER BY current_utilization ASC
        LIMIT 1
    ''', (quantity,))
    
    rack = cursor.fetchone()
    
    if rack:
        result = {
            'success': True,
            'rack': {
                'id': rack[0],
                'rack_id': rack[1],
                'location': rack[2],
                'available_space': rack[3] - rack[4]
            }
        }
    else:
        result = {'success': False, 'message': 'No available rack space for this quantity'}
    
    conn.close()
    return result

@eel.expose
def add_inventory(inventory_data: Dict) -> Dict:
    """Add inventory to a rack"""
    if not current_user or current_user['role'] not in ['Store Manager', 'Store Worker']:
        return {'success': False, 'message': 'Unauthorized'}
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Add inventory
        cursor.execute('''
            INSERT INTO inventory (style_id, size, color, quantity, rack_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            inventory_data['style_id'],
            inventory_data['size'],
            inventory_data['color'],
            inventory_data['quantity'],
            inventory_data['rack_id']
        ))
        
        # Update rack utilization
        cursor.execute('''
            UPDATE racks 
            SET current_utilization = current_utilization + ?
            WHERE id = ?
        ''', (inventory_data['quantity'], inventory_data['rack_id']))
        
        # Log transaction
        cursor.execute('''
            INSERT INTO transactions (transaction_type, user_id, details)
            VALUES (?, ?, ?)
        ''', ('ADD_INVENTORY', current_user['id'], 
              f"Added {inventory_data['quantity']} items to rack"))
        
        conn.commit()
        conn.close()
        
        return {'success': True, 'message': 'Inventory added successfully'}
    except Exception as e:
        conn.close()
        return {'success': False, 'message': str(e)}

@eel.expose
def search_inventory(search_params: Dict) -> List[Dict]:
    """Search inventory by style, color, size"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = '''
        SELECT i.id, s.style_number, s.style_name, i.size, i.color, 
               i.quantity, r.rack_id, r.location, i.status
        FROM inventory i
        JOIN styles s ON i.style_id = s.id
        JOIN racks r ON i.rack_id = r.id
        WHERE i.status = 'active' AND i.quantity > 0
    '''
    params = []
    
    if search_params.get('style_number'):
        query += ' AND s.style_number LIKE ?'
        params.append(f"%{search_params['style_number']}%")
    
    if search_params.get('color'):
        query += ' AND i.color LIKE ?'
        params.append(f"%{search_params['color']}%")
    
    if search_params.get('size'):
        query += ' AND i.size = ?'
        params.append(search_params['size'])
    
    query += ' ORDER BY s.style_name, i.size, i.color'
    
    cursor.execute(query, params)
    
    inventory = []
    for row in cursor.fetchall():
        inventory.append({
            'id': row[0],
            'style_number': row[1],
            'style_name': row[2],
            'size': row[3],
            'color': row[4],
            'quantity': row[5],
            'rack_id': row[6],
            'rack_location': row[7],
            'status': row[8]
        })
    
    conn.close()
    return inventory

@eel.expose
def get_dashboard_stats() -> Dict:
    """Get dashboard statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total styles
    cursor.execute('SELECT COUNT(*) FROM styles WHERE is_active = 1')
    total_styles = cursor.fetchone()[0]
    
    # Total inventory items
    cursor.execute('SELECT SUM(quantity) FROM inventory WHERE status = "active"')
    total_items = cursor.fetchone()[0] or 0
    
    # Total racks
    cursor.execute('SELECT COUNT(*) FROM racks')
    total_racks = cursor.fetchone()[0]
    
    # Average rack utilization
    cursor.execute('SELECT AVG(current_utilization * 100.0 / capacity) FROM racks WHERE capacity > 0')
    avg_utilization = cursor.fetchone()[0] or 0
    
    # Low stock items (quantity < 5)
    cursor.execute('''
        SELECT COUNT(*) FROM inventory 
        WHERE status = "active" AND quantity < 5
    ''')
    low_stock_items = cursor.fetchone()[0]
    
    # Recent transactions
    cursor.execute('''
        SELECT t.transaction_type, t.details, t.timestamp, u.username
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.timestamp DESC
        LIMIT 10
    ''')
    
    recent_transactions = []
    for row in cursor.fetchall():
        recent_transactions.append({
            'type': row[0],
            'details': row[1],
            'timestamp': row[2],
            'user': row[3]
        })
    
    conn.close()
    
    return {
        'total_styles': total_styles,
        'total_items': total_items,
        'total_racks': total_racks,
        'avg_utilization': round(avg_utilization, 1),
        'low_stock_items': low_stock_items,
        'recent_transactions': recent_transactions
    }

def main():
    """Start the application"""
    print("Starting Clothing Store Inventory Management System...")
    eel.start('index.html', size=(1200, 800), port=8080)

if __name__ == '__main__':
    main()
