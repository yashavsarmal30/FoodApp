import re

def IsEmail(email) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def IsStrongPassword(password) -> bool:
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password) is not None

def IsPhoneNumber(phone_number) -> bool:
    pattern = r'^\d{10}$'
    return re.match(pattern, phone_number) is not None

def isValidPanCardNo(panCardNo):

    regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"

    p = re.compile(regex)

    if(panCardNo == None):
        return False
    
    if(re.search(p, panCardNo) and len(panCardNo) == 10):
        return True
    else:
        return False 


if __name__ == '__main__':
   print("Run >>>>>>>>  main.py <<<<<<<< File")