class UserManager:

    def __init__(self):
        self.users = list()
        self.userCount = 0

    def addUser(self, name, gender):
        self.userCount+=1
        userRecord = {"id":self.userCount,"user":name,"gender":gender}
        self.users.append(userRecord)
        return self.users.__getitem__(-1)
    
    def getUsers(self):
        return self.users