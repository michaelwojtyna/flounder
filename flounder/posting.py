class Posting:
    def __init__(self, userid, item, description, message, status, resolved,  value, date):
        self.userid = userid
        self.item = item
        self.description = description
        self.message = message
        self.status = status
        self.resolved = resolved
        self.value = value
        self.date = date

    def toString(self):
        return "Poster: " + self.userid + " Item: " + self.item + " Message: " + self.message +" Description: "+ self.description + "Date: " + self.date 
