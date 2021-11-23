import os

class Ticket:
    def __init__(self):
        self.contents = dict()

    def get_attr(self,attr):
        if attr not in self.contents.keys():
            print(attr,"not existed!")
            break
        return self.contents.keys[attr]
    
cmd = "curl https://zccyitaohe.zendesk.com/api/v2/requests.json -v -u yitaohe2@illinois.edu:Lich97zz."
os.system(cmd)
