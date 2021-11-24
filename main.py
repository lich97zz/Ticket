import os
from subprocess import PIPE, run
import json
import prettytable



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
#todo configure password and username    
cmd = "curl https://zccjackhe2.zendesk.com/api/v2/requests.json -v -u yitaohe2@illinois.edu:MissHarry60."

def sortf(ticket):
    return ticket.get_attr('id')

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout


def display_ticket_simple(ticket_arr, start_id, end_id):
    pt = prettytable.PrettyTable(['id','subject','description'])
    for i in range(start_id,end_id):
        ticket = ticket_arr[i]
        pt.add_row([ticket['id'],ticket['subject'],ticket['description']])
    print(pt)

content = out(cmd)
request_str = json.loads(content)
content_key = content[1:].split(':')[0][1:-1]
res = []
for ticket in request_str[content_key]:
    res.append(Ticket(ticket))
res.sort(key=sortf)

display_ticket_simple(res, 0,15)
print('***\n')

display_ticket_simple(res, 15,30)


