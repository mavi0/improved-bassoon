import requests 
import uuid

h = {'Content-type': 'application/json',}

for c in range(1, 10):
    d = '{\"command\": \"killall iperf3\", \"name\": \"kill iperf' + str(uuid.uuid4()) + '\"}'
    print(d)
    print(requests.post("http://localhost:8080/cmd/h" + str(c), headers = h, data = d))


def iperf(startHost, endHost, h, j):
    for i in range(startHost, endHost):
        d = '{\"command\": \"iperf3 -s -p 520' + str(i) + '\", \"name\": \"iperf' + str(uuid.uuid4()) + '\"}'
        print(d)
        print("http://localhost:8080/cmd/h"  + str(j))
        print(requests.post("http://localhost:8080/cmd/h" + str(j), headers = h, data = d))
        
        d = '{\"command\": \"iperf3 -c 10.0.0.' + str(j) + ' -t 600 -p 520' + str(i) + '\", \"name\": \"iperf' + str(uuid.uuid4())+ '\"}'
        print(d)
        print("http://localhost:8080/cmd/h"  + str(i))
        print(requests.post("http://localhost:8080/cmd/h" + str(i), headers = h, data=d))

s = 1
for j in range(7, 10):
    e = s + 2
    iperf(s, e, h, j)
    s = e


    