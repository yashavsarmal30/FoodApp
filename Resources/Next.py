from re import *
from threading import Thread
from tkinter import messagebox
from tkinter import *
from typing import Literal, Tuple, Any
from PIL import Image, ImageDraw
from customtkinter import *
from dotenv import load_dotenv
import ipapi
from Resources.Email import send_mail
from Resources.database import Database
from Resources.Notification import Send
import json
import os

load_dotenv()

set_appearance_mode("system")
set_default_color_theme("green")

class Page(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)
        self.create_back_button()

    def create_back_button(self):
        back_button = CTkButton(self,
                text="← Back",
                font=("Arial", 14),
                fg_color="transparent",
                hover_color="#e8f5e9",
                text_color="#2d6a4f",
                width=80,
                height=40,
                command=lambda: self.master.master.show_home_page())
        back_button.place(x=20, y=20)

class HomePage(Page):
    def __init__(self, master, user_data, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F5F5")
        self.user_data = user_data
        self.create_widgets()

    def create_widgets(self):
        # Remove the back button from HomePage
        for widget in self.winfo_children():
            if isinstance(widget, CTkButton) and widget.cget("text") == "← Back":
                widget.destroy()
                break

        # Header Section
        header_frame = CTkFrame(self, fg_color="transparent", height=100)
        header_frame.pack(pady=20, padx=20, fill="x")
        
        # Welcome Section
        welcome_frame = CTkFrame(header_frame, fg_color="transparent")
        welcome_frame.pack(fill="x")
        
        CTkLabel(welcome_frame, 
                text=f"👋 Welcome, {self.user_data[0][1]}!",
                font=("Arial", 24, "bold"),
                text_color="#2d6a4f").pack(side=LEFT)
        
        # Location Display
        try:
            location_text = f"📍 {ipapi.location(output='city')}, {ipapi.location(output='region')}"
        except Exception:
            location_text = "📍 Tomato Land"
            
        CTkLabel(welcome_frame,
                text=location_text,
                font=("Arial", 14),
                text_color="#666666").pack(side=RIGHT, padx=20)

        # Categories Section
        self.create_categories_section()
        
        # Featured Restaurants
        self.create_restaurants_section()

    def create_categories_section(self):
        categories_label = CTkLabel(self, 
                text="Popular Categories",
                font=("Arial", 20, "bold"),
                text_color="#2d6a4f")
        categories_label.pack(pady=(20, 5), anchor="w", padx=25)
        
        categories_frame = CTkScrollableFrame(self, orientation="horizontal", height=220)
        categories_frame.pack(pady=10, padx=20, fill="x")
        
        categories = [
            ("Pizza", "./Images/Pizza.png"),
            ("Burger", "./Images/Burger.png"),
            ("Pasta", "./Images/pasta.png"),
            ("Street Food", "./Images/panipuri.png"),
            ("Desserts", "./Images/IceCream.png"),
            ("Thali", "./Images/Thali.png"),
            ("Wraps", "./Images/Wrap.png"),
            ("Sushi", "./Images/sushi.png"),
            ("Salads", "./Images/salad.png"),
            ("BBQ", "./Images/bbq.png"),
            ("Vegan", "./Images/Vegan.png")
        ]
        
        for name, path in categories:
            card = CTkFrame(categories_frame, width=180, height=180, corner_radius=15)
            card.configure(fg_color="white")
            
            # Make the entire card clickable
            card.bind("<Button-1>", lambda e, n=name: self.master.master.show_menu_page(n))
            
            img = CTkImage(Image.open(path), size=(150, 150))
            img_label = CTkLabel(card, image=img, text="", corner_radius=10)
            img_label.pack(pady=5)
            img_label.bind("<Button-1>", lambda e, n=name: self.master.master.show_menu_page(n))
            
            name_label = CTkLabel(card, 
                    text=name,
                    font=("Arial", 12, "bold"),
                    text_color="#2d6a4f")
            name_label.pack(pady=5)
            name_label.bind("<Button-1>", lambda e, n=name: self.master.master.show_menu_page(n))
            
            card.pack(side=LEFT, padx=10)

    def create_restaurants_section(self):
        restaurants_label = CTkLabel(self, 
                text="Featured Restaurants",
                font=("Arial", 20, "bold"),
                text_color="#2d6a4f")
        restaurants_label.pack(pady=(20, 5), anchor="w", padx=25)
        
        restaurants_frame = CTkScrollableFrame(self, orientation="horizontal", height=250)
        restaurants_frame.pack(padx=20, fill="x")
        
        restaurants = [
            ("Pizza Hut", "./Images/McDoutlet.jpg", "4.2", "Italian, Fast Food"),
            ("Dominos", "./Images/dominosoutlet.jpg", "4.5", "Pizza, Italian"),
            ("Wendy's", "./Images/wendysoutlet.jpg", "4.0", "American, Fast Food"),
            ("Belgian Waffle", "./Images/belgianwaffleoutlet.jpg", "4.8", "Desserts, Cafe"),
            ("Juice Center", "./Images/juicecenteroutlet.jpg", "4.3", "Beverages, Healthy"),
            
            ("Pasta Palace", "./Images/pastaoutlet.jpg", "4.6", "Italian, Pasta"),
            ("Street Bites", "./Images/streetfoodoutlet.jpg", "4.1", "Street Food"),
            ("Sweet Tooth", "./Images/dessertsoutlet.jpg", "4.7", "Desserts"),
            ("Thali House", "./Images/thalioutlet.jpg", "4.4", "Indian, Thali"),
            ("Wrap It Up", "./Images/wrapoutlet.jpg", "4.2", "Wraps, Fast Food"),
            ("Sushi World", "./Images/sushioutlet.jpg", "4.9", "Japanese, Sushi"),
            ("Salad Stop", "./Images/saladoutlet.jpg", "4.5", "Healthy, Salads"),
            ("BBQ Nation", "./Images/bbqoutlet.jpg", "4.6", "BBQ, Grill"),
            ("Vegan Delight", "./Images/veganoutlet.jpg", "4.8", "Vegan, Healthy")
        ]
        
        for name, path, rating, cuisine in restaurants:
            card = CTkFrame(restaurants_frame, width=300, height=220, corner_radius=15)
            card.configure(fg_color="white")
            
            # Restaurant Image
            img = CTkImage(Image.open(path), size=(280, 180))
            CTkLabel(card, image=img, text="", corner_radius=10).pack(padx=10, pady=(10,0))
            
            # Restaurant Info
            info_frame = CTkFrame(card, fg_color="transparent")
            info_frame.pack(fill="x", padx=10, pady=5)
            
            CTkLabel(info_frame, 
                    text=name,
                    font=("Arial", 14, "bold"),
                    text_color="#2d6a4f").pack(side=LEFT)
            
            rating_frame = CTkFrame(info_frame, fg_color="transparent")
            rating_frame.pack(anchor="w", pady=5)
            
            CTkLabel(rating_frame,
                    text="⭐",
                    font=("Arial", 12)).pack(side=LEFT)
            
            CTkLabel(rating_frame,
                    text=rating,
                    font=("Arial", 12),
                    text_color="#666666").pack(side=LEFT, padx=5)
            
            CTkLabel(info_frame,
                    text=cuisine,
                    font=("Arial", 12),
                    text_color="#666666").pack(pady=(0,10))
            
            card.bind("<Button-1>", lambda e, n=name: self.master.master.show_restaurant_page(n))
            card.pack(side=LEFT, padx=10)

class RestaurantPage(Page):
    def __init__(self, master, restaurant_name, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F5F5")
        self.restaurant_name = restaurant_name
        self.create_widgets()

    def create_widgets(self):
        # Remove the default back button and create a custom one
        for widget in self.winfo_children():
            if isinstance(widget, CTkButton) and widget.cget("text") == "← Back":
                widget.destroy()
                break

        # Custom back button for restaurant page
        back_button = CTkButton(self,
                text="← Back to Home",
                font=("Arial", 14),
                fg_color="transparent",
                hover_color="#e8f5e9",
                text_color="#2d6a4f",
                width=120,
                height=40,
                command=self.master.master.show_home_page)
        back_button.place(x=20, y=20)
        
        # Restaurant Header
        header_frame = CTkFrame(self, fg_color="white", corner_radius=15)
        header_frame.pack(pady=10, padx=20, fill="x")
        
        # Get restaurant details from database
        results = Database.execute("""
            SELECT Restaurants.name, Restaurants.rating, Restaurants.cuisine, Restaurants.image_path
            FROM Restaurants 
            WHERE Restaurants.name = %s
        """, (self.restaurant_name,), fetch=True)
        
        if results:
            restaurant = results[0]
            
            # Restaurant Image
            img = CTkImage(Image.open(restaurant[3]), size=(200, 150))
            CTkLabel(header_frame, image=img, text="", corner_radius=10).pack(pady=10, padx=20)
            
            # Restaurant Info
            info_frame = CTkFrame(header_frame, fg_color="transparent")
            info_frame.pack(pady=10, padx=20, fill="x")
            
            CTkLabel(info_frame,
                    text=restaurant[0],
                    font=("Arial", 24, "bold"),
                    text_color="#2d6a4f").pack(anchor="w")
            
            rating_frame = CTkFrame(info_frame, fg_color="transparent")
            rating_frame.pack(anchor="w", pady=5)
            
            CTkLabel(rating_frame,
                    text="⭐",
                    font=("Arial", 14)).pack(side=LEFT)
            
            CTkLabel(rating_frame,
                    text=str(restaurant[1]),
                    font=("Arial", 14),
                    text_color="#666666").pack(side=LEFT, padx=5)
            
            CTkLabel(info_frame,
                    text=restaurant[2],
                    font=("Arial", 14),
                    text_color="#666666").pack(anchor="w")
        
        # Menu Items
        self.create_menu_items()

    def create_menu_items(self):
        # Get menu items from database
        results = Database.execute("""
            SELECT Menu.name, Menu.price, Menu.description, Menu.image_path, Menu.category
            FROM Menu 
            JOIN Restaurants ON Menu.restaurant_id = Restaurants.restaurant_id 
            WHERE Restaurants.name = %s
        """, (self.restaurant_name,), fetch=True)
        
        if results:
            # Group items by category
            categories = {}
            for item in results:
                if item[4] not in categories:
                    categories[item[4]] = []
                categories[item[4]].append(item)
            
            # Create menu items for each category
            for category, items in categories.items():
                # Category Label
                CTkLabel(self,
                        text=category,
                        font=("Arial", 20, "bold"),
                        text_color="#2d6a4f").pack(pady=(20, 5), anchor="w", padx=25)
                
                # Items Grid
                items_frame = CTkFrame(self, fg_color="transparent")
                items_frame.pack(padx=20, fill="x")
                
                for item in items:
                    self.create_menu_item(items_frame, item)
        else:
            CTkLabel(self,
                    text="No items found",
                    font=("Arial", 20),
                    text_color="#666666").pack(pady=50)

    def create_menu_item(self, parent, item):
        item_frame = CTkFrame(parent, fg_color="white", corner_radius=15)
        item_frame.pack(pady=5, padx=5, fill="x")
        
        # Item Image
        try:
            img = CTkImage(Image.open(item[3]), size=(100, 100))
        except (FileNotFoundError, AttributeError):
            # Create a placeholder image if the file doesn't exist
            placeholder = Image.new('RGB', (100, 100), color='#E8F5E9')
            draw = ImageDraw.Draw(placeholder)
            draw.text((50, 50), "No Image", fill='#2d6a4f', anchor="mm")
            img = CTkImage(placeholder, size=(100, 100))
        
        img_label = CTkLabel(item_frame, image=img, text="", corner_radius=10)
        img_label.pack(side=LEFT, padx=10, pady=10)
        img_label.bind("<Button-1>", lambda e, n=item[0]: self.master.master.show_menu_page(n))
        
        # Item Info
        info_frame = CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side=LEFT, padx=10, pady=10, fill="x", expand=True)
        
        CTkLabel(info_frame,
                text=item[0],
                font=("Arial", 16, "bold"),
                text_color="#2d6a4f").pack(anchor="w")
        
        CTkLabel(info_frame,
                text=item[2],
                font=("Arial", 14),
                text_color="#666666").pack(anchor="w")
        
        # Price and Add to Cart
        price_frame = CTkFrame(item_frame, fg_color="transparent")
        price_frame.pack(side=RIGHT, padx=10, pady=10)
        
        CTkLabel(price_frame,
                text=f"₹{item[1]}",
                font=("Arial", 16, "bold"),
                text_color="#2d6a4f").pack(side=LEFT, padx=10)
        
        CTkButton(price_frame,
                text="Add to Cart",
                font=("Arial", 14),
                width=100,
                fg_color="#2d6a4f",
                hover_color="#1b4332",
                command=lambda i=item: self.master.master.add_to_cart(i)).pack(side=LEFT)

class CartPage(Page):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F5F5")
        self.create_widgets()

    def create_widgets(self):
        # Remove default back button
        for widget in self.winfo_children():
            if isinstance(widget, CTkButton) and widget.cget("text") == "← Back":
                widget.destroy()
                break

        # Custom back button
        back_button = CTkButton(self,
                text="← Back to Home",
                font=("Arial", 14),
                fg_color="transparent",
                hover_color="#e8f5e9",
                text_color="#2d6a4f",
                width=120,
                height=40,
                command=lambda: self.master.master.show_home_page())
        back_button.place(x=20, y=20)

        # Header
        header_frame = CTkFrame(self, fg_color="white", corner_radius=15)
        header_frame.pack(pady=(60, 20), padx=20, fill="x")
        
        CTkLabel(header_frame,
                text="Your Cart",
                font=("Arial", 24, "bold"),
                text_color="#2d6a4f").pack(pady=10, padx=20)
        
        # Cart Items
        self.items_frame = CTkScrollableFrame(self, fg_color="transparent")
        self.items_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Update cart items
        self.update_cart_items()
        
        # Checkout Section
        self.create_checkout_section()

    def update_cart_items(self):
        # Clear existing items
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        if not self.master.master.cart:
            # Show empty cart message
            empty_frame = CTkFrame(self.items_frame, fg_color="white", corner_radius=15)
            empty_frame.pack(pady=20, padx=20, fill="x")
            
            CTkLabel(empty_frame,
                    text="Your cart is empty",
                    font=("Arial", 16),
                    text_color="#666666").pack(pady=20)
            
            CTkButton(empty_frame,
                    text="Browse Menu",
                    font=("Arial", 14),
                    fg_color="#2d6a4f",
                    hover_color="#1b4332",
                    command=lambda: self.master.master.show_home_page()).pack(pady=10)
            return

        # Add cart items
        for item in self.master.master.cart:
            self.create_cart_item(item)

    def create_cart_item(self, item):
        item_frame = CTkFrame(self.items_frame, fg_color="white", corner_radius=15)
        item_frame.pack(pady=5, padx=5, fill="x")
        
        # Item Image
        try:
            img = CTkImage(Image.open(item[3]), size=(80, 80))
        except (FileNotFoundError, AttributeError):
            # Create a placeholder image if the file doesn't exist
            placeholder = Image.new('RGB', (80, 80), color='#E8F5E9')
            draw = ImageDraw.Draw(placeholder)
            draw.text((40, 40), "No Image", fill='#2d6a4f', anchor="mm")
            img = CTkImage(placeholder, size=(80, 80))
            
        CTkLabel(item_frame, image=img, text="", corner_radius=10).pack(side=LEFT, padx=10, pady=10)
        
        # Item Info
        info_frame = CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side=LEFT, padx=10, pady=10, fill="x", expand=True)
        
        CTkLabel(info_frame,
                text=item[0],  # name
                font=("Arial", 16, "bold"),
                text_color="#2d6a4f").pack(anchor="w")
        
        if len(item) > 5:  # If restaurant name is available
            CTkLabel(info_frame,
                    text=item[5],  # restaurant name
                    font=("Arial", 12),
                    text_color="#666666").pack(anchor="w")
        
        CTkLabel(info_frame,
                text=f"₹{item[1]}",  # price
                font=("Arial", 14),
                text_color="#666666").pack(anchor="w")
        
        # Quantity Controls
        quantity_frame = CTkFrame(item_frame, fg_color="transparent")
        quantity_frame.pack(side=RIGHT, padx=10, pady=10)
        
        CTkButton(quantity_frame,
                text="-",
                width=30,
                height=30,
                fg_color="#2d6a4f",
                hover_color="#1b4332",
                command=lambda i=item: self.decrease_quantity(i)).pack(side=LEFT)
        
        CTkLabel(quantity_frame,
                text=str(item[4]),  # quantity
                font=("Arial", 14),
                width=30).pack(side=LEFT, padx=5)
        
        CTkButton(quantity_frame,
                text="+",
                width=30,
                height=30,
                fg_color="#2d6a4f",
                hover_color="#1b4332",
                command=lambda i=item: self.increase_quantity(i)).pack(side=LEFT)
        
        # Remove Button
        CTkButton(item_frame,
                text="✕",
                font=("Arial", 12),
                width=30,
                height=30,
                fg_color="#dc3545",
                hover_color="#c82333",
                command=lambda i=item: self.remove_item(i)).pack(side=RIGHT, padx=10, pady=10)

    def create_checkout_section(self):
        if hasattr(self, 'checkout_frame'):
            self.checkout_frame.destroy()
            
        self.checkout_frame = CTkFrame(self, fg_color="white", corner_radius=15)
        self.checkout_frame.pack(pady=10, padx=20, fill="x", side="bottom")
        
        # Total Price
        total = sum(item[1] * item[4] for item in self.master.master.cart)
        
        CTkLabel(self.checkout_frame,
                text=f"Total: ₹{total:.2f}",
                font=("Arial", 20, "bold"),
                text_color="#2d6a4f").pack(pady=10, padx=20)
        
        # Checkout Button
        CTkButton(self.checkout_frame,
                text="Proceed to Checkout",
                font=("Arial", 16, "bold"),
                width=200,
                height=50,
                fg_color="#2d6a4f",
                hover_color="#1b4332",
                command=self.master.master.proceed_to_checkout,
                state="normal" if self.master.master.cart else "disabled").pack(pady=10, padx=20)

    def decrease_quantity(self, item):
        if item[4] > 1:
            item[4] -= 1
            self.update_cart_items()
            self.create_checkout_section()

    def increase_quantity(self, item):
        item[4] += 1
        self.update_cart_items()
        self.create_checkout_section()

    def remove_item(self, item):
        self.master.master.cart.remove(item)
        self.update_cart_items()
        self.create_checkout_section()

    def proceed_to_checkout(self):
        if not self.master.master.cart:
            messagebox.showwarning("Empty Cart", "Your cart is empty!")
            return
        
        # Calculate total
        total = sum(item[1] * item[4] for item in self.master.master.cart)
        
        # Create order in database
        order_query = """
            INSERT INTO Orders (user_id, status, total_price)
            VALUES (%s, 'pending', %s)
            RETURNING order_id
        """
        order_result = Database.execute(order_query, (self.master.master.user_data[0][0], total), fetch=True)
        order_id = order_result[0][0]
        
        # Add order details
        for item in self.master.master.cart:
            detail_query = """
                INSERT INTO Order_Details (order_id, menu_id, quantity, item_price)
                VALUES (%s, (SELECT menu_id FROM Menu WHERE name = %s), %s, %s)
            """
            Database.execute(detail_query, (order_id, item[0], item[4], item[1]))
        
        # Send confirmation email
        email_subject = "Order Confirmation - Tomato Food Delivery"
        email_body = f"""
        Dear {self.master.master.user_data[0][1]},

        Thank you for your order! Your order has been received and is being processed.

        Order Details:
        Order ID: {order_id}
        Total Amount: ₹{total}

        Items Ordered:
        """
        
        for item in self.master.master.cart:
            email_body += f"\n- {item[0]} (Quantity: {item[4]}) - ₹{item[1] * item[4]}"
        
        email_body += "\n\nWe will notify you once your order is ready for delivery."
        
        try:
            send_mail(to=self.master.master.user_data[0][3], subject=email_subject, content=email_body)
            messagebox.showinfo("Success", "Order placed successfully! Check your email for confirmation.")
            self.master.master.cart = []  # Clear cart
            self.master.master.show_home_page()  # Return to home page
        except Exception as e:
            messagebox.showerror("Error", f"Order placed but failed to send email: {str(e)}")

