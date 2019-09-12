#!/usr/bin/python

import sys, getopt, subprocess, atexit, threading, time
from config import HOSTS, IPERF_HOSTS, IPERF_SERVER, DURATION

def goodbye():
    print("Stopping iperf sessions...\n")
    for i in range(len(HOSTS)):
        print("Stopping iperf server on " + HOSTS[i])
        run_command(HOSTS[i], "stopServer.sh")   

def run_command(host, command):
    subprocess.call("ssh sdn@" + host + " -o StrictHostKeyChecking=no -t 'source ~/.bash_profile && cd traffic && bash " + command + "'", shell=True, stdout=subprocess.PIPE)

def main():
    atexit.register(goodbye)
    # Start iperf3 server deamons on all hosts
    for i in range(len(IPERF_SERVER)):
        print("Starting iperf server on " + IPERF_SERVER[i])
        run_command(IPERF_SERVER[i], "startServer.sh")

    print("Starting default iperf sessions [10.0.0.1 -> 10.0.0.3] and [10.0.0.2 -> 10.0.0.4] for 600 seconds (10 mins)")
    print("More options coming soon...\n")

    threads = []

    for i in range(len(IPERF_HOSTS)):
        try:
            thread = threading.Thread(target=run_command, args=(IPERF_HOSTS[i], "startIperf.sh " + IPERF_SERVER[i]))
            thread.daemon = True                            # Daemonize thread
            thread.start()
            # thread.start_new_thread(run_command, (IPERF_HOSTS[i], "startIperf.sh " + IPERF_SERVER[i]))
        except:
            print("unable to start thread")
        # run_command(IPERF_HOSTS[i], "startIperf.sh " + IPERF_SERVER[i])

    time.sleep(DURATION)
    for thread in threads:
        thread.join()

    subprocess.call("stty sane", shell=True)

    #input("Press Enter to quit...")


if __name__ == "__main__":
   main()


#, '-t', '"export PATH=/usr/local/jdk/bin:/usr/kerberos/sbin:/usr/kerberos/bin:/usr/local/sbin:usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/opt/cpanel/composer/bin:/usr/local/easy/bin:/usr/local/bin:/usr/X11R6/bin:/root/bin && sleep 1 && cd traffic && ls"'