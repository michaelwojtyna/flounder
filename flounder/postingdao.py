import dataset
import datetime
from posting import Posting

class PostingDao:
    def __init__(self):
        self.connectString = 'sqlite:///postings.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['postings']

    def rowToPosting(self,row):
        posting = Posting(row['userid'], row['item'], row['description'], row['message'],row['status'], row['resolved'], row['value'], row['date'])
        return posting

    def postingToRow(self, posting):
        row = dict(userid = posting.userid, item = posting.item, description = posting.description, message = posting.message, status = posting.status, resolved = posting.resolved, value = posting.value, date = posting.date)
        return row

    def selectByPosting(self,value):
        rows = self.table.find(value=value)
        if (rows is None):
            result = None
        else:
            count = 0
            for row in rows:
                if (count > 0):
                    return None
                else:
                    result = self.rowToPosting(row)
                    count = count + 1
        return result

    def selectAll(self):
        table = self.db['postings']
        rows = table.all()
        result = []
        for row in rows:
            result.append(self.rowToPosting(row))
        result.sort(key=lambda x: datetime.datetime.strptime(x.date, '%Y-%m-%d'))
        result.reverse()
        return result

    def selectByStatus(self, status):
        table = self.db['postings']
        rows = self.table.find(status=status)
        result = []
        for row in rows:
            result.append(self.rowToPosting(row))
        result.sort(key=lambda x: datetime.datetime.strptime(x.date, '%Y-%m-%d'))
        result.reverse()
        return result

    def selectPostByUser(self,userid):
        table = self.db['postings']
        rows = self.table.find(userid=userid)
        result = []
        for row in rows:
            result.append(self.rowToPosting(row))
        result.sort(key=lambda x: datetime.datetime.strptime(x.date, '%Y-%m-%d'))
        result.reverse()
        return result
        

    def insert(self, posting):
        self.table.insert(self.postingToRow(posting))
        self.db.commit()

    def delete(self, value):
        self.table.delete(value=value)
        self.db.commit()

    def resolved(self, resolved):
        self.table.find


       
        
                                           
