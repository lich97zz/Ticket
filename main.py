import os
from subprocess import PIPE, run
import json
class Ticket:
    def __init__(self):
        self.contents = dict()

    def get_attr(self,attr):
        if attr not in self.contents.keys():
            print(attr,"not existed!")
            return
        return self.contents.keys[attr]

#todo configure password and username    
cmd = "curl https://zccjackhe2.zendesk.com/api/v2/requests.json -v -u yitaohe2@illinois.edu:MissHarry60."


def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

content = out(cmd)
request_str = json.loads(content)
content_key = content[1:].split(':')[0][1:-1]
res = []
for ticket in request_str[content_key]:
    res.append(ticket)
    
print(res[0])
