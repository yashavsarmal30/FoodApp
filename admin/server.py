from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs, urlparse
from decimal import Decimal
from .auth import admin_auth
from .db_service import admin_db

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

class AdminHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        # Check authentication for all routes except login
        if not path.endswith('/login') and not self.is_authenticated():
            self.redirect_to_login()
            return

        # Serve static files
        if path.startswith('/static/'):
            self.serve_static_file(path)
            return

        # API endpoints
        if path == '/admin/api/stats':
            self.serve_api_stats()
        elif path == '/admin/api/users':
            self.serve_api_users(query)
        elif path.startswith('/admin/api/restaurants'):
            restaurant_id = path.split('/')[-1] if path.count('/') > 3 else None
            self.serve_api_restaurants(restaurant_id)
        elif path.startswith('/admin/api/menu'):
            if path.count('/') > 3:
                menu_id = path.split('/')[-1]
                self.serve_menu_item(menu_id)
            elif 'restaurant_id' in query:
                self.serve_restaurant_menu(query['restaurant_id'][0])
            else:
                self.serve_api_menu()
        elif path == '/admin/api/orders':
            self.serve_api_orders()
        elif path == '/admin/api/payments':
            self.serve_api_payments()
        elif path == '/admin/api/reviews':
            self.serve_api_reviews()
        # HTML pages
        elif path == '/admin/login':
            self.serve_login_page()
        elif path == '/admin/dashboard':
            self.serve_dashboard()
        elif path in ['/admin/users', '/admin/restaurants', '/admin/menu-items', 
                     '/admin/orders', '/admin/payments', '/admin/reviews', '/admin/settings']:
            self.serve_page(path)
        elif path == '/admin/api/dashboard/stats':
            self.serve_api_dashboard_stats()
        elif path == '/admin/api/dashboard/revenue-chart':
            self.serve_api_dashboard_revenue_chart()
        elif path == '/admin/api/dashboard/order-status':
            self.serve_api_dashboard_order_status()
        elif path == '/admin/api/dashboard/popular-categories':
            self.serve_api_dashboard_popular_categories()
        elif path == '/admin/api/dashboard/recent-orders':
            self.serve_api_dashboard_recent_orders()
        elif path == '/admin/api/dashboard/recent-reviews':
            self.serve_api_dashboard_recent_reviews()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/admin/login':
            self.handle_login()
        elif self.path == '/admin/api/restaurants':
            self.handle_add_restaurant()
        elif self.path == '/admin/api/menu':
            self.handle_add_menu_item()
        else:
            self.send_error(404)

    def do_PUT(self):
        if not self.is_authenticated():
            self.send_error(401)
            return

        if self.path.startswith('/admin/api/restaurants/'):
            restaurant_id = self.path.split('/')[-1]
            self.handle_update_restaurant(restaurant_id)
        elif self.path.startswith('/admin/api/menu/'):
            menu_id = self.path.split('/')[-1]
            self.handle_update_menu_item(menu_id)
        else:
            self.send_error(404)

    def do_DELETE(self):
        if not self.is_authenticated():
            self.send_error(401)
            return

        if self.path.startswith('/admin/api/restaurants/'):
            restaurant_id = self.path.split('/')[-1]
            self.handle_delete_restaurant(restaurant_id)
        elif self.path.startswith('/admin/api/menu/'):
            menu_id = self.path.split('/')[-1]
            self.handle_delete_menu_item(menu_id)
        elif self.path.startswith('/admin/api/users/'):
            user_id = self.path.split('/')[-1]
            self.handle_delete_user(user_id)
        else:
            self.send_error(404)

    def handle_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        if admin_auth.authenticate(data['username'], data['password']):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        else:
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False}).encode())

    def serve_api_stats(self):
        stats = admin_db.get_dashboard_stats()
        self.send_json_response(stats)

    def serve_api_users(self, query):
        role = query.get('role', [None])[0]
        users = admin_db.get_users(role=role)
        self.send_json_response(users)

    def serve_api_restaurants(self, restaurant_id=None):
        if restaurant_id:
            restaurant = admin_db.get_restaurant(restaurant_id)
            if restaurant:
                self.send_json_response(restaurant)
            else:
                self.send_error(404)
        else:
            restaurants = admin_db.get_table_data('restaurants')
            self.send_json_response(restaurants)

    def handle_add_restaurant(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        restaurant_data = json.loads(post_data.decode('utf-8'))
        
        success = admin_db.add_restaurant(restaurant_data)
        if success:
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        else:
            self.send_error(400)

    def handle_update_restaurant(self, restaurant_id):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        restaurant_data = json.loads(post_data.decode('utf-8'))
        
        success = admin_db.update_record('Restaurants', restaurant_id, restaurant_data)
        if success:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        else:
            self.send_error(400)

    def handle_delete_restaurant(self, restaurant_id):
        success = admin_db.delete_record('Restaurants', restaurant_id)
        if success:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        else:
            self.send_error(400)

    def serve_page(self, path):
        page_name = path.split('/')[-1]
        template_path = os.path.join(os.path.dirname(__file__), 'templates', f'{page_name}.html')
        if os.path.exists(template_path):
            with open(template_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404)

    def serve_static_file(self, path):
        try:
            file_path = os.path.join(os.path.dirname(__file__), path[1:])
            with open(file_path, 'rb') as file:
                self.send_response(200)
                if path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                elif path.endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                elif path.endswith('.jpg') or path.endswith('.jpeg'):
                    self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404)

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, cls=DecimalEncoder).encode())

    def is_authenticated(self):
        # Implement proper authentication check
        return True

    def redirect_to_login(self):
        self.send_response(302)
        self.send_header('Location', '/admin/login')
        self.end_headers()

    def serve_dashboard(self):
        """Serve the dashboard page."""
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'dashboard.html')
        if os.path.exists(template_path):
            with open(template_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404)

    def serve_login_page(self):
        """Serve the login page."""
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'login.html')
        if os.path.exists(template_path):
            with open(template_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404)

    def serve_api_menu(self):
        """Serve menu items data."""
        menu_items = admin_db.get_table_data('menu')
        self.send_json_response(menu_items)

    def serve_api_orders(self):
        """Serve orders data."""
        orders = admin_db.get_table_data('orders')
        self.send_json_response(orders)

    def serve_api_payments(self):
        """Serve payments data."""
        payments = admin_db.get_table_data('payments')
        self.send_json_response(payments)

    def serve_api_reviews(self):
        """Serve reviews data."""
        reviews = admin_db.get_table_data('reviews')
        self.send_json_response(reviews)

    def handle_add_menu_item(self):
        """Handle adding a new menu item."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        menu_data = json.loads(post_data.decode('utf-8'))
        
        menu_id = admin_db.add_menu_item(menu_data)
        if menu_id:
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'menu_id': menu_id}).encode())
        else:
            self.send_error(400)

    def handle_update_menu_item(self, menu_id):
        """Handle updating a menu item."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        menu_data = json.loads(post_data.decode('utf-8'))
        
        success = admin_db.update_menu_item(menu_id, menu_data)
        if success:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        else:
            self.send_error(400)

    def handle_delete_menu_item(self, menu_id):
        """Handle deleting a menu item."""
        success = admin_db.delete_menu_item(menu_id)
        if success:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        else:
            self.send_error(400)

    def serve_menu_item(self, menu_id):
        """Serve a specific menu item."""
        menu_item = admin_db.get_menu_item(menu_id)
        if menu_item:
            self.send_json_response(menu_item)
        else:
            self.send_error(404)

    def serve_restaurant_menu(self, restaurant_id):
        """Serve menu items for a specific restaurant."""
        menu_items = admin_db.get_menu_by_restaurant(restaurant_id)
        self.send_json_response(menu_items)

    def handle_delete_user(self, user_id):
        """Handle deleting a user."""
        success = admin_db.delete_user(user_id)
        if success:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        else:
            self.send_error(400)

    def serve_api_dashboard_stats(self):
        """Serve dashboard statistics"""
        stats = admin_db.get_dashboard_stats()
        self.send_json_response(stats)

    def serve_api_dashboard_revenue_chart(self):
        """Serve revenue chart data"""
        period = self.get_query_param('period', 'week')
        data = admin_db.get_revenue_chart_data(period)
        self.send_json_response(data)

    def serve_api_dashboard_order_status(self):
        """Serve order status distribution data"""
        data = admin_db.get_order_status_distribution()
        self.send_json_response(data)

    def serve_api_dashboard_popular_categories(self):
        """Serve popular categories data"""
        data = admin_db.get_popular_categories()
        self.send_json_response(data)

    def serve_api_dashboard_recent_orders(self):
        """Serve recent orders data"""
        limit = 5  # Number of recent orders to return
        orders = admin_db.get_recent_orders(limit)
        self.send_json_response(orders)

    def serve_api_dashboard_recent_reviews(self):
        """Serve recent reviews data"""
        limit = 5  # Number of recent reviews to return
        reviews = admin_db.get_recent_reviews(limit)
        self.send_json_response(reviews)

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AdminHandler)
    print(f'Admin server running on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 