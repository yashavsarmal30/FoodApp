from Resources import Auth
import random
import tkinter as tk
from Resources import Check , HashData
from PIL import Image
from typing import Tuple
from customtkinter import *
from dotenv import load_dotenv
from tkcalendar import Calendar
from captcha.image import ImageCaptcha

load_dotenv()   #Loads the .env File

set_appearance_mode("system")
set_default_color_theme("green")

class App(CTk):

    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Tomato : Food Delivery")
        self.geometry("1430x710")
        self.after(201, lambda :self.iconbitmap('./Images/Tomato.ico'))
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.after(0, lambda:self.state('zoomed'))
        self.grid_columnconfigure(0, weight=1)

        self.User_Login_Page() # User Login Frame

    def User_Login_Page(self) -> None:
        # User Log in Frame
        self.LoginFrame = CTkFrame(self)

        self.LogoImage = CTkImage(Image.open('./Images/Tomato.png'), size=(200, 190))
        self.Logo = CTkLabel(self.LoginFrame, image=self.LogoImage, text="")
        self.Logo.place(relx=0.14, rely=0.07)

        self.LogoText = CTkLabel(self.LoginFrame, text="TOMATO : THE FOOD DELIVERY", font=("Arial", 35))
        self.LogoText.place(relx=0.35, rely=0.11)

        self.Username_Lable = CTkLabel(self.LoginFrame, text="Login ID : ", font=("Arial", 22))
        self.Username_Lable.place(relx=0.40, rely=0.39)
        self.UserNameEntry = CTkEntry(self.LoginFrame, corner_radius=15, placeholder_text="Enter Username/Email/Phone No", width=250, height=30)
        self.UserNameEntry.place(relx=0.50, rely=0.39)

        self.Password_Lable = CTkLabel(self.LoginFrame, text="Password : ", font=("Arial", 22))
        self.Password_Lable.place(relx=0.40, rely=0.50)
        self.PasswordEntry = CTkEntry(self.LoginFrame, corner_radius=15, placeholder_text="Password", width=250, show="*", height=30)
        self.PasswordEntry.place(relx=0.50, rely=0.50)

        encryptphoto = CTkImage(Image.open("./Images/encrypt.png"), size=(40, 40))
        encrypyimage = CTkLabel(self.LoginFrame, image=encryptphoto, text="")
        encrypyimage.place(relx=0.69, rely=0.49)

        self.LoginButton = CTkButton(self.LoginFrame, text="Log In", command=lambda: Auth.UserLogin(self.get_User_Login_Details(), self), width=100, height=40)
        self.LoginButton.place(relx=0.48, rely=0.60)

        self.SignUp_Lable = CTkLabel(self.LoginFrame, text="Don't Have Account ?  ", font=("Arial", 12))
        self.SignUp_Lable.place(relx=0.47, rely=0.69)
        self.CreateAccount = CTkLabel(self.LoginFrame, text="Create One", font=("Arial", 15), text_color="blue")
        self.CreateAccount.bind("<Button-1>", lambda _: self.User_SignUp_Page())
        self.CreateAccount.place(relx=0.55, rely=0.69)
        
        self.LoginFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def get_User_Login_Details(self) -> dict:
        UserId = self.UserNameEntry.get()
        UserPassword = self.PasswordEntry.get()
        return {"Username" : UserId,"Password":UserPassword}
    
    def User_SignUp_Page(self) -> None:
    # User Sign Up Frame
            self.LoginFrame.destroy()
            self.SignUpFrame = CTkFrame(self)

            self.LogoImage = CTkImage(Image.open('./Images/Tomato.png'), size=(100, 90))
            self.Logo = CTkLabel(self.SignUpFrame, image=self.LogoImage, text="TOMATO : THE FOOD DELIVERY", compound="left")
            self.Logo.pack()
            font = CTkFont(family='Arial', size=25)  # Change the size as needed
            self.Logo.configure(font=font)

            self.SignupTabs = CTkTabview(master=self.SignUpFrame)
            self.SignupTabs.pack(fill='both', expand=True)
            self.SignupTabs.add("0%")
            self.SignupTabs.add("50%")
            self.SignupTabs.add("100%")
            self.SignupTabs.set("0%")
            self.SignupTabs.configure(state="disabled")

            self.Name_Lable = CTkLabel(self.SignupTabs.tab("0%"), text="Name : ", font=('Arial', 21))
            self.Name_Lable.place(relx=0.2, rely=0.1)
            self.FNameEntry = CTkEntry(self.SignupTabs.tab("0%"), placeholder_text="First Name ", width=150, height=32)
            self.FNameEntry.place(relx=0.3, rely=0.1)
            self.LNameEntry = CTkEntry(self.SignupTabs.tab("0%"), placeholder_text="Last Name ", width=150, height=32)
            self.LNameEntry.place(relx=0.47, rely=0.1)

            self.Username_Lable = CTkLabel(self.SignupTabs.tab("0%"), text="Create Username : ", font=('Arial', 21))
            self.Username_Lable.place(relx=0.2, rely=0.2)
            self.usernameEntry = CTkEntry(self.SignupTabs.tab("0%"), placeholder_text="Ex: thefoodieHuman", width=150, height=32)
            self.usernameEntry.place(relx=0.43, rely=0.2)
            self.UserPassword_Lable = CTkLabel(self.SignupTabs.tab("0%"), text="Create Password : ", font=('Arial', 19))
            self.UserPassword_Lable.place(relx=0.2, rely=0.3)
            self.UserPasswordEntry = CTkEntry(self.SignupTabs.tab("0%"), show='*', placeholder_text="Strong Password", width=150, height=32)
            self.UserPasswordEntry.place(relx=0.43, rely=0.3)

            self.Dob_Label = CTkLabel(self.SignupTabs.tab("0%"), text="Date Of Birth : ", font=('Arial', 21))
            self.Dob_Label.place(relx=0.2, rely=0.4)
            self.DOB = Calendar(self.SignupTabs.tab("0%"))
            self.DOB.place(relx=0.43, rely=0.4)

            self.Gender_Label = CTkLabel(self.SignupTabs.tab("0%"), text="Gender : ", font=('Arial', 21))
            self.Gender_Label.place(relx=0.2, rely=0.67)
            self.UserGender = StringVar()
            self.GenderMBox = CTkRadioButton(self.SignupTabs.tab('0%'), text="MALE", variable=self.UserGender, value='Male')
            self.GenderMBox.place(relx=0.3, rely=0.67)
            self.GenderFBox = CTkRadioButton(self.SignupTabs.tab('0%'), text="FEMALE", variable=self.UserGender, value='Female')
            self.GenderFBox.place(relx=0.45, rely=0.67)

            self.NextTo50p = CTkButton(master=self.SignupTabs.tab("0%"), text="Next", command=lambda: self.SignupValidation(1), width=160, height=35)
            self.NextTo50p.place(relx=0.3, rely=0.75)

            # <------------------------------------------------------------------------------------------------------------------------------------------>
            self.EmailID_Lable = CTkLabel(master=self.SignupTabs.tab("50%"), text="EMAIL ID : ", font=('Arial', 21))
            self.EmailID_Lable.place(relx=0.2, rely=0.1)
            self.UserEmailEntry = CTkEntry(master=self.SignupTabs.tab("50%"), placeholder_text="fodie@pizza.com", width=180, height=32)
            self.UserEmailEntry.place(relx=0.3, rely=0.1)

            self.PhoneNo_Lable = CTkLabel(master=self.SignupTabs.tab("50%"), text="Phone No  : ", font=('Arial', 20))
            self.PhoneNo_Lable.place(relx=0.2, rely=0.2)
            self.UserPhoneNoEntry = CTkEntry(master=self.SignupTabs.tab("50%"), placeholder_text="+91123456789", width=180, height=32)
            self.UserPhoneNoEntry.place(relx=0.3, rely=0.2)

            self.Addres_Lable = CTkLabel(master=self.SignupTabs.tab("50%"), text="Your Home Address  : ", font=('Arial', 20))
            self.Addres_Lable.place(relx=0.2, rely=0.3)
            self.UserAddressEntry = CTkTextbox(master=self.SignupTabs.tab('50%'), height=100, width=310)
            self.UserAddressEntry.place(relx=0.35, rely=0.3)

            self.PreviousTo0p = CTkButton(master=self.SignupTabs.tab("50%"), command=lambda: self.SignupTabs.set("0%"), text="Previous")
            self.PreviousTo0p.place(relx=0.3, rely=0.6)

            self.NextTo100p = CTkButton(master=self.SignupTabs.tab("50%"), command=lambda: self.SignupValidation(2), text="Next")
            self.NextTo100p.place(relx=0.6, rely=0.6)
            # <--------------------------------------------------------------------------------------------------------------------------------------------->
            self.CurrentCapchaText = None
            self.CaptchaImagePng = CTkImage(Image.open('./Temp/CaptchaImage.png'), size=(200, 180))
            self.Captcha = CTkLabel(master=self.SignupTabs.tab("100%"), text="", image=self.CaptchaImagePng)
            self.Captcha.pack()
            self.Reloadcaptcha = CTkButton(master=self.SignupTabs.tab("100%"), command=self.reload_captcha, text="reload")
            self.Reloadcaptcha.place(relx=0.65, rely=0.1)
            self.CaptchaInput_Lable = CTkLabel(master=self.SignupTabs.tab("100%"), text="Enter The Given Captcha : ", font=('Arial', 21))
            self.CaptchaInput_Lable.place(relx=0.3, rely=0.41)
            self.UserCaptchEntry = CTkEntry(master=self.SignupTabs.tab("100%"), placeholder_text="captcha", width=200, height=45, font=('Arial', 15))
            self.UserCaptchEntry.place(relx=0.5, rely=0.4)

            self.CheckBoxVal = BooleanVar()
            self.TnCAgreeBox = CTkCheckBox(self.SignupTabs.tab('100%'), variable=self.CheckBoxVal, onvalue=1, offvalue=0, text="Agree To Our Term's and Conditions and Privacy Policy")
            self.TnCAgreeBox.place(relx=0.35, rely=0.55)

            self.SignUpButton = CTkButton(master=self.SignupTabs.tab("100%"), text="Sign Up", width=160, height=35, command=lambda: self.SignupValidation(3))
            self.SignUpButton.place(relx=0.4, rely=0.62)

            self.SignUpFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def get_User_SignUp_Details(self) -> dict:
        Dob      = self.DOB.get_date()
        Gender   = self.UserGender.get()
        Username = self.usernameEntry.get()
        Email    = self.UserEmailEntry.get()
        PhoneNo  = self.UserPhoneNoEntry.get()
        Address  = self.UserAddressEntry.get("0.0", "end")
        Name     = f'{self.FNameEntry.get()} {self.LNameEntry.get()}'
        password = HashData.HashPassword(self.UserPasswordEntry.get())

        return {"Name":Name,'Username':(Username),"Password":(password),'Date of Birth':(Dob),'Gender':Gender,'Email':(Email),'Phone No':(PhoneNo),'Address':(Address)}

    def SignupValidation(self, Phase: int) -> None:
        if Phase == 1:
            name = f'{self.FNameEntry.get()}{self.LNameEntry.get()}'
            username = self.usernameEntry.get()
            password = self.UserPasswordEntry.get()
            dob = self.DOB.get_date()
            if not name or not username or not password or not dob:
                tk.messagebox.showerror("Incomplete", "Please enter all required details.")
            else:
                self.SignupTabs.set("50%")

        elif Phase == 2:
            em = self.UserEmailEntry.get()
            ph = self.UserPhoneNoEntry.get()
            ad = self.UserAddressEntry.get("0.0", "end")
                
            if not em or not ph or not ad:
                tk.messagebox.showerror("Incomplete", "Please enter all required details.")
            else : 
                if Check.IsEmail(em) and Check.IsPhoneNumber(ph):
                    self.SignupTabs.set("100%")
                else:
                 tk.messagebox.showerror("Invalid", "Invalid Email Or Phone Number")

        elif Phase == 3:
            u1 = self.UserCaptchEntry.get()
            u2 = self.CurrentCapchaText
            t  = self.TnCAgreeBox.get()

            if u1 == u2 :
                if t == 1:
                    pass
                else :
                  if tk.messagebox.askyesno("Agreement","Do You Agree to out T&C ?"):
                      self.CheckBoxVal.set(not self.CheckBoxVal.get())
            else :
                tk.messagebox.showerror("Invalid", "Invalid Captcha.")
                return
            
            Auth.UserSignUp(self.get_User_SignUp_Details())
            self.SignUpFrame.destroy()
            self.User_Login_Page() # User Login Frame

    def reload_captcha(self) -> None:
        
        foods = [
        "pizza",
        "burger",
        "sushi",
        "pasta",
        "salad",
        "taco",
        "steak",
        "sandwich",
        "ramen",
        "curry",
        "pancake",
        "waffle",
        "ice cream",
        "cake",
        "cookie",
        "muffin"
        ]       

        x = random.randrange(0, len(foods) - 1)
        captcha_text = foods[x]
        self.CurrentCapchaText = foods[x]
        captcha = ImageCaptcha(font_sizes=(40, 60, 70), fonts=["arial"], width=200, height=180)
        captcha_image = captcha.generate(captcha_text).read()

        with open('./Temp/CaptchaImage.png', 'wb') as f:
            f.write(captcha_image)
 
        self.CaptchaImagePng = CTkImage(Image.open('./Temp/CaptchaImage.png'), size=(200, 180))
        self.Captcha.configure(image=self.CaptchaImagePng)

if __name__ == "__main__":
        app = App()
        app.mainloop()
        