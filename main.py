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
        update_time = self.get_attr('updated_at',25)
        update_time = update_time.replace('T',' ')
        update_time = update_time.replace('Z','')
        requester_id = self.get_attr('requester_id',20)
        return [index,update_time,subject,requester_id]

    def detail_info(self):
        return self.contents
##        res = []
##        for attr in self.contents.keys():
##            res.append([attr,self.get_attr(attr)])
##        return res
    def empty_val(self,attr):
        empty = ['','None','[]','{}']
        return self.contents[attr] in empty
    
class Query:
    def __init__(self):
        self.ticket_arr = []

    def __init__(self,content):
        self.ticket_arr = []
        request_str = json.loads(content)
        content_key = content[1:].split(':')[0][1:-1]

        #err handle
        err_key = ['Error','ERROR','error']
        for err in err_key:
            if err in content_key:
                print("Oops, something wrong happened with err:",content_key[err])
                if 'message' in content_key:
                    print("Info:",content_key['message'])
                raise Exception
            
        self.ticket_arr = []
        for ticket in request_str[content_key]:
            self.ticket_arr.append(Ticket(ticket))
        self.ticket_arr.sort(key=self.sortf)
        
    def time_to_arr(self, time_str):
        date = time_str.split('T')[0]
        time = time_str.split('T')[1][:-1]
        year,month,day = date.split('-')
        hour,minute,second = time.split(':')
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        return [year,month,day,hour,minute,second]
    
    def sortf(self,ticket):
        time = ticket.get_attr('updated_at')
        return self.time_to_arr(time)

    def display_ticket_simple(self, start_id, end_id):
        if end_id > len(self.ticket_arr):
            end_id = len(self.ticket_arr)
        if start_id < 0:
            start_id = 0
            end_id = start_id+25
        print("View ",start_id+1,"to",end_id," out of", len(self.ticket_arr),"tickets")
        pt = prettytable.PrettyTable(['id','Updated at','subject','requester'])
        for i in range(start_id,end_id):
            ticket = self.ticket_arr[i]
            info = ticket.simple_info()
            pt.add_row(info)
        print(pt)

    def display_ticket_detail(self,ticket_id):
        def display_attr(ticket,key,max_key_len,max_val_len=75):
            if key not in ticket.contents.keys():
                return
            
            stdout_key = key+(max_key_len-len(key))*'.'
            val = str(ticket.contents[key])

            if key == 'description':
                print(stdout_key+'\n\n'+val+'\n')
                return
            
            if key in ['created_at','updated_at']:
                val = val.replace('T', ' ')
                val = val.replace('Z', '')
                
            stdout_val = ""
            for i in range(min(max_val_len,len(val))):
                stdout_val+=val[i]
            if len(val) > max_val_len:
                stdout_val+='\n '
                stdout_val+=max_key_len*' '
                for i in range(max_val_len, len(val)):
                    if i%max_val_len == 0:
                        stdout_val+='\n '
                        stdout_val+=max_key_len*' '
                    stdout_val+=val[i]
            print(stdout_key,val)

        tmp_id = -1
        for i in range(len(self.ticket_arr)):
            if ticket_id == self.ticket_arr[i].contents['id']:
                tmp_id = i
                break
        if tmp_id == -1:
            print("**Invalid ticket id ",ticket_id)
            return
        
        print("Displaying ticket #",ticket_id)

        ticket_id = tmp_id
        
        ticket = self.ticket_arr[ticket_id]
        detail_info = ticket.detail_info()
        display_keys = []
        for key in detail_info.keys():
            empty = ['','None','[]','{}',None,[]]
            if detail_info[key] in empty:
                continue
            display_keys.append(key)
        key_len = [len(key) for key in display_keys]
        max_key_len = max(key_len)+1

        order = ['id','subject','description','status','requester_id','created_at',\
                 'updated_at','assignee_id']
        for key in order:
            if key in display_keys:
                display_attr(ticket,key,max_key_len)
                display_keys.remove(key)
        
        display_keys.sort()
        for key in display_keys:
            display_attr(ticket,key,max_key_len)

def main():
    subdomain = ""
    token = ""
    with open("configure",'r') as f:
        f_content = f.readlines()
        if f_content < 2:
            print("Invalid configuration, please check the subdomain and token in the configure file...")
            return
        subdomain = str(f_content[0])
        token = str(f_content[1])
    cmd = "curl https://"+subdomain+".zendesk.com/api/v2/users.json -H \"Authorization: Bearer "+token+"\""
    ##cmd = "curl https://"+subdomain+".zendesk.com/api/v2/requests.json -v -u yitaohe2@illinois.edu:MissHarry60."
    content = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout

    display_ticket = 0
    global q
    q = Query(content)

    print("Welcome to ticket viewer")
    print("*Type 1 to view all tickets")
    print("*Type 2 to view a ticket")
    print("*Type 'quit' to exit")

    while True:
        user_in = input("")
        display_ticket = 0
        mode = 1
        
        if user_in in ['1',' 1 ',' 1','  1']:
            while True:
                q.display_ticket_simple(display_ticket,display_ticket+25)
                print("*Type 2 to view a ticket")
                if display_ticket > 0:
                    print("*Type P to view previous page")
                if display_ticket+25 < len(q.ticket_arr):
                    print("*Type N to view next page")
                
                user_in = input("")
                if display_ticket > 0 and user_in in ['P',' P ',' P','  P','p',' p ',' p','  p']:
                    display_ticket -= 25
                elif display_ticket+25 < len(q.ticket_arr) and user_in in ['N',' N ',' N','  N','n',' n ',' n','  n']:
                    display_ticket += 25
                else:
                    if user_in not in ['P',' P ',' P','  P','p',' p ',' p','  p','N',' N ',' N','  N','n',' n ',' n','  n']:
                        break
                
            
        if user_in in ['2',' 2 ',' 2','  2']:
            user_in = input("Please enter ticket id:")
            q.display_ticket_detail(int(user_in))
        if user_in in ['quit','Quit','QUIT','q','Q']:
            print("*Thanks for using ticket viewer. Bye.")
            return
        
        else:
            print()
            print("*Type 1 to view all tickets")
            print("*Type 2 to view a ticket")
            print("*Type 'quit' to exit")


main()

