import os
try:
    from plyer import notification
except Exception:
     os.system("pip3 install plyer")
     
def Send(*,Title : str = '',Message : str = ''):
    """
        Parameters:
                Title   : Title to Been shown in Notification
                message : Message of the Notification
    """
    
    if Title == '' :
         print("In Notifications.Send() Method\n    No Title Or Message Passed")
    elif Message == '' :
            print("In Notifications.Send() Method\n    No Title Or Message Passed")
    else: 
        try:
            notification.notify(
                title = Title,
                message = Message,
                app_name = "Tomato",
                ticker = "Tomato",
                timeout=2,
                app_icon = os.path.join(os.path.dirname(__file__), '..', 'Images', 'Tomato.ico')
            )
        except Exception:
            print("Error Occured While Sending the Notification")



if __name__ == '__main__':
   print("Run >>>>>>>>  main.py <<<<<<<< File")