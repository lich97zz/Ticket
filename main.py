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
##out = os.popen(cmd).read()

from subprocess import PIPE, run

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

out_str = out(cmd)
print("OUT:",out_str)
