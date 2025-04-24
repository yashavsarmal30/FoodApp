import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal
import os

class AdminDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='neondb',
            user='neondb_owner',
            password='npg_wcL9F4Efrovk',
            host='ep-small-pine-a5sxxb5h-pooler.us-east-2.aws.neon.tech',
            port=5432,
            sslmode='require'
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def close(self):
        if self.conn:
            self.conn.close()

    def get_dashboard_stats(self):
        """Get overall dashboard statistics"""
        with self.conn:
            cursor = self.conn.cursor()
            
            # Get total users
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            # Get total restaurants
            cursor.execute("SELECT COUNT(*) FROM restaurants")
            total_restaurants = cursor.fetchone()[0]
            
            # Get active orders
            cursor.execute("SELECT COUNT(*) FROM orders WHERE status IN ('pending', 'processing', 'out_for_delivery')")
            active_orders = cursor.fetchone()[0]
            
            # Get total revenue
            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status = 'delivered'")
            total_revenue = float(cursor.fetchone()[0])
            
            return {
                "total_users": total_users,
                "total_restaurants": total_restaurants,
                "active_orders": active_orders,
                "total_revenue": total_revenue
            }

    def get_revenue_chart_data(self, period='week'):
        """Get revenue data for the chart"""
        with self.conn:
            cursor = self.conn.cursor()
            
            if period == 'week':
                days = 7
                group_format = '%Y-%m-%d'
            elif period == 'month':
                days = 30
                group_format = '%Y-%m-%d'
            else:  # year
                days = 365
                group_format = '%Y-%m'

            cursor.execute("""
                SELECT strftime(?, date(order_time)) as date,
                       COALESCE(SUM(total_amount), 0) as revenue
                FROM orders
                WHERE status = 'delivered'
                AND order_time >= date('now', ?)
                GROUP BY date
                ORDER BY date
            """, (group_format, f'-{days} days'))
            
            rows = cursor.fetchall()
            return {
                "labels": [row[0] for row in rows],
                "values": [float(row[1]) for row in rows]
            }

    def get_order_status_distribution(self):
        """Get distribution of orders by status"""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM orders
                GROUP BY status
            """)
            rows = cursor.fetchall()
            statuses = ['pending', 'processing', 'out_for_delivery', 'delivered', 'cancelled']
            counts = {status: 0 for status in statuses}
            for status, count in rows:
                if status in counts:
                    counts[status] = count
            return {"values": list(counts.values())}

    def get_popular_categories(self):
        """Get most popular food categories"""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT category, COUNT(*) as order_count
                FROM order_items oi
                JOIN menu_items mi ON oi.menu_item_id = mi.id
                GROUP BY category
                ORDER BY order_count DESC
                LIMIT 5
            """)
            rows = cursor.fetchall()
            return {
                "labels": [row[0] for row in rows],
                "values": [row[1] for row in rows]
            }

    def get_recent_orders(self, limit=5):
        """Get recent orders with details"""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT o.id as order_id, 
                       u.name as customer_name,
                       r.name as restaurant_name,
                       o.total_amount,
                       o.status,
                       o.order_time
                FROM orders o
                JOIN users u ON o.user_id = u.id
                JOIN restaurants r ON o.restaurant_id = r.id
                ORDER BY o.order_time DESC
                LIMIT ?
            """, (limit,))
            
            columns = ['order_id', 'customer_name', 'restaurant_name', 'total', 'status', 'time']
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_recent_reviews(self, limit=5):
        """Get recent reviews with details"""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT u.name as customer_name,
                       r.name as restaurant_name,
                       rv.rating,
                       rv.review_text as text,
                       rv.review_date as time
                FROM reviews rv
                JOIN users u ON rv.user_id = u.id
                JOIN restaurants r ON rv.restaurant_id = r.id
                ORDER BY rv.review_date DESC
                LIMIT ?
            """, (limit,))
            
            columns = ['customer_name', 'restaurant_name', 'rating', 'text', 'time']
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_users(self, role=None):
        try:
            if role:
                self.cursor.execute("""
                    SELECT user_id, name, username, email, phone_number, is_admin
                    FROM Users
                    WHERE is_admin = %s
                    ORDER BY user_id DESC
                """, (role == 'owner',))
            else:
                self.cursor.execute("""
                    SELECT user_id, name, username, email, phone_number, is_admin
                    FROM Users
                    ORDER BY user_id DESC
                """)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching users: {e}")
            return []

    def get_restaurant(self, restaurant_id):
        try:
            self.cursor.execute("""
                SELECT r.*, u.name as owner_name
                FROM Restaurants r
                LEFT JOIN Users u ON r.owner_user_id = u.user_id
                WHERE r.restaurant_id = %s
            """, (restaurant_id,))
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching restaurant: {e}")
            return None

    def add_restaurant(self, data):
        try:
            self.cursor.execute("""
                INSERT INTO Restaurants (
                    owner_user_id, name, restaurant_type, location,
                    contact_number, description, is_active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING restaurant_id
            """, (
                data['owner_user_id'],
                data['name'],
                data['restaurant_type'],
                data['location'],
                data['contact_number'],
                data.get('description'),
                True
            ))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error adding restaurant: {e}")
            self.conn.rollback()
            return False

    def get_table_data(self, table_name):
        try:
            if table_name == 'restaurants':
                self.cursor.execute("""
                    SELECT r.restaurant_id as id, r.name, r.restaurant_type,
                           r.location, r.rating, r.is_active, r.contact_number,
                           r.description, u.name as owner_name,
                           COUNT(o.order_id) as total_orders,
                           COALESCE(SUM(o.total_price), 0) as revenue
                    FROM Restaurants r
                    LEFT JOIN Users u ON r.owner_user_id = u.user_id
                    LEFT JOIN Orders o ON r.restaurant_id = o.restaurant_id
                    GROUP BY r.restaurant_id, r.name, r.restaurant_type,
                             r.location, r.rating, r.is_active,
                             r.contact_number, r.description, u.name
                    ORDER BY r.restaurant_id DESC
                """)
            elif table_name == 'menu':
                self.cursor.execute("""
                    SELECT m.menu_id as id, m.name, m.description,
                           m.price, m.is_available, m.category,
                           r.name as restaurant_name
                    FROM Menu m
                    JOIN Restaurants r ON m.restaurant_id = r.restaurant_id
                    ORDER BY m.menu_id DESC
                """)
            elif table_name == 'orders':
                self.cursor.execute("""
                    SELECT o.order_id as id, u.name as customer_name,
                           r.name as restaurant_name, o.total_price,
                           o.status, o.order_time, o.delivery_time
                    FROM Orders o
                    JOIN Users u ON o.user_id = u.user_id
                    JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
                    ORDER BY o.order_time DESC
                """)
            elif table_name == 'payments':
                self.cursor.execute("""
                    SELECT p.payment_id as id, o.order_id,
                           p.payment_type, p.transaction_id,
                           p.payment_status, p.amount_paid,
                           p.payment_date
                    FROM Payments p
                    JOIN Orders o ON p.order_id = o.order_id
                    ORDER BY p.payment_date DESC
                """)
            elif table_name == 'reviews':
                self.cursor.execute("""
                    SELECT review_id as id, u.name as user_name,
                           r.name as restaurant_name, rating,
                           comment, review_date
                    FROM Reviews rv
                    JOIN Users u ON rv.user_id = u.user_id
                    JOIN Restaurants r ON rv.restaurant_id = r.restaurant_id
                    ORDER BY review_date DESC
                """)
            else:
                self.cursor.execute(f"SELECT * FROM {table_name}")
            
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching data from {table_name}: {e}")
            return []

    def _get_count(self, table_name):
        try:
            self.cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            result = self.cursor.fetchone()
            return result['count'] if result else 0
        except psycopg2.Error as e:
            print(f"Error getting count from {table_name}: {e}")
            return 0

    def _get_total_revenue(self):
        try:
            self.cursor.execute("""
                SELECT COALESCE(SUM(amount_paid), 0) as total
                FROM Payments
                WHERE payment_status = 'successful'
            """)
            result = self.cursor.fetchone()
            return float(result['total']) if result['total'] else 0.0
        except psycopg2.Error as e:
            print(f"Error getting total revenue: {e}")
            return 0.0

    def _get_active_orders(self):
        try:
            self.cursor.execute("""
                SELECT COUNT(*) as count
                FROM Orders
                WHERE status IN ('pending', 'processing', 'out_for_delivery')
            """)
            result = self.cursor.fetchone()
            return result['count'] if result else 0
        except psycopg2.Error as e:
            print(f"Error getting active orders: {e}")
            return 0

    def _get_pending_reviews(self):
        try:
            self.cursor.execute("""
                SELECT COUNT(*) as count
                FROM Reviews
                WHERE review_date >= NOW() - INTERVAL '24 hours'
            """)
            result = self.cursor.fetchone()
            return result['count'] if result else 0
        except psycopg2.Error as e:
            print(f"Error getting pending reviews: {e}")
            return 0

    def update_record(self, table_name, record_id, data):
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            id_column = f"{table_name.lower()[:-1]}_id"
            query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
            values = list(data.values()) + [record_id]
            
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error updating record in {table_name}: {e}")
            self.conn.rollback()
            return False

    def delete_record(self, table_name, record_id):
        try:
            id_column = f"{table_name.lower()[:-1]}_id"
            self.cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (record_id,))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error deleting record from {table_name}: {e}")
            self.conn.rollback()
            return False

    def get_top_restaurants(self):
        try:
            self.cursor.execute("""
                SELECT r.name, COUNT(o.order_id) as total_orders,
                       r.rating, SUM(o.total_price) as revenue
                FROM Restaurants r
                LEFT JOIN Orders o ON r.restaurant_id = o.restaurant_id
                GROUP BY r.restaurant_id, r.name
                ORDER BY revenue DESC NULLS LAST
                LIMIT 5
            """)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error getting top restaurants: {e}")
            return []

    def add_menu_item(self, data):
        """Add a new menu item."""
        try:
            self.cursor.execute("""
                INSERT INTO Menu (restaurant_id, name, description, price, is_available, category)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING menu_id
            """, (
                data['restaurant_id'],
                data['name'],
                data.get('description'),
                data['price'],
                data.get('is_available', True),
                data['category']
            ))
            self.conn.commit()
            result = self.cursor.fetchone()
            return result['menu_id'] if result else None
        except psycopg2.Error as e:
            print(f"Error adding menu item: {e}")
            self.conn.rollback()
            return None

    def update_menu_item(self, menu_id, data):
        """Update an existing menu item."""
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            values = list(data.values()) + [menu_id]
            
            self.cursor.execute(f"""
                UPDATE Menu 
                SET {set_clause}
                WHERE menu_id = %s
                RETURNING menu_id
            """, values)
            
            self.conn.commit()
            result = self.cursor.fetchone()
            return result['menu_id'] if result else None
        except psycopg2.Error as e:
            print(f"Error updating menu item: {e}")
            self.conn.rollback()
            return None

    def delete_menu_item(self, menu_id):
        """Delete a menu item."""
        try:
            self.cursor.execute("DELETE FROM Menu WHERE menu_id = %s", (menu_id,))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error deleting menu item: {e}")
            self.conn.rollback()
            return False

    def get_menu_item(self, menu_id):
        """Get a specific menu item."""
        try:
            self.cursor.execute("""
                SELECT m.*, r.name as restaurant_name
                FROM Menu m
                JOIN Restaurants r ON m.restaurant_id = r.restaurant_id
                WHERE m.menu_id = %s
            """, (menu_id,))
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching menu item: {e}")
            return None

    def get_menu_by_restaurant(self, restaurant_id):
        """Get all menu items for a specific restaurant."""
        try:
            self.cursor.execute("""
                SELECT * FROM Menu
                WHERE restaurant_id = %s
                ORDER BY category, name
            """, (restaurant_id,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching restaurant menu: {e}")
            return []

    def get_all_users(self, role=None):
        """Get all users with optional role filter."""
        try:
            if role:
                self.cursor.execute("""
                    SELECT user_id, name, username, email, phone_number, 
                           gender, dob, is_admin, govt_id
                    FROM Users
                    WHERE is_admin = %s
                    ORDER BY user_id DESC
                """, (role == 'admin',))
            else:
                self.cursor.execute("""
                    SELECT user_id, name, username, email, phone_number, 
                           gender, dob, is_admin, govt_id
                    FROM Users
                    ORDER BY user_id DESC
                """)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching users: {e}")
            return []

    def delete_user(self, user_id):
        """Delete a user and all related data."""
        try:
            # Start a transaction
            self.cursor.execute("BEGIN")
            
            # Delete related records first
            self.cursor.execute("DELETE FROM Reviews WHERE user_id = %s", (user_id,))
            self.cursor.execute("DELETE FROM Orders WHERE user_id = %s", (user_id,))
            
            # Finally delete the user
            self.cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            
            # Commit the transaction
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error deleting user: {e}")
            self.conn.rollback()
            return False

    def get_user(self, user_id):
        """Get a specific user's details."""
        try:
            self.cursor.execute("""
                SELECT user_id, name, username, email, phone_number, 
                       gender, dob, is_admin, govt_id
                FROM Users
                WHERE user_id = %s
            """, (user_id,))
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching user: {e}")
            return None

# Create a singleton instance
admin_db = AdminDB() 