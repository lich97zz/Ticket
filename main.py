import os

class Ticket:
    def __init__(self):
        self.contents = dict()

    def get_attr(self,attr):
        if attr not in self.contents.keys():
            print(attr,"not existed!")
            return
        return self.contents.keys[attr]
    
cmd = "curl https://zccjackhe2.zendesk.com/api/v2/groups.json -v -u yitaohe2@illinois.edu:MissHarry60."
os.system(cmd)

import sys
from io import TextIOWrapper, BytesIO

# setup the environment
old_stdout = sys.stdout
sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)


# get output
sys.stdout.seek(0)      # jump to the start
out = sys.stdout.read() # read output

# restore stdout
sys.stdout.close()
sys.stdout = old_stdout


print("OUT:",out)
