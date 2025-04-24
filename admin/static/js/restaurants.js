document.addEventListener('DOMContentLoaded', function() {
    loadRestaurants();
    loadOwners();
    
    // Add event listeners
    document.getElementById('restaurantForm').addEventListener('submit', handleAddRestaurant);
    document.getElementById('editRestaurantForm').addEventListener('submit', handleEditRestaurant);
});

async function loadRestaurants() {
    try {
        const response = await fetch('/admin/api/restaurants');
        const restaurants = await response.json();
        const tbody = document.querySelector('#restaurants-table tbody');
        tbody.innerHTML = '';

        restaurants.forEach(restaurant => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${restaurant.id}</td>
                <td>${restaurant.name}</td>
                <td>${restaurant.restaurant_type}</td>
                <td>${restaurant.location}</td>
                <td>${restaurant.rating ? restaurant.rating.toFixed(1) : 'N/A'}</td>
                <td>
                    <span class="status ${restaurant.is_active ? 'active' : 'inactive'}">
                        ${restaurant.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>
                    <button class="btn-view" onclick="viewRestaurant(${restaurant.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn-edit" onclick="showEditRestaurantModal(${restaurant.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" onclick="deleteRestaurant(${restaurant.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error loading restaurants:', error);
        alert('Error loading restaurants');
    }
}

async function loadOwners() {
    try {
        const response = await fetch('/admin/api/users?role=owner');
        const owners = await response.json();
        const ownerSelect = document.getElementById('owner');
        ownerSelect.innerHTML = '<option value="">Select Owner</option>';

        owners.forEach(owner => {
            const option = document.createElement('option');
            option.value = owner.user_id;
            option.textContent = owner.name;
            ownerSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading owners:', error);
    }
}

function showAddRestaurantForm() {
    document.getElementById('add-restaurant-form').style.display = 'block';
}

function hideAddRestaurantForm() {
    document.getElementById('add-restaurant-form').style.display = 'none';
    document.getElementById('restaurantForm').reset();
}

async function handleAddRestaurant(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const restaurantData = Object.fromEntries(formData);

    try {
        const response = await fetch('/admin/api/restaurants', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(restaurantData)
        });

        if (response.ok) {
            alert('Restaurant added successfully!');
            hideAddRestaurantForm();
            loadRestaurants();
        } else {
            alert('Failed to add restaurant');
        }
    } catch (error) {
        console.error('Error adding restaurant:', error);
        alert('Error adding restaurant');
    }
}

async function showEditRestaurantModal(restaurantId) {
    try {
        const response = await fetch(`/admin/api/restaurants/${restaurantId}`);
        const restaurant = await response.json();

        // Populate form fields
        document.getElementById('edit-id').value = restaurant.id;
        document.getElementById('edit-name').value = restaurant.name;
        document.getElementById('edit-type').value = restaurant.restaurant_type;
        document.getElementById('edit-location').value = restaurant.location;
        document.getElementById('edit-contact').value = restaurant.contact_number;
        document.getElementById('edit-description').value = restaurant.description;
        document.getElementById('edit-status').value = restaurant.is_active.toString();

        // Show modal
        document.getElementById('edit-restaurant-modal').style.display = 'block';
    } catch (error) {
        console.error('Error loading restaurant details:', error);
        alert('Error loading restaurant details');
    }
}

function hideEditRestaurantModal() {
    document.getElementById('edit-restaurant-modal').style.display = 'none';
    document.getElementById('editRestaurantForm').reset();
}

async function handleEditRestaurant(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const restaurantData = Object.fromEntries(formData);
    const restaurantId = restaurantData.id;
    delete restaurantData.id;

    try {
        const response = await fetch(`/admin/api/restaurants/${restaurantId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(restaurantData)
        });

        if (response.ok) {
            alert('Restaurant updated successfully!');
            hideEditRestaurantModal();
            loadRestaurants();
        } else {
            alert('Failed to update restaurant');
        }
    } catch (error) {
        console.error('Error updating restaurant:', error);
        alert('Error updating restaurant');
    }
}

function viewRestaurant(restaurantId) {
    window.location.href = `/admin/restaurants/${restaurantId}`;
}

async function deleteRestaurant(restaurantId) {
    if (!confirm('Are you sure you want to delete this restaurant?')) {
        return;
    }

    try {
        const response = await fetch(`/admin/api/restaurants/${restaurantId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Restaurant deleted successfully!');
            loadRestaurants();
        } else {
            alert('Failed to delete restaurant');
        }
    } catch (error) {
        console.error('Error deleting restaurant:', error);
        alert('Error deleting restaurant');
    }
} 