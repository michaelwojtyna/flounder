import dataset
from user import User
import sys

class UserDao:
    def __init__(self):
        self.connectString = 'sqlite:///usersLF.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['usersLF']

    def rowToUser(self,row):
        user = User(row['userid'], row['password'], row['email'])
        return user

    def userToRow(self,user):
        row = dict(userid=user.userid, password=user.password, email=user.email)
        return row

    def selectByUserid(self,userid):
        rows = self.table.find(userid=userid)
        result = None

        if (rows is None):
           
            print('UserDao:selectByUserid failed to find user with ' + userid)
            result = None
        else:
            count = 0
            for row in rows:
                if (count > 0):
                    print('UserDao:selectByUserid more than one user selected with ' + userid)
                    return None
                else:
                    result = self.rowToUser(row)
                    count = count + 1
        
        
        return result

    def selectAll(self):
        table = self.db['usersLF']
        rows   = table.all()

        result = []
        for row in rows:
            result.append(self.rowToUser(row))

        return result
        
    def insert(self,user):
        self.table.insert(self.userToRow(user))
        self.db.commit()

    def update(self,user):
        self.table.update(self.userToRow(user),['userid'])
        self.db.commit()

    def delete(self,user):
        self.table.delete(userid=userid)
        self.db.commit()

    def populate(self):
        self.table.insert(self.userToRow(User('mwojtyna','flounderAdmin','mwojtyna@students.stonehill.edu')))
        self.table.insert(self.userToRow(User('wgreelish','flounderAdmin','wgreelish@students.stonehill.edu')))
        self.table.insert(self.userToRow(User('icornelius','flounderAdmin','icornelius@students.stonehill.edu')))
        self.table.insert(self.userToRow(User('dsmolinski','flounderAdmin', 'dsmolinski@students.stonehill.edu')))
        self.db.commit()


