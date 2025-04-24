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
import time
import threading

load_dotenv()   #Loads the .env File

set_appearance_mode("system")
set_default_color_theme("green")

class App(CTk):

    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        # Configure DPI awareness
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
            
        self.title("Food Delivery App")
        self.geometry("1430x710")
        
        # Configure grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Set icon and window state
        try:
            self.iconbitmap('./Images/Tomato.ico')
        except:
            pass
            
        # Set window state
        try:
            self.state('zoomed')
        except:
            pass
            
        # Initialize variables for callbacks
        self._after_ids = set()
        
        # Start with login page
        self.User_Login_Page()

    def _safe_after(self, ms, func, *args):
        """Safely schedule an after callback"""
        after_id = self.after(ms, func, *args)
        self._after_ids.add(after_id)
        return after_id

    def _cancel_after(self, after_id):
        """Cancel a scheduled after callback"""
        if after_id in self._after_ids:
            self.after_cancel(after_id)
            self._after_ids.remove(after_id)

    def destroy(self):
        """Override destroy to clean up after callbacks"""
        for after_id in self._after_ids:
            try:
                self.after_cancel(after_id)
            except:
                pass
        self._after_ids.clear()
        super().destroy()

    def User_Login_Page(self) -> None:
        # User Log in Frame
        self.LoginFrame = CTkFrame(self, fg_color=("white", "#2b2b2b"))
        self.LoginFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Left side with logo and branding
        left_frame = CTkFrame(self.LoginFrame, fg_color="transparent")
        left_frame.place(relx=0.1, rely=0.1, relwidth=0.4, relheight=0.8)

        self.LogoImage = CTkImage(Image.open('./Images/Tomato.png'), size=(250, 240))
        self.Logo = CTkLabel(left_frame, image=self.LogoImage, text="")
        self.Logo.pack(pady=(0, 20))

        self.LogoText = CTkLabel(left_frame, 
                               text="TOMATO\nTHE FOOD DELIVERY", 
                               font=("Arial", 35, "bold"),
                               text_color=("#2b2b2b", "white"))
        self.LogoText.pack()

        # Right side with login form
        right_frame = CTkFrame(self.LoginFrame, fg_color="transparent")
        right_frame.place(relx=0.55, rely=0.2, relwidth=0.35, relheight=0.6)

        # Login form elements
        self.Username_Lable = CTkLabel(right_frame, 
                                     text="Login ID", 
                                     font=("Arial", 18, "bold"),
                                     text_color=("#2b2b2b", "white"))
        self.Username_Lable.pack(pady=(0, 5))
        
        self.UserNameEntry = CTkEntry(right_frame, 
                                    corner_radius=10, 
                                    placeholder_text="Enter Username/Email/Phone No", 
                                    width=300, 
                                    height=40,
                                    font=("Arial", 14))
        self.UserNameEntry.pack(pady=(0, 15))

        self.Password_Lable = CTkLabel(right_frame, 
                                     text="Password", 
                                     font=("Arial", 18, "bold"),
                                     text_color=("#2b2b2b", "white"))
        self.Password_Lable.pack(pady=(0, 15))
        
        password_frame = CTkFrame(right_frame, fg_color="transparent")
        password_frame.pack(fill="x")
        
        self.PasswordEntry = CTkEntry(password_frame, 
                                    corner_radius=10, 
                                    placeholder_text="Enter your password", 
                                    width=300, 
                                    height=40,
                                    show="•",
                                    font=("Arial", 14))
        self.PasswordEntry.pack(pady=(0, 15))

        # Show/Hide password button
        self.show_password = False
        def toggle_password():
            self.show_password = not self.show_password
            self.PasswordEntry.configure(show="" if self.show_password else "•")
            toggle_btn.configure(text="👁️" if self.show_password else "👁️‍🗨️")
        
        toggle_btn = CTkButton(password_frame, 
                             text="👁️‍🗨️", 
                             width=40, 
                             height=40,
                             command=toggle_password,
                             fg_color="transparent",
                             hover_color=("#f0f0f0", "#3a3a3a"))
        toggle_btn.pack(side="left", padx=(100, 0))

        # Login button
        self.LoginButton = CTkButton(right_frame, 
                                   text="Log In", 
                                   command=lambda: Auth.UserLogin(self.get_User_Login_Details(), self), 
                                   width=300, 
                                   height=45,
                                   font=("Arial", 16, "bold"),
                                   corner_radius=10)
        self.LoginButton.pack(pady=(20, 10))

        # Sign up link
        signup_frame = CTkFrame(right_frame, fg_color="transparent")
        signup_frame.pack()
        
        self.SignUp_Lable = CTkLabel(signup_frame, 
                                   text="Don't have an account?", 
                                   font=("Arial", 14),
                                   text_color=("#2b2b2b", "white"))
        self.SignUp_Lable.pack(side="left")
        
        self.CreateAccount = CTkLabel(signup_frame, 
                                    text="Sign up", 
                                    font=("Arial", 14, "bold"),
                                    text_color="#1a73e8",
                                    cursor="hand2")
        self.CreateAccount.pack(side="left", padx=(5, 0))
        self.CreateAccount.bind("<Button-1>", lambda _: self.User_SignUp_Page())

    def get_User_Login_Details(self) -> dict:
        UserId = self.UserNameEntry.get()
        UserPassword = self.PasswordEntry.get()
        return {"Username" : UserId,"Password":UserPassword}
    
    def User_SignUp_Page(self) -> None:
        self.LoginFrame.destroy()
        self.SignUpFrame = CTkFrame(self, fg_color=("white", "#2b2b2b"))
        self.SignUpFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Header with logo
        header_frame = CTkFrame(self.SignUpFrame, fg_color="transparent")
        header_frame.pack(pady=(20, 40))

        self.LogoImage = CTkImage(Image.open('./Images/Tomato.png'), size=(80, 80))
        self.Logo = CTkLabel(header_frame, 
                           image=self.LogoImage, 
                           text="TOMATO : THE FOOD DELIVERY", 
                           compound="left",
                           font=("Arial", 24, "bold"),
                           text_color=("#2b2b2b", "white"))
        self.Logo.pack()

        # Progress bar
        self.progress_bar = CTkProgressBar(self.SignUpFrame, width=400)
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)

        # Signup tabs
        self.SignupTabs = CTkTabview(master=self.SignUpFrame, 
                                   width=600, 
                                   height=500,
                                   segmented_button_fg_color=("#f0f0f0", "#3a3a3a"),
                                   segmented_button_selected_color=("#1a73e8", "#1a73e8"),
                                   segmented_button_selected_hover_color=("#0d47a1", "#0d47a1"))
        self.SignupTabs.pack(pady=(0, 20))
        
        # Create tabs
        self.SignupTabs.add("Personal Info")
        self.SignupTabs.add("Contact Info")
        self.SignupTabs.add("Verification")
        self.SignupTabs.set("Personal Info")
        self.SignupTabs.configure(state="disabled")

        # Personal Info Tab
        personal_frame = CTkFrame(self.SignupTabs.tab("Personal Info"), fg_color="transparent")
        personal_frame.pack(padx=20, pady=20)

        # Name fields
        name_frame = CTkFrame(personal_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 15))
        
        self.Name_Lable = CTkLabel(name_frame, 
                                 text="Name", 
                                 font=('Arial', 16, "bold"),
                                 text_color=("#2b2b2b", "white"))
        self.Name_Lable.pack(side="left", padx=(0, 10))
        
        self.FNameEntry = CTkEntry(name_frame, 
                                 placeholder_text="First Name", 
                                 width=150, 
                                 height=35,
                                 font=('Arial', 14))
        self.FNameEntry.pack(side="left", padx=(0, 10))
        
        self.LNameEntry = CTkEntry(name_frame, 
                                 placeholder_text="Last Name", 
                                 width=150, 
                                 height=35,
                                 font=('Arial', 14))
        self.LNameEntry.pack(side="left")

        # Username field
        username_frame = CTkFrame(personal_frame, fg_color="transparent")
        username_frame.pack(fill="x", pady=(0, 15))
        
        self.Username_Lable = CTkLabel(username_frame, 
                                     text="Username", 
                                     font=('Arial', 16, "bold"),
                                     text_color=("#2b2b2b", "white"))
        self.Username_Lable.pack(side="left", padx=(0, 10))
        
        self.usernameEntry = CTkEntry(username_frame, 
                                    placeholder_text="Ex: thefoodieHuman", 
                                    width=310, 
                                    height=35,
                                    font=('Arial', 14))
        self.usernameEntry.pack(side="left")

        # Password field with strength indicator
        password_frame = CTkFrame(personal_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 15))
        
        self.UserPassword_Lable = CTkLabel(password_frame, 
                                         text="Password", 
                                         font=('Arial', 16, "bold"),
                                         text_color=("#2b2b2b", "white"))
        self.UserPassword_Lable.pack(side="left", padx=(0, 10))
        
        self.UserPasswordEntry = CTkEntry(password_frame, 
                                        show='•', 
                                        placeholder_text="Strong Password", 
                                        width=310, 
                                        height=35,
                                        font=('Arial', 14))
        self.UserPasswordEntry.pack(side="left")

        # Date of Birth
        dob_frame = CTkFrame(personal_frame, fg_color="transparent")
        dob_frame.pack(fill="x", pady=(0, 15))
        
        self.Dob_Label = CTkLabel(dob_frame, 
                                text="Date of Birth", 
                                font=('Arial', 16, "bold"),
                                text_color=("#2b2b2b", "white"))
        self.Dob_Label.pack(side="left", padx=(0, 10))
        
        self.DOB = Calendar(dob_frame, 
                          selectmode='day',
                          year=2000, 
                          month=1, 
                          day=1,
                          background='white',
                          foreground='black',
                          bordercolor='#1a73e8',
                          headersbackground='#1a73e8',
                          headersforeground='white',
                          selectbackground='#1a73e8',
                          selectforeground='white')
        self.DOB.pack(side="left")

        # Gender selection
        gender_frame = CTkFrame(personal_frame, fg_color="transparent")
        gender_frame.pack(fill="x", pady=(0, 15))
        
        self.Gender_Label = CTkLabel(gender_frame, 
                                   text="Gender", 
                                   font=('Arial', 16, "bold"),
                                   text_color=("#2b2b2b", "white"))
        self.Gender_Label.pack(side="left", padx=(0, 10))
        
        self.UserGender = StringVar()
        self.GenderMBox = CTkRadioButton(gender_frame, 
                                       text="Male", 
                                       variable=self.UserGender, 
                                       value='Male',
                                       font=('Arial', 14))
        self.GenderMBox.pack(side="left", padx=(0, 10))
        
        self.GenderFBox = CTkRadioButton(gender_frame, 
                                       text="Female", 
                                       variable=self.UserGender, 
                                       value='Female',
                                       font=('Arial', 14))
        self.GenderFBox.pack(side="left")

        # Next button
        self.NextTo50p = CTkButton(personal_frame, 
                                 text="Next →", 
                                 command=lambda: self.SignupValidation(1), 
                                 width=160, 
                                 height=40,
                                 font=('Arial', 14, "bold"),
                                 corner_radius=10)
        self.NextTo50p.pack(pady=(20, 0))

        # Contact Info Tab
        contact_frame = CTkFrame(self.SignupTabs.tab("Contact Info"), fg_color="transparent")
        contact_frame.pack(padx=20, pady=20)

        # Email field
        email_frame = CTkFrame(contact_frame, fg_color="transparent")
        email_frame.pack(fill="x", pady=(0, 15))
        
        self.EmailID_Lable = CTkLabel(email_frame, 
                                    text="Email", 
                                    font=('Arial', 16, "bold"),
                                    text_color=("#2b2b2b", "white"))
        self.EmailID_Lable.pack(side="left", padx=(0, 10))
        
        self.UserEmailEntry = CTkEntry(email_frame, 
                                     placeholder_text="example@email.com", 
                                     width=310, 
                                     height=35,
                                     font=('Arial', 14))
        self.UserEmailEntry.pack(side="left")

        # Phone field
        phone_frame = CTkFrame(contact_frame, fg_color="transparent")
        phone_frame.pack(fill="x", pady=(0, 15))
        
        self.PhoneNo_Lable = CTkLabel(phone_frame, 
                                    text="Phone", 
                                    font=('Arial', 16, "bold"),
                                    text_color=("#2b2b2b", "white"))
        self.PhoneNo_Lable.pack(side="left", padx=(0, 10))
        
        self.UserPhoneNoEntry = CTkEntry(phone_frame, 
                                       placeholder_text="+91 1234567890", 
                                       width=310, 
                                       height=35,
                                       font=('Arial', 14))
        self.UserPhoneNoEntry.pack(side="left")

        # Address field
        address_frame = CTkFrame(contact_frame, fg_color="transparent")
        address_frame.pack(fill="x", pady=(0, 15))
        
        self.Addres_Lable = CTkLabel(address_frame, 
                                   text="Address", 
                                   font=('Arial', 16, "bold"),
                                   text_color=("#2b2b2b", "white"))
        self.Addres_Lable.pack(side="left", padx=(0, 10))
        
        self.UserAddressEntry = CTkTextbox(address_frame, 
                                         height=100, 
                                         width=310,
                                         font=('Arial', 14))
        self.UserAddressEntry.pack(side="left")

        # Navigation buttons
        nav_frame = CTkFrame(contact_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(20, 0))
        
        self.PreviousTo0p = CTkButton(nav_frame, 
                                    text="← Previous", 
                                    command=lambda: self.SignupTabs.set("Personal Info"),
                                    width=150, 
                                    height=40,
                                    font=('Arial', 14, "bold"),
                                    corner_radius=10)
        self.PreviousTo0p.pack(side="left", padx=(0, 10))
        
        self.NextTo100p = CTkButton(nav_frame, 
                                  text="Next →", 
                                  command=lambda: self.SignupValidation(2),
                                  width=150, 
                                  height=40,
                                  font=('Arial', 14, "bold"),
                                  corner_radius=10)
        self.NextTo100p.pack(side="left")

        # Verification Tab
        verification_frame = CTkFrame(self.SignupTabs.tab("Verification"), fg_color="transparent")
        verification_frame.pack(padx=20, pady=20)

        # Captcha
        captcha_frame = CTkFrame(verification_frame, fg_color="transparent")
        captcha_frame.pack(pady=(0, 20))
        
        self.CaptchaImagePng = CTkImage(Image.open('./Temp/CaptchaImage.png'), size=(200, 80))
        self.Captcha = CTkLabel(captcha_frame, 
                              text="", 
                              image=self.CaptchaImagePng)
        self.Captcha.pack(side="left", padx=(0, 10))
        
        self.Reloadcaptcha = CTkButton(captcha_frame, 
                                     text="🔄", 
                                     command=self.reload_captcha,
                                     width=40, 
                                     height=40,
                                     font=('Arial', 16),
                                     corner_radius=20)
        self.Reloadcaptcha.pack(side="left")

        # Captcha input
        captcha_input_frame = CTkFrame(verification_frame, fg_color="transparent")
        captcha_input_frame.pack(fill="x", pady=(0, 15))
        
        self.CaptchaInput_Lable = CTkLabel(captcha_input_frame, 
                                         text="Enter Captcha", 
                                         font=('Arial', 16, "bold"),
                                         text_color=("#2b2b2b", "white"))
        self.CaptchaInput_Lable.pack(side="left", padx=(0, 10))
        
        self.UserCaptchEntry = CTkEntry(captcha_input_frame, 
                                      placeholder_text="Type the text above", 
                                      width=310, 
                                      height=35,
                                      font=('Arial', 14))
        self.UserCaptchEntry.pack(side="left")

        # Terms and conditions
        self.CheckBoxVal = BooleanVar()
        self.TnCAgreeBox = CTkCheckBox(verification_frame, 
                                     variable=self.CheckBoxVal, 
                                     onvalue=1, 
                                     offvalue=0, 
                                     text="I agree to the Terms and Conditions and Privacy Policy",
                                     font=('Arial', 14))
        self.TnCAgreeBox.pack(pady=(0, 20))

        # Sign up button
        self.SignUpButton = CTkButton(verification_frame, 
                                    text="Sign Up", 
                                    command=lambda: self.SignupValidation(3),
                                    width=200, 
                                    height=45,
                                    font=('Arial', 16, "bold"),
                                    corner_radius=10)
        self.SignUpButton.pack()

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
            
            # Validate name
            if not name.strip():
                tk.messagebox.showerror("Error", "Please enter your name.")
                return
                
            # Validate username
            if not username.strip():
                tk.messagebox.showerror("Error", "Please enter a username.")
                return
            if len(username) < 4:
                tk.messagebox.showerror("Error", "Username must be at least 4 characters long.")
                return
                
            # Validate password
            if not password:
                tk.messagebox.showerror("Error", "Please enter a password.")
                return
            if len(password) < 8:
                tk.messagebox.showerror("Error", "Password must be at least 8 characters long.")
                return
                
            # Validate date of birth
            if not dob:
                tk.messagebox.showerror("Error", "Please select your date of birth.")
                return
                
            # Update progress bar and move to next tab
            self.progress_bar.set(0.33)
            self.SignupTabs.set("Contact Info")

        elif Phase == 2:
            em = self.UserEmailEntry.get()
            ph = self.UserPhoneNoEntry.get()
            ad = self.UserAddressEntry.get("0.0", "end").strip()
            
            # Validate email
            if not em:
                tk.messagebox.showerror("Error", "Please enter your email address.")
                return
            if not Check.IsEmail(em):
                tk.messagebox.showerror("Error", "Please enter a valid email address.")
                return
                
            # Validate phone number
            if not ph:
                tk.messagebox.showerror("Error", "Please enter your phone number.")
                return
            if not Check.IsPhoneNumber(ph):
                tk.messagebox.showerror("Error", "Please enter a valid phone number.")
                return
                
            # Validate address
            if not ad:
                tk.messagebox.showerror("Error", "Please enter your address.")
                return
                
            # Update progress bar and move to next tab
            self.progress_bar.set(0.66)
            self.SignupTabs.set("Verification")
            self.reload_captcha()  # Generate new captcha

        elif Phase == 3:
            u1 = self.UserCaptchEntry.get().strip()
            u2 = self.CurrentCapchaText
            t = self.CheckBoxVal.get()

            # Validate captcha
            if not u1:
                tk.messagebox.showerror("Error", "Please enter the captcha text.")
                return
            if u1.lower() != u2.lower():
                tk.messagebox.showerror("Error", "Incorrect captcha. Please try again.")
                self.reload_captcha()
                return
                
            # Validate terms and conditions
            if not t:
                if not tk.messagebox.askyesno("Terms and Conditions", 
                                            "Do you agree to our Terms and Conditions and Privacy Policy?"):
                    return
                self.CheckBoxVal.set(True)
            
            # Update progress bar and complete signup
            self.progress_bar.set(1.0)
            
            # Show loading message
            loading_window = CTkToplevel(self)
            loading_window.title("Signing Up...")
            loading_window.geometry("300x100")
            loading_window.transient(self)
            loading_window.grab_set()
            
            loading_label = CTkLabel(loading_window, text="Creating your account...")
            loading_label.pack(pady=20)
            
            progress = CTkProgressBar(loading_window)
            progress.pack(pady=10)
            progress.set(0)
            
            def update_progress():
                for i in range(101):
                    progress.set(i/100)
                    loading_window.update()
                    time.sleep(0.01)
                    
            # Start progress update in a separate thread
            progress_thread = threading.Thread(target=update_progress)
            progress_thread.daemon = True
            progress_thread.start()
            
            def complete_signup():
                try:
                    Auth.UserSignUp(self.get_User_SignUp_Details())
                    loading_window.destroy()
                    tk.messagebox.showinfo("Success", "Account created successfully!")
                    self.SignUpFrame.destroy()
                    self.User_Login_Page()
                except Exception as e:
                    loading_window.destroy()
                    tk.messagebox.showerror("Error", f"Failed to create account: {str(e)}")
            
            # Schedule signup completion after progress animation
            self._safe_after(2000, complete_signup)

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
        