@echo off
echo ========================================
echo Clothing Store Inventory Management System
echo Build Script for Windows EXE
echo ========================================
echo.

echo Installing required dependencies...
pip install -r requirements.txt

echo.
echo Cleaning previous build files...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"

echo.
echo Building executable with PyInstaller...
pyinstaller --clean clothing_store.spec

echo.
echo Copying additional files to distribution...
if not exist "dist\ClothingStoreInventory" mkdir "dist\ClothingStoreInventory"
copy "README.md" "dist\ClothingStoreInventory\"
copy "USER_MANUAL.md" "dist\ClothingStoreInventory\"
copy "add_sample_data.py" "dist\ClothingStoreInventory\"

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your executable is located at:
echo dist\ClothingStoreInventory\ClothingStoreInventory.exe
echo.
echo To run the application:
echo 1. Navigate to dist\ClothingStoreInventory\
echo 2. Double-click ClothingStoreInventory.exe
echo.
echo First-time login credentials:
echo Username: admin
echo Password: admin123
echo.
pause
