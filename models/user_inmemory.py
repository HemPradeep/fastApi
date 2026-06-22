class UserManager:

    def __init__(self):
        self.users = list()
        self.userCount = 0

    def doesUserExists(self,id):
        index = self.getIndexById(id)
        return type(index) == int

    def addUser(self, name, gender):
        self.userCount+=1
        userRecord = {"id":self.userCount,"user":name,"gender":gender}
        self.users.append(userRecord)
        return self.users.__getitem__(-1)
    
    def getUsers(self):
        return self.users
    
    def editUserData(self, id, user):
        index = self.getIndexById(id)
        userData = self.users.__getitem__(index)
        userData["user"] = user
        return self.users.__getitem__(index)
    
    def getIndexById(self,id):
        return next(
    (i for i, user in enumerate(self.users) if user["id"] == id),
    None
    )
    
    def deleteAUser(self, id):
        index = self.getIndexById(id)
        self.users.pop(index)

    def getUserById(self, id):
        index = self.getIndexById(id)
        return self.users.__getitem__(index)
        