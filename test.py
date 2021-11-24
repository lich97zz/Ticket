import json

raise Exception

class Ticket:
    def __init__(self):
        self.contents = dict()
        
    def __init__(self, content):
        self.contents = content
        
    def get_attr(self,attr):
        if attr not in self.contents.keys():
            return " N/A "
        return self.contents[attr]
    
    def simple_info(self):
        index = self.get_attr('id')
        subject = self.get_attr('subject')
        description = self.get_attr('description')
        return [index,subject,description]
    
content = ""
with open("test.txt",'r') as f:
    content = f.readlines()
content = content[0]
request_str = json.loads(content)
content_key = content[1:].split(':')[0][1:-1]
res = []
for ticket in request_str[content_key]:
    res.append(Ticket(ticket))
    
##import prettytable
##pt = prettytable.PrettyTable(['id','subject','description'])
##for ticket in res:
##    pt.add_row([ticket['id'],ticket['subject'],ticket['description']])
##print(pt)
def sortf(ticket):
    return ticket.get_attr('id')
res.sort(key=sortf)