class MenuPage(Page):
    def __init__(self, master, category_name, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F5F5")
        self.category_name = category_name
        self.create_widgets()

    def create_widgets(self):
        # Back Button
        back_button = CTkButton(self,
                text="← Back to Home",
                font=("Arial", 14),
                fg_color="transparent",
                hover_color="#e8f5e9",
                text_color="#2d6a4f",
                width=120,
                height=40,
                command=lambda: self.master.master.show_home_page())
        back_button.place(x=20, y=20)

        # Category Header
        header_frame = CTkFrame(self, fg_color="white", corner_radius=15)
        header_frame.pack(pady=(60, 20), padx=20, fill="x")
        
        CTkLabel(header_frame,
                text=f"{self.category_name} Menu",
                font=("Arial", 24, "bold"),
                text_color="#2d6a4f").pack(pady=20)

        # Menu Items Container
        self.menu_container = CTkScrollableFrame(self, fg_color="transparent")
        self.menu_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Fetch and display menu items
        self.load_menu_items()

    def load_menu_items(self):
        # Fetch menu items from database
        query = """
            SELECT m.menu_id, m.name, m.description, m.price, r.name as restaurant_name, r.rating
            FROM Menu m
            JOIN Restaurants r ON m.restaurant_id = r.restaurant_id
            WHERE m.category = %s AND m.is_available = TRUE
        """
        menu_items = Database.execute(query, (self.category_name,), fetch=True)

        if not menu_items:
            CTkLabel(self.menu_container,
                    text="No items found in this category",
                    font=("Arial", 16),
                    text_color="#666666").pack(pady=20)
            return

        for item in menu_items:
            self.create_menu_item_card(item)

    def create_menu_item_card(self, item):
        # Create card frame
        card = CTkFrame(self.menu_container, fg_color="white", corner_radius=15)
        card.pack(pady=10, padx=20, fill="x")

        # Item details
        details_frame = CTkFrame(card, fg_color="transparent")
        details_frame.pack(pady=15, padx=20, fill="x")

        # Restaurant name and rating
        restaurant_frame = CTkFrame(details_frame, fg_color="transparent")
        restaurant_frame.pack(fill="x")
        
        CTkLabel(restaurant_frame,
                text=item[4],  # Restaurant name
                font=("Arial", 14),
                text_color="#666666").pack(side="left")
        
        CTkLabel(restaurant_frame,
                text=f"⭐ {item[5]}",  # Rating
                font=("Arial", 14),
                text_color="#666666").pack(side="right")

        # Item name and price
        CTkLabel(details_frame,
                text=item[1],  # Item name
                font=("Arial", 18, "bold"),
                text_color="#2d6a4f").pack(anchor="w", pady=(10,5))
        
        CTkLabel(details_frame,
                text=item[2],  # Description
                font=("Arial", 14),
                text_color="#666666").pack(anchor="w")

        # Price and Add to Cart button
        action_frame = CTkFrame(details_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(10,0))
        
        CTkLabel(action_frame,
                text=f"₹{item[3]}",  # Price
                font=("Arial", 16, "bold"),
                text_color="#2d6a4f").pack(side="left")
        
        CTkButton(action_frame,
                text="Add to Cart",
                font=("Arial", 14),
                fg_color="#2d6a4f",
                hover_color="#1b4332",
                command=lambda: self.add_to_cart(item)).pack(side="right")

    def add_to_cart(self, item):
        # Create cart item tuple with all necessary information
        cart_item = [
            item[1],  # name
            float(item[3]),  # price
            item[2],  # description
            "./Images/food-placeholder.png",  # default image path
            1,  # initial quantity
            item[4]  # restaurant name
        ]
        self.master.master.add_to_cart(cart_item)

class MainPage(CTk):
    def __init__(self, user_data):
        super().__init__()
        
        # Configure window
        self.title("Tomato Food Delivery")
        self.geometry("1280x720")
        self.minsize(1280, 720)
        
        # Store user data
        self.user_data = user_data
        self.cart = []  # List to store cart items
        
        # Create container
        self.container = CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        # Create header
        self.create_header()
        
        # Show home page
        self.show_home_page()

    def create_header(self):
        header = CTkFrame(self.container, height=80, fg_color="white")
        header.pack(fill="x")
        
        # Logo
        logo = CTkLabel(header,
                       image=CTkImage(Image.open('./Images/Tomato-Light.jpg'), size=(80,75)),
                       text="")
        logo.pack(side=LEFT, padx=20)
        
        # Search Bar
        search_entry = CTkEntry(header,
                              placeholder_text="Search food or restaurants...",
                              width=500,
                              height=40,
                              border_width=0,
                              corner_radius=20,
                              fg_color="#EBEBEB")
        search_entry.pack(side=LEFT, padx=20)
        search_entry.bind("<Return>", lambda e: self.search(search_entry.get()))
        
        # Theme Toggle
        theme_btn = CTkButton(header,
                            image=CTkImage(Image.open("./Images/DarkMode.png"), size=(25,25)),
                            text="",
                            width=40,
                            height=40,
                            fg_color="transparent",
                            hover_color="#EBEBEB",
                            command=self.toggle_theme)
        theme_btn.pack(side=RIGHT, padx=10)
        
        # Cart Button
        cart_btn = CTkButton(header,
                           image=CTkImage(Image.open("./Images/Cart-Light.jpg"), size=(30,30)),
                           text="",
                           width=40,
                           height=40,
                           fg_color="transparent",
                           hover_color="#EBEBEB",
                           command=self.show_cart_page)
        cart_btn.pack(side=RIGHT, padx=10)

    def show_home_page(self):
        if hasattr(self, "current_page"):
            self.current_page.destroy()
        self.current_page = HomePage(self.container, self.user_data)
        self.current_page.pack(fill="both", expand=True)

    def show_restaurant_page(self, restaurant_name):
        if hasattr(self, "current_page"):
            self.current_page.destroy()
        self.current_page = RestaurantPage(self.container, restaurant_name)
        self.current_page.pack(fill="both", expand=True)

    def show_cart_page(self):
        if hasattr(self, "current_page"):
            self.current_page.destroy()
        self.current_page = CartPage(self.container)
        self.current_page.pack(fill="both", expand=True)

    def show_menu_page(self, category_name):
        if hasattr(self, "current_page"):
            self.current_page.destroy()
        self.current_page = MenuPage(self.container, category_name)
        self.current_page.pack(fill="both", expand=True)

    def add_to_cart(self, item):
        # Check if item already in cart
        for cart_item in self.cart:
            if cart_item[0] == item[0]:  # Compare names
                cart_item[4] += 1  # Increase quantity
                messagebox.showinfo("Success", f"Added another {item[0]} to cart!")
                return
        
        # Add new item to cart
        self.cart.append(item)
        messagebox.showinfo("Success", f"{item[0]} added to cart!")

    def search(self, query):
        # Implement search functionality
        pass

    def toggle_theme(self):
        # Implement theme toggle
        pass

    def proceed_to_checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Your cart is empty!")
            return
        
        # Calculate total
        total = sum(item[1] * item[4] for item in self.cart)
        
        # Create order in database
        order_query = """
            INSERT INTO Orders (user_id, status, total_price)
            VALUES (%s, 'pending', %s)
            RETURNING order_id
        """
        order_result = Database.execute(order_query, (self.user_data[0][0], total), fetch=True)
        order_id = order_result[0][0]
        
        # Add order details
        for item in self.cart:
            detail_query = """
                INSERT INTO Order_Details (order_id, menu_id, quantity, item_price)
                VALUES (%s, (SELECT menu_id FROM Menu WHERE name = %s), %s, %s)
            """
            Database.execute(detail_query, (order_id, item[0], item[4], item[1]))
        
        # Send confirmation email
        email_subject = "Order Confirmation - Tomato Food Delivery"
        email_body = f"""
        Dear {self.user_data[0][1]},

        Thank you for your order! Your order has been received and is being processed.

        Order Details:
        Order ID: {order_id}
        Total Amount: ₹{total}

        Items Ordered:
        """
        
        for item in self.cart:
            email_body += f"\n- {item[0]} (Quantity: {item[4]}) - ₹{item[1] * item[4]}"
        
        email_body += "\n\nWe will notify you once your order is ready for delivery."
        
        try:
            send_mail(to=self.user_data[0][3], subject=email_subject, content=email_body)
            messagebox.showinfo("Success", "Order placed successfully! Check your email for confirmation.")
            self.cart = []  # Clear cart
            self.show_home_page()  # Return to home page
        except Exception as e:
            messagebox.showerror("Error", f"Order placed but failed to send email: {str(e)}")

if __name__ == "__main__":
    print("Run>>>>>>>>>main.py<<<<<<<<<<File")