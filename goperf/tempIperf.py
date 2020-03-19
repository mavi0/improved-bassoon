import requests 

h = {'Content-type': 'application/json',}

def iperf(startHost, endHost, h, j):
    for i in range(startHost, endHost):
        d = '{\"command\": \"iperf3 -s -p 520' + str(i) + '\", \"name\": \"iperf' + str(i) + str(j) + '\"}'
        print(d)
        print("http://localhost:8080/cmd/h"  + str(j))
        print(requests.post("http://localhost:8080/cmd/h" + str(j), headers = h, data = d))
        
        d = '{\"command\": \"iperf3 -c 10.0.0.' + str(j) + ' -t 600 -p 520' + str(i) + '\", \"name\": \"iperf' + str(j) + str(i) + '\"}'
        print(d)
        print("http://localhost:8080/cmd/h"  + str(i))
        print(requests.post("http://localhost:8080/cmd/h" + str(i), headers = h, data=d))

s = 1
for j in range(7, 10):
    e = s + 2
    iperf(s, e, h, j)
    s = e


    