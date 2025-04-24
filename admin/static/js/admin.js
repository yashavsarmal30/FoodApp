// Dashboard Statistics
document.addEventListener('DOMContentLoaded', function() {
    // Load dashboard stats
    fetchDashboardStats();
    
    // Load recent orders and top restaurants if on dashboard
    if (window.location.pathname === '/admin/dashboard') {
        fetchRecentOrders();
        fetchTopRestaurants();
    }

    // Add event listeners for sidebar navigation
    document.querySelectorAll('.sidebar a').forEach(link => {
        link.addEventListener('click', function(e) {
            document.querySelector('.sidebar a.active')?.classList.remove('active');
            this.classList.add('active');
        });
    });

    // Logout functionality
    document.getElementById('logout')?.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
            window.location.href = '/admin/login';
        }
    });
});

async function fetchDashboardStats() {
    try {
        const response = await fetch('/admin/api/stats');
        const stats = await response.json();
        
        // Update dashboard stats
        document.getElementById('total-users').textContent = stats.total_users;
        document.getElementById('total-restaurants').textContent = stats.total_restaurants;
        document.getElementById('total-orders').textContent = stats.total_orders;
        document.getElementById('total-revenue').textContent = `₹${stats.total_revenue.toFixed(2)}`;
    } catch (error) {
        console.error('Error fetching dashboard stats:', error);
    }
}

async function fetchRecentOrders() {
    try {
        const response = await fetch('/admin/api/orders');
        const orders = await response.json();
        const tbody = document.querySelector('#recent-orders-table tbody');
        tbody.innerHTML = '';

        orders.slice(0, 10).forEach(order => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${order.id}</td>
                <td>${order.customer_name}</td>
                <td>${order.restaurant_name}</td>
                <td>₹${order.total_price.toFixed(2)}</td>
                <td><span class="status ${order.status.toLowerCase()}">${order.status}</span></td>
                <td>
                    <button class="btn-view" onclick="viewOrder(${order.id})">View</button>
                    <button class="btn-update" onclick="updateOrderStatus(${order.id})">Update</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error fetching recent orders:', error);
    }
}

async function fetchTopRestaurants() {
    try {
        const response = await fetch('/admin/api/restaurants');
        const restaurants = await response.json();
        const tbody = document.querySelector('#top-restaurants-table tbody');
        tbody.innerHTML = '';

        restaurants.slice(0, 5).forEach(restaurant => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${restaurant.name}</td>
                <td>${restaurant.total_orders || 0}</td>
                <td>${restaurant.rating ? restaurant.rating.toFixed(1) : 'N/A'}</td>
                <td>₹${restaurant.revenue ? restaurant.revenue.toFixed(2) : '0.00'}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error fetching top restaurants:', error);
    }
}

function viewOrder(orderId) {
    window.location.href = `/admin/orders/${orderId}`;
}

async function updateOrderStatus(orderId) {
    const newStatus = prompt('Enter new status (pending/processing/completed/cancelled):');
    if (!newStatus) return;

    try {
        const response = await fetch(`/admin/api/orders/${orderId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus })
        });

        if (response.ok) {
            alert('Order status updated successfully!');
            fetchRecentOrders(); // Refresh the orders table
        } else {
            alert('Failed to update order status');
        }
    } catch (error) {
        console.error('Error updating order status:', error);
        alert('Error updating order status');
    }
}

// Add restaurant form handling
document.getElementById('add-restaurant-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    try {
        const response = await fetch('/admin/api/restaurants', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(Object.fromEntries(formData))
        });

        if (response.ok) {
            alert('Restaurant added successfully!');
            this.reset();
            window.location.reload();
        } else {
            alert('Failed to add restaurant');
        }
    } catch (error) {
        console.error('Error adding restaurant:', error);
        alert('Error adding restaurant');
    }
});

// Add menu item form handling
document.getElementById('add-menu-item-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    try {
        const response = await fetch('/admin/api/menu', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(Object.fromEntries(formData))
        });

        if (response.ok) {
            alert('Menu item added successfully!');
            this.reset();
            window.location.reload();
        } else {
            alert('Failed to add menu item');
        }
    } catch (error) {
        console.error('Error adding menu item:', error);
        alert('Error adding menu item');
    }
});

// Form Validation
document.getElementById('loginForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        alert('Please fill in all fields');
        return;
    }

    fetch('/admin/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/admin/dashboard';
        } else {
            alert('Invalid credentials');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during login');
    });
});

// Image Upload
function handleImageUpload(input, previewId) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(previewId).src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}

// Table Management
function createDataTable(tableId) {
    const table = document.getElementById(tableId);
    if (table) {
        // Add sorting functionality
        const headers = table.querySelectorAll('th');
        headers.forEach(header => {
            header.addEventListener('click', () => {
                const column = header.cellIndex;
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                const direction = header.classList.contains('asc') ? -1 : 1;
                
                rows.sort((a, b) => {
                    const aValue = a.cells[column].textContent;
                    const bValue = b.cells[column].textContent;
                    return direction * (aValue > bValue ? 1 : -1);
                });

                const tbody = table.querySelector('tbody');
                rows.forEach(row => tbody.appendChild(row));
                
                headers.forEach(h => h.classList.remove('asc', 'desc'));
                header.classList.add(direction === 1 ? 'asc' : 'desc');
            });
        });
    }
}

// Initialize all tables
document.querySelectorAll('table').forEach(table => {
    createDataTable(table.id);
}); 