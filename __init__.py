from time import sleep
from tkinter.messagebox import showerror
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
from login_face import *

from tkinter import *
from constants import *
from read_messages import *
from typing import *
import datetime
from rules import *
import sys

PRODUCTION_STATE=not (len(sys.argv)>1 and sys.argv[1]=="develop")
if not PRODUCTION_STATE:print("YOU ARE IN DEVELOPING MODE")




class User(UserSchema):
    def __init__(self, data: dict) -> None:
        super().__init__(**data)
    @property
    def postsNum(self):
        num=0
        for group in self.data.values():
            num+=sum(group.values())
        return num
    def get_sites(self, groups: list, messageId: str,noWanted_groups:list=[]):
        maximumAllowedGroups=max(MAXIMUM_POSTS-self.postsToday,0)
        groups=groups.copy()
        def getKeyNum(group:str):
            groupCode = FaceBook_pattern.sub(r"\5", group)
            if groupCode in self.data:
                return sum(self.data[groupCode].values())
            else:
                return 0
        groups.sort(key=getKeyNum)
        for g in noWanted_groups:
            groups.remove(g)
        result=[]
        messageId=str(messageId)
        for group in groups[:maximumAllowedGroups]:
            groupCode = FaceBook_pattern.sub(r"\5", group)
            if groupCode in self.data:
                if messageId not in self.data[groupCode] or not self.data[groupCode][messageId]:
                    self.data[groupCode].update({messageId: 0})
                    result.append(group)
            else:
                self.data.update({groupCode: {messageId: 0}})
                result.append(group)
        return result

    def updateSucceedSites(self, groups, message, num=1):
        for group in groups:
            group = FaceBook_pattern.sub(r"\5", group)
            self.data[group][message] += num
            self.lastTimePost=datetime.datetime.now()
            self.postsToday += num

class UsersController():
    def __init__(self):
        self.users = [User(data) for data in DATAUSED]
        self.activeUser: User = None
    def login(self):
        users = self.users.copy()
        users=[user for user in users if (not user.blocking_state) and user.postsToday<MAXIMUM_POSTS]
        users.sort(key=lambda user: user.postsNum)
        if len(users):
            self.activeUser = users[0]
            return users[0].email, users[0].password
    
    def getSites(self, groups, message,nowanted_groups=[]):
        if not self.activeUser:
            return []
        return self.activeUser.get_sites(groups, message,nowanted_groups)

    def updatesucceed_sites(self, *groups, messageid, num=1):
        self.activeUser.updateSucceedSites(groups, messageid, num)
        if PRODUCTION_STATE:self.activeUser.save()


class Application(UsersController):
    def __init__(self) -> None:
        super().__init__()
        self.driver = webdriver.Chrome(
            CHROME_DRIVER_PATH, options=CHROME_OPTIONS, service_log_path=None)
        self.driver.implicitly_wait(30)
        self.results = []

    def login(self): 
        self.logout()   
        self.results=[]
        data=super().login()
        if data:
            print(f"LOGINING IN {data[0]}")
            email, password = data
            login_drive(self.driver, email, password)
            return email, password
        
        print("NO CURRENT ACTIVE ACCOUNTS")

    def getgroups(self):
        if not self.activeUser:
            if not self.login():return
            sleep(20)  
        if self.results:return
            
        self.results = get_groups_posts(self.driver)
        return self.results

    def logout(self):
        self.driver.delete_all_cookies()
        self.activeUser = False
 
    def add_posts(self):
        if not self.activeUser:
            return self.do_work_forMe()
        if not self.results:
            return print("there is no results")
        total_messages=0
        for data in MESSAGES:
            message, id = data["message"], int(data["id"])
            org_sites = self.getSites(self.results, id,)
            succeed_posts=[]
            while True:
                print("the lenght of can posted sites" ,len(org_sites))
                sites = post2groups(self.driver,org_sites, message,lambda site:self.updatesucceed_sites(site,messageid=id))
                succeed_posts+=sites
                total_messages+=len(sites)
                if not self.activeUser.currentstate:break
                if len(sites)!=len(org_sites):
                    if not len(sites):
                        print("no groups accesed completely failed to access")
                    else:
                        print("there are some drops in groups trying another groups")
                else:
                    break
                
                org_sites = self.getSites(self.results, id,succeed_posts)
                

            if not self.activeUser.currentstate:break   
        
        print(f"First Boot messuages {self.activeUser.email} with total {succeed_posts} Posts has finsihed")
        self.logout()
        self.do_work_forMe()

    def do_work_forMe(self):
        try:
            if not self.activeUser:
                if not self.login():return
                sleep(20)
            self.getgroups()
            self.add_posts()
        except Exception as e:
            print(e)

class App(Tk,Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Application.__init__(self)
        Button(self, text="login", command=self.login).pack()
        
        Button(self, text="groups", command=self.getgroups).pack()
        
        Button(self, text="add posts", command=self.add_posts).pack()
        
        Button(self, text="Do all Work",command=self.do_work_forMe).pack()
        
        self.after(1000, self.do_work_forMe)
    def login(self):
        data=super().login()
        if not data:
            return self.destroy()
        return data
    def destroy(self) -> None:
        self.driver.quit()
        return super().destroy()

def run():
    App().mainloop()

    

    
if __name__ == '__main__':
    run()
