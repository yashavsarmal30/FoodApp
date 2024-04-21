import datetime
from threading import Thread
from customtkinter import *
from Resources import Next
from Resources.Check import IsEmail, IsPhoneNumber
import Resources.Email as Email
import Resources.HashData as HashData
from Resources.database import Database
from tkinter import messagebox
from typing import Any

def UserLogin(Details: dict, frame: CTkFrame | Any | None) -> None:
    try:
            UserId = Details['Username']
            Password = Details['Password']

            if not UserId or not Password:
                messagebox.showwarning('Empty Field', 'Please enter both username and password.')
                return

            query = None
            if IsEmail(str(UserId)):
                query = 'SELECT password FROM users WHERE Email = %s and is_admin = FALSE'
            elif IsPhoneNumber(str(UserId)):
                query = 'SELECT password FROM users WHERE phone_number = %s and is_admin = FALSE'
            else:
                query = 'SELECT password FROM users WHERE username = %s and is_admin = FALSE'
            
            user_db_pass = Database.execute(query=query, params=(UserId,), fetch=True)

            if user_db_pass:
                if HashData.VerifyPassword(user_db_pass[0][0], Password.encode()):
                    frame.destroy()
                    user_data = Database.execute(query='SELECT * FROM users WHERE password = %s', params=(user_db_pass[0][0],), fetch=True)
                    Thread(target=Email.SendLoginAlert, args=(user_data[0][3],)).start()
                    a =  Next.MainPage(user_data)
                    a.mainloop()
                else:
                    messagebox.showerror("Invalid Credentials", "Invalid username or password.")
            else:
                messagebox.showerror("Invalid Credentials", "Invalid username or password.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def UserSignUp(Details: dict) -> None:
    try:
        Query = "INSERT INTO users (name, username, email, password, phone_number, address, gender, dob) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);" 

        data = (
            Details['Name'],
            Details['Username'],
            Details['Email'],
            Details['Password'],
            Details['Phone No'],
            Details['Address'],
            Details['Gender'],
            datetime.datetime.strptime(Details['Date of Birth'], "%m/%d/%y")
        )

        Database.execute(Query, data)
        messagebox.showinfo("Success", "Account Created Successfully .")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to register user: {e}")

if __name__ == '__main__':
    print("Run >>>>>>> main.py <<<<<<< File")
