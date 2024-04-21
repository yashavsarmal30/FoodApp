import os

try:
    import argon2
except Exception :
    os.system("pip install argon2-cffi")
    print("\n\nRestarting The Program\n\n")

import argon2
hasher = argon2.PasswordHasher()
    
def HashPassword(Password:str) -> str:
    """
    Description: Hashes the Given Password
    Argument: Password (str)
    Returns: Hash Value of the Password (str)
    """
    return hasher.hash(Password)

def VerifyPassword(HashedPassword:str, EntryPassword:str) -> bool:
    """
    Description: Verifies the Password with Hash Value
    Argument: HashedPassword (str) - Hash Value
              EntryPassword (str) - Currently Entered Password
    Returns: True if Password Matches, False Otherwise
    """
    try:
        hasher.verify(HashedPassword, EntryPassword)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False
    except argon2.exceptions.HashingError or Exception:
        # Handle hashing errors, if any
            return False



if __name__ == '__main__':
       print("Run >>>>>>>>  main.py <<<<<<<< File")