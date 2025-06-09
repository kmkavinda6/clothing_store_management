#!/bin/bash

# Clothing Store Inventory Management System Startup Script

echo "Starting Clothing Store Inventory Management System..."
echo "=========================================="
echo ""
echo "Default Login Credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "The application will open in your default web browser."
echo "Press Ctrl+C to stop the application."
echo ""

# Change to the application directory
cd "$(dirname "$0")"

# Run the Python application
python3 main.py
