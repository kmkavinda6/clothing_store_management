// Clothing Store Inventory Management - Frontend JavaScript

let currentUser = null;
let styles = [];
let racks = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkLoginStatus();
    setupEventListeners();
});

// Check if user is logged in
async function checkLoginStatus() {
    try {
        currentUser = await eel.get_current_user()();
        if (currentUser) {
            showMainContent();
            updateUserInterface();
            loadDashboardData();
        } else {
            showLoginModal();
        }
    } catch (error) {
        console.error('Error checking login status:', error);
        showLoginModal();
    }
}

// Setup event listeners
function setupEventListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Style form
    document.getElementById('styleForm').addEventListener('submit', handleAddStyle);
    
    // Inventory form
    document.getElementById('inventoryForm').addEventListener('submit', handleAddInventory);
    
    // Search form
    document.getElementById('searchForm').addEventListener('submit', handleSearch);
    
    // Tab change events
    document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(event) {
            const tabId = event.target.getAttribute('data-bs-target');
            handleTabChange(tabId);
        });
    });
}

// Handle login
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const result = await eel.login(username, password)();
        
        if (result.success) {
            currentUser = result.user;
            hideLoginModal();
            showMainContent();
            updateUserInterface();
            loadDashboardData();
            showAlert('Login successful!', 'success');
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('Login failed. Please try again.', 'danger');
    }
}

// Handle logout
async function logout() {
    try {
        await eel.logout()();
        currentUser = null;
        hideMainContent();
        showLoginModal();
        showAlert('Logged out successfully', 'info');
    } catch (error) {
        console.error('Logout error:', error);
    }
}

// Show/hide UI elements
function showLoginModal() {
    const modal = new bootstrap.Modal(document.getElementById('loginModal'));
    modal.show();
}

function hideLoginModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
    if (modal) modal.hide();
}

function showMainContent() {
    document.getElementById('mainContent').style.display = 'block';
}

function hideMainContent() {
    document.getElementById('mainContent').style.display = 'none';
}

// Update user interface based on role
function updateUserInterface() {
    if (!currentUser) return;
    
    document.getElementById('currentUser').textContent = `${currentUser.username} (${currentUser.role})`;
    
    // Show/hide tabs based on role
    const styleManagementTab = document.getElementById('styleManagementTab');
    if (currentUser.role === 'Store Manager') {
        styleManagementTab.style.display = 'block';
    } else {
        styleManagementTab.style.display = 'none';
    }
}

