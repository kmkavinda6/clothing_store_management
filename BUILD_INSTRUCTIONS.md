# Building the Clothing Store Inventory System to EXE

## Prerequisites

1. **Python 3.6+** installed on your system
2. **pip** package manager
3. **Windows** operating system

## Build Process

### Option 1: Automated Build (Recommended)

1. Open Command Prompt or PowerShell as Administrator
2. Navigate to the project directory:
   ```cmd
   cd "d:\work\clothing_store_management-main"
   ```
3. Run the build script:
   ```cmd
   build.bat
   ```

The script will:
- Install required dependencies
- Clean previous builds
- Create the executable using PyInstaller
- Copy documentation files
- Show completion message

### Option 2: Manual Build

1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

2. Build with PyInstaller:
   ```cmd
   pyinstaller --clean clothing_store.spec
   ```

## After Building

The executable will be created in:
```
dist\ClothingStoreInventory\ClothingStoreInventory.exe
```

## Distribution

To distribute the application:

1. Copy the entire `dist\ClothingStoreInventory\` folder
2. Include the following files in the distribution:
   - `ClothingStoreInventory.exe` (main executable)
   - `web\` folder (contains the web interface)
   - `README.md` (documentation)
   - `USER_MANUAL.md` (user guide)
   - `start_exe.bat` (optional startup script)

## Running the Executable

### Method 1: Direct
Double-click `ClothingStoreInventory.exe`

### Method 2: With Startup Script
1. Copy `start_exe.bat` to the same folder as the executable
2. Double-click `start_exe.bat`

## Default Login
- **Username**: admin
- **Password**: admin123

## Database Location

The SQLite database (`inventory.db`) will be created in the same directory as the executable when first run.

## Troubleshooting

### Common Issues

1. **Missing DLL errors**: Install Microsoft Visual C++ Redistributable
2. **Port already in use**: Close other applications using port 8080
3. **Web interface doesn't load**: Check if antivirus is blocking the application

### System Requirements for End Users

- Windows 10 or newer
- 4GB RAM minimum
- 100MB disk space
- Modern web browser installed

## File Structure After Build

```
dist/
└── ClothingStoreInventory/
    ├── ClothingStoreInventory.exe    # Main executable
    ├── web/                          # Web interface files
    │   ├── index.html
    │   ├── css/
    │   └── js/
    ├── README.md                     # Documentation
    ├── USER_MANUAL.md               # User guide
    └── start_exe.bat                # Optional startup script
```

## Notes

- The executable is self-contained and includes all Python dependencies
- No Python installation required on target machines
- Database is created automatically on first run
- Sample data can be added using the included script
