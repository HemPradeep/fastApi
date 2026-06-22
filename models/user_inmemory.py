class UserManager:
    
    def __init__(self):
        self.users = list()
        self.userCount = 0

    def addUser(self, name, gender):
        self.userCount+=1
        return self.users.append({"id":self.userCount,"user":name,"gender":gender})
    
    def getUsers(self):
        return [{"id":1, "user":"pradeep", "gender": "M"}]