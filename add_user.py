from constants import *
from read_messages import *
def add_user():
    accounts=[]
    while True:
        try:
            input_str=str(input("email :"))
            password=str(input("password :"))
            if input_str and password:
                user=UserSchema(input_str,password)
                accounts.append(user)
                user.save()
        except KeyboardInterrupt :
            print("finished")
            break
if __name__=="__main__":
    add_user()