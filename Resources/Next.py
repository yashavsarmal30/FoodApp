from re import *
from threading import Thread
from tkinter import messagebox
from tkinter import *
from typing import Literal, Tuple , Any
from PIL import Image   
from customtkinter import *
from dotenv import load_dotenv
import ipapi
from Resources import Email
from Resources.database import Database
from Resources.Notification import Send

load_dotenv()

set_appearance_mode("system")
set_default_color_theme("green")

BuyOrders = []

class UserFrame(CTkScrollableFrame):
    def __init__(self, master :Any, UserData:list ,width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, scrollbar_fg_color: str | Tuple[str] | None = None, scrollbar_button_color: str | Tuple[str] | None = None, scrollbar_button_hover_color: str | Tuple[str] | None = None, label_fg_color: str | Tuple[str] | None = None, label_text_color: str | Tuple[str] | None = None, label_text: str = "", label_font: Tuple | CTkFont | None = None, label_anchor: str = "center", orientation: Literal['vertical'] | Literal['horizontal'] = "vertical"):

        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, scrollbar_fg_color, scrollbar_button_color, scrollbar_button_hover_color, label_fg_color, label_text_color, label_text, label_font, label_anchor, orientation)
        
        frame1 = CTkFrame(self)
        frame1.columnconfigure((0,1,2,3),weight=1)
        frame1.rowconfigure((0),weight=1)
        
        nameframe = CTkFrame(self,height=40) 
        CTkLabel(nameframe,text=f"Hello 🙋‍♂️ {UserData[0][1]}",font=("Segoe UI Emoji",32)).pack(fill=X)
        nameframe.pack(fill=BOTH,side=TOP)
        CTkFrame(self,height=25).pack(expand=True,fill=BOTH)

        ScrollMenus = CTkScrollableFrame(self,orientation='horizontal')

        PizzaImage = CTkImage(Image.open("./Images/Pizza.png"),size=(250,250))
        _ = CTkLabel(ScrollMenus, text="", image=PizzaImage)
        _.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        _.bind('<Button-1>', lambda event: self.Res_Click('Pizza'))

        BurgerImage = CTkImage(Image.open("./Images/Burger.png"),size=(250,250))
        _ = CTkLabel(ScrollMenus, text="", image=BurgerImage)    
        _.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        _.bind('<Button-1>', lambda event: self.Res_Click('Burger'))


        PastaImage = CTkImage(Image.open("./Images/pasta.png"),size=(250,250))
        _ = CTkLabel(ScrollMenus, text="", image=PastaImage)    
        _.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        _.bind('<Button-1>', lambda event: self.Res_Click('Pasta'))

        PanipuriImage = CTkImage(Image.open("./Images/panipuri.png"),size=(250,250))
        _ = CTkLabel(ScrollMenus, text="", image=PanipuriImage)    
        _.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        _.bind('<Button-1>', lambda event: self.Res_Click('Balakrishna'))

        
        IceCreamImage = CTkImage(Image.open("./Images/IceCream.png"),size=(200,200))
        _ = CTkLabel(ScrollMenus, text="", image=IceCreamImage)    
        _.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        _.bind('<Button-1>', lambda event: self.Res_Click('Dessert'))

        ThaliImage = CTkImage(Image.open("./Images/Thali.png"),size=(200,200))
        _ = CTkLabel(ScrollMenus, text="", image=ThaliImage)    
        _.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        _.bind('<Button-1>', lambda event: self.Res_Click('Thali'))
        
        WrapImage = CTkImage(Image.open("./Images/Wrap.png"),size=(200,200))
        _ = CTkLabel(ScrollMenus, text="", image=WrapImage)    
        _.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        _.bind('<Button-1>', lambda event: self.Res_Click('Wrap'))
        
        WaffleImage = CTkImage(Image.open("./Images/Waffle.png"),size=(200,200))
        _ = CTkLabel(ScrollMenus, text="", image=WaffleImage)    
        _.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        _.bind('<Button-1>', lambda _ : self.Res_Click('Dessert'))
        ScrollMenus.pack(expand=True,fill=X)

        CTkFrame(self,height=60).pack(expand=True,fill=BOTH)

        h1 = CTkFrame(self,height=250)
        McdoutletImage = CTkImage(Image.open("./Images/McDoutlet.jpg"),size=(350,220))
        _ = CTkLabel(h1,image=McdoutletImage,text="")
        _.pack(side=LEFT,padx=30)
        _.bind("<Button-1>",lambda _ : self.Res_Click('Pizza Hut'))

        DominosImage = CTkImage(Image.open("./Images/dominosoutlet.jpg"),size=(350,220))
        _ =CTkLabel(h1,image=DominosImage,text="")
        _.pack(side=LEFT,padx=30)
        _.bind("<Button-1>",lambda _ :self.Res_Click('Pizza'))

        wendysImage = CTkImage(Image.open("./Images/wendysoutlet.jpg"),size=(350,220))
        _ = CTkLabel(h1,image=wendysImage,text="")
        _.pack(side=LEFT,padx=30)
        _.bind("<Button-1>",lambda _ :self.Res_Click('Wraps'))
        h1.pack(fill=BOTH)
        
        CTkFrame(self,height=50).pack(expand=True,fill=BOTH)

        h2 = CTkFrame(self,height=250)

        BelgiamwaffleImage = CTkImage(Image.open("./Images/belgianwaffleoutlet.jpg"),size=(350,220))
        _ = CTkLabel(h2,image=BelgiamwaffleImage,text="")
        _.pack(side=LEFT,fill=BOTH,padx=30)
        _.bind("<Button-1>",lambda _ :self.Res_Click('Dessert'))

        hot1 = CTkImage(Image.open("./Images/hotel1.png"),size=(350,220))
        _ = CTkLabel(h2,image=hot1,text="")
        _.pack(side=LEFT,fill=BOTH,padx=30)
        _.bind("<Button-1>",lambda _ :self.Res_Click('Balakrishna'))

        hot2 = CTkImage(Image.open("./Images/hotel2.png"),size=(350,220))
        _ = CTkLabel(h2,image=hot2,text="")
        _.pack(side=LEFT,fill=BOTH,padx=30)
        _.bind("<Button-1>",lambda _ :self.Res_Click('Balakrishna'))
        h2.pack(expand=True,fill=BOTH)

        CTkFrame(self,height=50).pack(expand=True,fill=BOTH)

        h3 = CTkFrame(self,height=250)

        ho1 = CTkImage(Image.open("./Images/juicecenteroutlet.jpg"),size=(350,220))
        _ = CTkLabel(h3,image=ho1,text="")
        _.pack(side=LEFT,fill=BOTH,padx=30)
        _.bind("<Button-1>",lambda _ :self.Res_Click('Beverage'))

        ho2 = CTkImage(Image.open("./Images/updpioutlet.jpeg"),size=(350,220))
        _ = CTkLabel(h3,image=ho2,text="")
        _.pack(side=LEFT,fill=BOTH,padx=30)
        _.bind("<Button-1>",lambda _ :self.Res_Click('Balakrishna'))

        ho3 = CTkImage(Image.open("./Images/hotel3.jpg"),size=(350,220))
        _ = CTkLabel(h3,image=ho3,text="")
        _.pack(side=LEFT,fill=BOTH,padx=30)
        _.bind("<Button-1>",lambda _ :self.Res_Click('Balakrishna'))
        h3.pack(expand=True,fill=BOTH)

        CTkFrame(self,height=50).pack(expand=True,fill=BOTH)
 
        Footer = CTkFrame(self,height=40,border_color='#A6C4A0')
        social = (CTkImage(Image.open("./Images/xcom.png")),CTkImage(Image.open("./Images/instagram.png")),CTkImage(Image.open("./Images/facebook.jpg")))
        CTkLabel(Footer,text="",image=social[0]).pack(side=LEFT,fill=BOTH,padx=10)
        CTkLabel(Footer,text="",image=social[1]).pack(side=LEFT,fill=BOTH,padx=10)
        CTkLabel(Footer,text="",image=social[2]).pack(side=LEFT,fill=BOTH,padx=10)
        try: 
             city = ipapi.location(output='city')
             region = ipapi.location(output='region')
             CTkLabel(Footer,text=f"{city}, {region}",font=("Arial",20)).pack(side=BOTTOM,fill=BOTH,padx=10,pady=20)
        except Exception:
              CTkLabel(Footer,text=f"❤️ Tomato 🍅",font=("Arial",20)).pack(side=BOTTOM,fill=BOTH,padx=10,pady=20)
        Footer.pack(expand=True,fill=BOTH)

    def change_cursor_enter(self,event):
         event.widget.configure(cursor="hand2")  # Change cursor to a hand when hovering over the frame

    def change_cursor_leave(self,event):
         event.widget.configure(cursor="")  # Reset cursor to default when leaving the frame

    def buy(self, item):
        # Append selected item to the list
        BuyOrders.append(item)
        print(f"{item} added to cart")
    
    def Res_Click(self,restro):

        self.destroy()
        l = CTkScrollableFrame(self.master,height=550)
        q = """
                SELECT Restaurants.name AS restaurant_name, 
                       Menu.name AS menu_name, 
                       Menu.price, 
                       Menu.description
                  FROM Menu 
                  JOIN Restaurants ON Menu.restaurant_id = Restaurants.restaurant_id
                 WHERE Menu.name = %s 
                    OR Menu.category = %s 
                    OR Restaurants.name = %s;
            """
        print(restro)
        sr = Database.execute(q,(restro,restro,restro),fetch=True)
        
        if sr:
            for _ , result in enumerate(sr):
                frame = CTkFrame(l, border_width=1, corner_radius=10)  

                # Menu item name (centered and bold)
                menu_label = CTkLabel(frame, text=result[1], font=("Arial", 20, "bold"))
                menu_label.pack(side=LEFT,pady=(20, 10),fill=BOTH,expand=True)  # Increased top padding

                # Description
                desc_label = CTkLabel(frame, text=result[3], font=("Arial", 14))
                desc_label.pack(side=LEFT,pady=(5, 10),fill=BOTH,expand=True)  # Increased top padding

                # Restaurant name
                restaurant_label = CTkLabel(frame, text=result[0], font=("Arial", 16))
                restaurant_label.pack(side=LEFT,pady=(5, 10),fill=BOTH,expand=True )  # Increased top padding
    
                # Price button
                price_button = CTkButton(frame, text=f"₹{result[2]}", font=("Arial", 16), command=lambda r=result: self.buy(r))
                price_button.pack(side=LEFT,pady=(5, 20),fill=BOTH,expand=True)  # Increased bottom padding

                frame.pack(fill='both', padx=10, pady=10)

        else:
            CTkLabel(l, text="No results found.", font=("Arial", 30)).pack()

        l.pack(fill='both',expand=True)

