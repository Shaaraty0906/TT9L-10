def login(name,password):
    success = False
    file = open("logindatabase.txt","r")
    for i in file:
         a,b = i.split(",")
         b = b.strip()
         if(a==name and b==password):
             success = True
             break
    file.close()
    if(success):
        print("-"*40)
        print("  | Login done, please enter  | ")
        print("-"*40)
    else:
        print("-"*50)
        print("   | You have not register, please register  | ")
        print("-"*50)
        
def register(name,password):
    file = open("logindatabase.txt","a")
    file.write("\n"+name+","+password)
def access(option):
    global name
    if(option=="login"):
        name = input("Enter ID: ")
        password = input("Enter Password: ")
        login(name,password)
    else:
        print(" | Enter ID and new password! | ")
        name = input("Enter ID : ")
        password = input("Enter your password: ")
        register(name,password)
        print(" | You have been registered, ENTER | ")

def begin():
    global option
    print("="*45)
    print(" |  Welcome to the log in page  |")
    print("-"*45)
    print("Press 'login' if you have an account")
    print("Press 'register' if you don't have an account")
    print("="*45)
    option = input("Enter (login/reg): ")
    if(option!="login" and option!="reg"):
        begin()
        
begin()
access(option)

