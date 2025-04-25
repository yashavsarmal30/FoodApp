from customtkinter import *
from PIL import Image
from .base_page import Page
from services.ip_location import ip_location_service

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
        
        # Location Display using the new service
        location_text = ip_location_service.get_location()
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
            card.bind("<Button-1>", lambda e, n=name: self.master.show_menu_page(n))
            
            img = CTkImage(Image.open(path), size=(150, 150))
            img_label = CTkLabel(card, image=img, text="", corner_radius=10)
            img_label.pack(pady=5)
            img_label.bind("<Button-1>", lambda e, n=name: self.master.show_menu_page(n))
            
            name_label = CTkLabel(card, 
                    text=name,
                    font=("Arial", 12, "bold"),
                    text_color="#2d6a4f")
            name_label.pack(pady=5)
            name_label.bind("<Button-1>", lambda e, n=name: self.master.show_menu_page(n))
            
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
            
        #     ("Pasta Palace", "./Images/pastaoutlet.jpg", "4.6", "Italian, Pasta"),
        #     ("Street Bites", "./Images/streetfoodoutlet.jpg", "4.1", "Street Food"),
        #     ("Sweet Tooth", "./Images/dessertsoutlet.jpg", "4.7", "Desserts"),
        #     ("Thali House", "./Images/thalioutlet.jpg", "4.4", "Indian, Thali"),
        #     ("Wrap It Up", "./Images/wrapoutlet.jpg", "4.2", "Wraps, Fast Food"),
        #     ("Sushi World", "./Images/sushioutlet.jpg", "4.9", "Japanese, Sushi"),
        #     ("Salad Stop", "./Images/saladoutlet.jpg", "4.5", "Healthy, Salads"),
        #     ("BBQ Nation", "./Images/bbqoutlet.jpg", "4.6", "BBQ, Grill"),
        #     ("Vegan Delight", "./Images/veganoutlet.jpg", "4.8", "Vegan, Healthy")
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
            
            card.bind("<Button-1>", lambda e, n=name: self.master.show_restaurant_page(n))
            card.pack(side=LEFT, padx=10) 