// Load dashboard data
async function loadDashboardData() {
    try {
        const stats = await eel.get_dashboard_stats()();
        
        document.getElementById('totalStyles').textContent = stats.total_styles;
        document.getElementById('totalItems').textContent = stats.total_items;
        document.getElementById('totalRacks').textContent = stats.total_racks;
        document.getElementById('lowStockItems').textContent = stats.low_stock_items;
        document.getElementById('avgUtilization').textContent = `${stats.avg_utilization}%`;
        
        // Load recent transactions
        const transactionsTable = document.getElementById('recentTransactions');
        transactionsTable.innerHTML = '';
        
        stats.recent_transactions.forEach(transaction => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><span class="badge bg-primary">${transaction.type}</span></td>
                <td>${transaction.details}</td>
                <td>${transaction.user}</td>
                <td>${formatDateTime(transaction.timestamp)}</td>
            `;
            transactionsTable.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showAlert('Error loading dashboard data', 'danger');
    }
}

// Load styles data
async function loadStyles() {
    try {
        styles = await eel.get_styles()();
        
        // Update styles table
        const stylesTable = document.getElementById('stylesTable');
        stylesTable.innerHTML = '';
        
        styles.forEach(style => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${style.style_number}</td>
                <td>${style.style_name}</td>
                <td><span class="badge bg-info">${style.category}</span></td>
                <td>${style.vendor || '-'}</td>
                <td>${style.available_sizes.join(', ')}</td>
                <td>${style.available_colors.join(', ')}</td>
            `;
            stylesTable.appendChild(row);
        });
        
        // Update inventory style dropdown
        const inventoryStyleSelect = document.getElementById('inventoryStyle');
        inventoryStyleSelect.innerHTML = '<option value="">Select Style</option>';
        styles.forEach(style => {
            const option = document.createElement('option');
            option.value = style.id;
            option.textContent = `${style.style_number} - ${style.style_name}`;
            inventoryStyleSelect.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading styles:', error);
        showAlert('Error loading styles', 'danger');
    }
}

// Load racks data
async function loadRacks() {
    try {
        racks = await eel.get_racks()();
        
        // Update racks grid
        const racksGrid = document.getElementById('racksGrid');
        racksGrid.innerHTML = '';
        
        racks.forEach(rack => {
            const utilizationClass = getUtilizationClass(rack.utilization_percent);
            
            const rackCard = document.createElement('div');
            rackCard.className = 'col-md-3 col-sm-6';
            rackCard.innerHTML = `
                <div class="card rack-card">
                    <div class="card-body">
                        <h6 class="card-title">${rack.rack_id}</h6>
                        <p class="card-text small text-muted">${rack.location}</p>
                        <div class="d-flex justify-content-between">
                            <small>Capacity:</small>
                            <small>${rack.current_utilization}/${rack.capacity}</small>
                        </div>
                        <div class="utilization-bar">
                            <div class="utilization-fill ${utilizationClass}" 
                                 style="width: ${rack.utilization_percent}%"></div>
                        </div>
                        <div class="text-center mt-2">
                            <small class="text-muted">${rack.utilization_percent}% utilized</small>
                        </div>
                    </div>
                </div>
            `;
            racksGrid.appendChild(rackCard);
        });
        
        // Update inventory rack dropdown
        const inventoryRackSelect = document.getElementById('inventoryRack');
        inventoryRackSelect.innerHTML = '<option value="">Select Rack</option>';
        racks.forEach(rack => {
            const option = document.createElement('option');
            option.value = rack.id;
            option.textContent = `${rack.rack_id} (${rack.capacity - rack.current_utilization} available)`;
            inventoryRackSelect.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading racks:', error);
        showAlert('Error loading racks', 'danger');
    }
}

// Handle tab changes
function handleTabChange(tabId) {
    switch (tabId) {
        case '#dashboard':
            loadDashboardData();
            break;
        case '#styles':
            loadStyles();
            break;
        case '#inventory':
            loadStyles();
            loadRacks();
            break;
        case '#search':
            // Search tab doesn't need initial loading
            break;
        case '#racks':
            loadRacks();
            break;
    }
}

// Handle add style
async function handleAddStyle(event) {
    event.preventDefault();
    
    if (currentUser.role !== 'Store Manager') {
        showAlert('Only Store Managers can add styles', 'warning');
        return;
    }
    
    const styleData = {
        style_number: document.getElementById('styleNumber').value,
        style_name: document.getElementById('styleName').value,
        category: document.getElementById('category').value,
        vendor: document.getElementById('vendor').value,
        description: document.getElementById('description').value,
        available_sizes: document.getElementById('availableSizes').value.split(',').map(s => s.trim()).filter(s => s),
        available_colors: document.getElementById('availableColors').value.split(',').map(s => s.trim()).filter(s => s)
    };
    
    try {
        const result = await eel.add_style(styleData)();
        
        if (result.success) {
            showAlert('Style added successfully!', 'success');
            document.getElementById('styleForm').reset();
            loadStyles();
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        console.error('Error adding style:', error);
        showAlert('Error adding style', 'danger');
    }
}

// Handle add inventory
async function handleAddInventory(event) {
    event.preventDefault();
    
    const inventoryData = {
        style_id: parseInt(document.getElementById('inventoryStyle').value),
        size: document.getElementById('inventorySize').value,
        color: document.getElementById('inventoryColor').value,
        quantity: parseInt(document.getElementById('inventoryQuantity').value),
        rack_id: parseInt(document.getElementById('inventoryRack').value)
    };
    
    try {
        const result = await eel.add_inventory(inventoryData)();
        
        if (result.success) {
            showAlert('Inventory added successfully!', 'success');
            document.getElementById('inventoryForm').reset();
            loadRacks(); // Refresh rack utilization
            loadDashboardData(); // Refresh dashboard stats
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        console.error('Error adding inventory:', error);
        showAlert('Error adding inventory', 'danger');
    }
}

// Suggest optimal rack
async function suggestOptimalRack() {
    const styleId = document.getElementById('inventoryStyle').value;
    const quantity = document.getElementById('inventoryQuantity').value;
    
    if (!styleId || !quantity) {
        showAlert('Please select a style and enter quantity first', 'warning');
        return;
    }
    
    try {
        const result = await eel.get_optimal_rack(parseInt(styleId), parseInt(quantity))();
        
        if (result.success) {
            document.getElementById('inventoryRack').value = result.rack.id;
            showAlert(`Suggested rack: ${result.rack.rack_id} (${result.rack.available_space} available)`, 'info');
        } else {
            showAlert(result.message, 'warning');
        }
    } catch (error) {
        console.error('Error getting optimal rack:', error);
        showAlert('Error getting rack suggestion', 'danger');
    }
}

// Handle search
async function handleSearch(event) {
    event.preventDefault();
    
    const searchParams = {
        style_number: document.getElementById('searchStyleNumber').value,
        color: document.getElementById('searchColor').value,
        size: document.getElementById('searchSize').value
    };
    
    try {
        const results = await eel.search_inventory(searchParams)();
        
        const resultsTable = document.getElementById('searchResults');
        resultsTable.innerHTML = '';
        
        if (results.length === 0) {
            resultsTable.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No items found</td></tr>';
            return;
        }
        
        results.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.style_number}</td>
                <td>${item.style_name}</td>
                <td><span class="badge bg-secondary">${item.size}</span></td>
                <td><span class="badge bg-info">${item.color}</span></td>
                <td><span class="badge ${item.quantity < 5 ? 'bg-warning' : 'bg-success'}">${item.quantity}</span></td>
                <td><strong>${item.rack_id}</strong></td>
                <td class="small">${item.rack_location}</td>
            `;
            resultsTable.appendChild(row);
        });
        
        showAlert(`Found ${results.length} items`, 'success');
        
    } catch (error) {
        console.error('Error searching inventory:', error);
        showAlert('Error searching inventory', 'danger');
    }
}

// Utility functions
function getUtilizationClass(percent) {
    if (percent < 50) return 'utilization-low';
    if (percent < 80) return 'utilization-medium';
    return 'utilization-high';
}

function formatDateTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Additional utility functions for enhanced functionality
function clearForm(formId) {
    document.getElementById(formId).reset();
}

function toggleLoading(elementId, show) {
    const element = document.getElementById(elementId);
    if (show) {
        element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        element.disabled = true;
    } else {
        element.innerHTML = element.getAttribute('data-original-text') || 'Submit';
        element.disabled = false;
    }
}

// Initialize tooltips and popovers if needed
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Export functions for testing if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatDateTime,
        getUtilizationClass,
        showAlert
    };
}
