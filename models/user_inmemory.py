class User:
    
    def __init__(self):
        self.users = list()
        self.userCount = 0

    def addUser(self, name, gender):
        return self.users.append({"id":self.userCount,"name":name,"gender":gender})
    
    def getUsers(self):
        return self.users
    
user = User()
user.addUser("hem", 12)
print(user.getUsers())