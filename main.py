import os

class Ticket:
    def __init__(self):
        self.contents = dict()

    def get_attr(self,attr):
        if attr not in self.contents.keys():
            print(attr,"not existed!")
            return
        return self.contents.keys[attr]

#todo configure password and username    
cmd = "curl https://zccjackhe2.zendesk.com/api/v2/groups.json -v -u yitaohe2@illinois.edu:MissHarry60."
out = os.popen(cmd).read()


print("OUT:",out)
