from constants import *
class UserSchema:
    def __str__(self,):
         return self.email+" "+self.password[:3]+("*"*len(self.password[3:]))
    def __init__(self,email,password,postsToday=0,lastTimePost=None,data: Dict[str, Dict[str, dict]]={},blocking_state=False) -> None:
        self.email =email
        self.password = password
    
        self.lastTimePost:datetime.datetime =lastTimePost if isinstance(lastTimePost,datetime.datetime) else datetime.datetime.now()
        self.postsToday= postsToday

        self.data: Dict[str, dict[str, dict]] = data
        self.blocking_state=blocking_state
    @property
    def postsToday(self):
        if (datetime.datetime.now()-self.lastTimePost).total_seconds()>MAXIMUM_POSTS:
            self._posttoday=0
            return 0
        return self._posttoday
    @postsToday.setter
    def postsToday(self,val):
        self._posttoday=val
    @property
    def currentstate(self):
        return self.postsToday<MAXIMUM_POSTS
    def __eq__(self, __o: dict) -> bool:
        if isinstance(__o,dict):
            return __o[EMAIL]==self.email and __o[PASSWORD]==self.password
        elif isinstance(__o,UserSchema):
            return self.email==__o.email  and __o.password==self.password
        return False
    def to_dict(self):
        return {EMAIL:self.email,PASSWORD:self.password,POSTSTODAY:self.postsToday,DATA:self.data,LASTPOSTTIME:self.lastTimePost,BLOCKING_STATE:self.blocking_state}
    def save(self):
        for i,user in enumerate(DATAUSED):
            if user==self:
                DATAUSED[i][DATA] = self.data
                DATAUSED[i][POSTSTODAY] =self.postsToday
                DATAUSED[i][LASTPOSTTIME]=self.lastTimePost
                break
        else:
            DATAUSED.append(self.to_dict())
        
        with open("./data.json", "r") as f:
            saving_info_read=f.read()
        try:
            NEW_DATA=[data.copy() for data in DATAUSED]
            for user in NEW_DATA:
                user[LASTPOSTTIME]=convert_time2str(user[LASTPOSTTIME])
                
            with open("./data.json", "w") as f:
                json.dump(NEW_DATA, f)
                print("data saved")
        except Exception as e :
            print(e)
            with open("./data.json", "w") as f:
                f.write(saving_info_read)
        
        return True

with open("./data.json", "r") as f:
    DATAUSED: List[dict] = json.load(f)
    for i in range(len(DATAUSED)):
        DATAUSED[i][LASTPOSTTIME] =convert_str2time(DATAUSED[i][LASTPOSTTIME])
with open("./channel_messages.json", "r") as f:
    MESSAGES: List[Dict[str, str]] = [
        data for data in json.load(f) if "message" in data]
    for i, data in enumerate(MESSAGES):
        MESSAGES[i]["message"] = emoji_pattern.sub(r'', data["message"])
        num=0
        for user in DATAUSED:
            for groub in user["data"].values():
                if str(MESSAGES[i]["id"]) in groub:
                    num+=groub[str(MESSAGES[i]["id"])]
        MESSAGES[i].update({POSTSMESSAGENUM:num})
    MESSAGES.sort(key=lambda message:message["id"],reverse=True)
    MESSAGES.sort(key=lambda message:message[POSTSMESSAGENUM])