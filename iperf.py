import time, sys
import iperf3
import json
from subprocess import check_output
from datetime import datetime
from time import sleep
from config import HOSTS, IPERF_HOSTS, IPERF_SERVER, DURATION, PROTOCOL, BLKSIZE, NUM_STREAMS, BASE_PORT

server_hostname = ""

def iperf():
    duration = int(DURATION)
    protocol = PROTOCOL
    blksize = int(BLKSIZE)
    num_streams = int(NUM_STREAMS)
    port = int(BASE_PORT)
    server_hostname = sys.argv[1]
    
    client = iperf3.Client()
    client.duration = duration
    client.server_hostname = server_hostname
    client.port = port
    client.protocol = protocol
    client.blksize = blksize
    client.num_streams = num_streams

    # print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    result = client.run()

def iperfTCP():
    print("Performing iperf TCP test.....")
    iperf()

try:
    iperfTCP()
except:
    print("There was an error performing the TCP iPerf test. Proceeding...")
    pass