class MainPage(CTk):
    def __init__(self,Urs:list, fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry("1220x700")
        self.resizable(False, False)
        self.UserDetails = Urs
        Header = CTkFrame(self)

        TomatoImage = CTkImage(dark_image=Image.open('./Images/Tomato-Dark.png'),light_image=Image.open('./Images/Tomato-Light.jpg'),size=(100,95))
        LogoLabel = CTkLabel(Header,image=TomatoImage,text='')
        LogoLabel.place(x=90,y=40)

        SearchEntry = CTkEntry(Header,placeholder_text="Search...",bg_color="transparent",corner_radius=25,width=500,height=50,font=("Arial",30))
        SearchEntry.place(x=280,y=65)
        SearchEntry.bind("<Return>", lambda event: self.search(SearchEntry.get()))

        ThemeToggle = CTkImage(dark_image=Image.open("./Images/DarkMode.png"),light_image=Image.open("./Images/LightMode.png"),size=(100,100))
        ThemeLabel = CTkLabel(Header,image=ThemeToggle,text='')
        ThemeLabel.bind('<Button-1>',lambda _ : self.changeapperance(get_appearance_mode()))
        ThemeLabel.place(x=850,y=44)

        CartImage = CTkImage(Image.open("./Images/Cart-Light.jpg"),size=(90,90))
        CartButton = CTkButton(Header,image=CartImage,text='',fg_color="transparent",width=100,height=80,command=self.open_cart)
        CartButton.place(x=1050,y=40)

        Header.pack(side=TOP,fill=BOTH)

        self.IteamPage = UserFrame(self,self.UserDetails)
        self.IteamPage.pack(side=TOP,fill=BOTH,expand=True)
    
    
    def search(self, q):
        # Check if the search results frame already exists
        if hasattr(self, "search_results_frame"):
            # Destroy the existing search results frame and its contents
            self.search_results_frame.destroy()

        query = """
                SELECT Restaurants.name AS restaurant_name, 
                       Menu.name AS menu_name, 
                       Menu.price, 
                       Menu.description
                  FROM Menu 
                  JOIN Restaurants ON Menu.restaurant_id = Restaurants.restaurant_id
                 WHERE Menu.name = %s 
                    OR Menu.category = %s 
                    OR Restaurants.name = %s;
                """
        # Execute the search query
        results = Database.execute(query, (q, q, q), fetch=True)

        # Create a new frame for displaying search results
        self.search_results_frame = CTkFrame(self)

        if results:
            # Add a scrollable frame for displaying search results
            search_results_scrollable_frame = CTkScrollableFrame(self.search_results_frame, orientation="vertical")

            # Display search results
            for result in results:
                result_frame = CTkFrame(search_results_scrollable_frame)
                result_frame.columnconfigure((0, 1), weight=1)
                result_frame.rowconfigure((0), weight=1)

                menu_label = CTkLabel(result_frame, text=result[1], font=("Arial", 20, "bold"))
                menu_label.pack(side="left", pady=(20, 10), fill="both", expand=True)

                desc_label = CTkLabel(result_frame, text=result[3], font=("Arial", 14))
                desc_label.pack(side="left", pady=(5, 10), fill="both", expand=True)

                restaurant_label = CTkLabel(result_frame, text=result[0], font=("Arial", 16))
                restaurant_label.pack(side="left", pady=(5, 10), fill="both", expand=True)

                price_button = CTkButton(result_frame, text=f"₹{result[2]}", font=("Arial", 16),  command=lambda r=result: self.buy(r))
                price_button.pack(side="left", pady=(5, 20), fill="both", expand=True)

                result_frame.pack(fill="both", padx=10, pady=10)

            search_results_scrollable_frame.pack(fill="both", expand=True)
        else:
            # Display "Item Not Found" message
            not_found_label = CTkLabel(self.search_results_frame, text="Item Not Found", font=("Arial", 20))
            not_found_label.pack(fill="both", expand=True)

            self.search_results_frame.after(2500, lambda: self.search_results_frame.destroy())


        # Pack the search results frame 
        self.search_results_frame.pack(fill="both", expand=True)

    def back_to_previous_view(self):
            if hasattr(self, "search_results_frame"):
               self.search_results_frame.destroy()

            self.IteamPage = UserFrame(self, [(None, None)])
            self.IteamPage.pack(fill="x", expand=True)

    def changeapperance(self,mode):
        if mode == 'Light':
            set_appearance_mode('Dark')
        else:
           set_appearance_mode('Light')
    
    def buy(self, item):
        # Append selected item to the list
        BuyOrders.append(item)
        print(f"{item} added to cart")

    def open_cart(self):
        # Destroy the current cart window if it exists
        if hasattr(self, "cart_window"):
            self.cart_window.destroy()

        # Calculate total price with tax and charges
        total_price = sum(item[2] for item in BuyOrders)
        total_price_with_tax = float(total_price) * 1.18  # Add 18% tax
        total_price_with_charges = total_price_with_tax + 30  # Add additional charges (example)

        # Create the cart window
        self.cart_window = Toplevel(self.master,background='#2b2b2b')
        self.cart_window.geometry("800x800")
        self.cart_window.title("Cart")
        self.cart_window.grab_set()

        self.ItemWindow = CTkScrollableFrame(self.cart_window, width=650, height=250)
        for item in BuyOrders:
            item_frame = Frame(self.ItemWindow,background='#2b2b2b')
            item_frame.pack(fill="x", padx=25, pady=5)

            item_name_label = CTkLabel(item_frame, text=item[1], font=("Arial", 25, "bold"))
            item_name_label.pack(side="left", padx=(0, 10))

            item_price_label = CTkLabel(item_frame, text=f"₹{item[2]}", font=("Arial", 25))
            item_price_label.pack(side="left", padx=(0, 10))

            removeitem = CTkButton(item_frame, text="Remove", command=lambda current_item=item: self.remove_item(current_item))
            removeitem.pack(side="left", padx=(0, 10))

        self.ItemWindow.place(x=0, y=0)

           # Display total amount with tax and charges
        total_label = CTkLabel(self.cart_window, text="Total Amount (incl. tax and charges): ₹{:.2f}".format(total_price_with_charges), font=("Arial", 22, "bold"))
        total_label.place(x=10, y=300)

        pay_frame = CTkFrame(self.cart_window, width=750)

        try:
            upi_image = Image.open("./Images/UPI.png")
            upi_photo = CTkImage(upi_image, size=(100, 100))
            upi_label = CTkButton(pay_frame, image=upi_photo, text='', command=lambda: self.Orderpay(1))
            upi_label.place(x=40,y=5)

            COD_Image = Image.open("./Images/COD.png")
            COD_photo = CTkImage(COD_Image, size=(100, 100))
            COD_Button = CTkButton(pay_frame, image=COD_photo, text='', command=lambda:self.Orderpay(2) )
            COD_Button.place(x=300,y=5)
        except FileNotFoundError:
            print("UPI image not found!")

        pay_frame.place(x=0, y=400)

        # Protocol to handle window close
        self.cart_window.protocol("WM_DELETE_WINDOW", self.close_cart)

    def Orderpay(self,n):
        if n == 1 :
            messagebox.showinfo("UPI", "Payment Link will be Sent to Your Email/Phone")
            self.close_cart()
            self.after(2000,lambda:Send(Title='Order Confirmed',Message="Order will be At your Place soon"))
            upi_Order = """
                    
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Pay with UPI</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f0f0f0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        max-width: 400px;
                        background-color: #fff;
                        border-radius: 10px;
                        padding: 20px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }
                    h1 {
                        color: #333;
                    }
                    .upi-image {
                        margin-bottom: 20px;
                        width: 200px; /* Adjust the width as needed */
                        height: auto; /* Maintain aspect ratio */
                    }
                    .pay-button {
                        background-color: #007bff;
                        color: #fff;
                        border: none;
                        padding: 10px 20px;
                        font-size: 16px;
                        border-radius: 5px;
                        cursor: pointer;
                        transition: background-color 0.3s;
                    }
                    .pay-button:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Pay with UPI</h1>
                 <img src="https://images.news18.com/optimize/OIEKg_dFrdqOuNfRJwh6ctdpPQI=/534x300/images.news18.com/ibnlive/uploads/534x300/jpg/2020/02/UPI.jpg" alt="UPI Image" class="upi-image">
                    <button class="pay-button">Pay with UPI</button>

                    <h3>Team Tomato</h3>
                </div>
            </body>
            </html>

                        """
            Thread(target=lambda:Email.send_mail(to= self.UserDetails[0][3],subject="Order Details",content=upi_Order)).start()
        elif n == 2:
            messagebox.showinfo("CASH ON DELIVERY", "Order Successfull!")
            self.close_cart()
            self.after(2000,lambda:Send(Title='Order Confirmed',Message="Order will be At your Place soon"))

    
    def close_cart(self):
        self.cart_window.grab_release()
        self.cart_window.destroy()

 
    def remove_item(self, item):
        BuyOrders.remove(item)
        # Refresh the cart window after removing the item
        self.cart_window.destroy()
        self.open_cart()




# root = MainPage()
# root.mainloop()

if __name__ == "__main__":
    print("Run>>>>>>>>>main.py<<<<<<<<<<File")