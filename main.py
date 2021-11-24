import os
from subprocess import PIPE, run
import json
import prettytable

class Ticket:
    def __init__(self):
        self.contents = dict()
        
    def __init__(self, content):
        self.contents = content
        
    def get_attr(self,attr,max_len=99999):
        if attr not in self.contents.keys():
            return " N/A "
        res = str(self.contents[attr])
        if len(res) > max_len:
            res = res[0:max_len]+'...'
        return res
    
    def simple_info(self):
        index = self.get_attr('id',8)
        subject = self.get_attr('subject',30)
        description = self.get_attr('description',20)
        return [index,subject,description]

    def detail_info(self):
        return self.contents
##        res = []
##        for attr in self.contents.keys():
##            res.append([attr,self.get_attr(attr)])
##        return res
    
#todo configure password and username    
cmd = "curl https://zccjackhe2.zendesk.com/api/v2/requests.json -v -u yitaohe2@illinois.edu:MissHarry60."

def sortf(ticket):
    return int(ticket.get_attr('id'))

def shell_out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout


def display_ticket_simple(ticket_arr, start_id, end_id):
    print("Displaying ",start_id,"to",end_id-1," out of", len(ticket_arr),"tickets")
    pt = prettytable.PrettyTable(['Updated at','subject','description'])
    for i in range(start_id,end_id):
        ticket = ticket_arr[i]
        pt.add_row(ticket.simple_info())
    print(pt)

def display_ticket_detail(ticket_arr, ticket_id):
    print("Displaying ticket #",ticket_id)
    ticket = ticket_arr[ticket_id]
    detail_info = ticket.detail_info()
    for key in detail_info.keys:
        print(key,":",detail_info[key])
##    print(detail_info.keys())
##    print(detail_info)
##dict_keys(['url', 'id', 'status', 'priority', 'type', 'subject',
##    'description', 'organization_id', 'via', 'custom_fields', 'requester_id',
##    'collaborator_ids', 'email_cc_ids', 'is_public', 'due_at', 'can_be_solved_by_me',
##    'created_at', 'updated_at', 'recipient', 'followup_source_id', 'assignee_id',
##    'ticket_form_id', 'fields'])

content = shell_out(cmd)
request_str = json.loads(content)
content_key = content[1:].split(':')[0][1:-1]

#err handle
err_key = ['Error','ERROR','error']
for err in err_key:
    if err in content_key:
        print("Oops, something wrong happened with err:",content_key[err])
        raise Exception
    
res = []
for ticket in request_str[content_key]:
    res.append(Ticket(ticket))
res.sort(key=sortf)

display_ticket_simple(res, 0,15)
print('***\n')
##display_ticket_detail(res, 0)
##print('***\n')
##display_ticket_detail(res, 10)



