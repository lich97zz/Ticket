import json
content = ""
with open("test.txt",'r') as f:
    content = f.readlines()
content = content[0]
request_str = json.loads(content)
content_key = content[1:].split(':')[0][1:-1]
res = []
for ticket in request_str[content_key]:
    res.append(ticket)

##balance = 0
##print(co)
##for i in range(len(content)):
##    if content[i]
