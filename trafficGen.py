#!/usr/bin/python

import sys, getopt, subprocess, atexit, threading, time, random
from config import HOSTS, IPERF_HOSTS, IPERF_SERVER, DURATION

HEADER      = '\033[95m'
OKBLUE      = '\033[94m'
OKGREEN     = '\033[92m'
WARNING     = '\033[93m'
FAIL        = '\033[91m'
ENDC        = '\033[0m'
BOLD        = '\033[1m'
UNDERLINE   = '\033[4m'
GIGABIT     = "1073741824"

def goodbye():
    print("Stopping iperf sessions...")
    for i in range(len(HOSTS)):
        print("Stopping iperf server on " + HOSTS[i])
        run_command(HOSTS[i], "stopServer.sh")   

def run_command(host, command):
    subprocess.call("ssh sdn@" + host + " -o StrictHostKeyChecking=no -t 'source ~/.bash_profile && cd traffic && bash " + command + "'", shell=True, stdout=subprocess.PIPE)

def start_servers(hosts):
    # Start iperf3 server deamons on all hosts
    for i in range(len(hosts)):
        print("Starting iperf server on " + hosts[i])
        run_command(hosts[i], "startServer.sh")

def default_iperf():
    print(OKGREEN + "Starting default iperf sessions on 2 threads [10.0.0.1 -> 10.0.0.3] and [10.0.0.2 -> 10.0.0.4] for " + str(DURATION) + " seconds" + ENDC)
    iperf_exec(GIGABIT)

def iperf_exec(speed):
    threads = []

    for i in range(len(IPERF_HOSTS)):
        try:
            print(OKBLUE + "Speed: " + str(int(speed)/1000000) + "Mbps" + ENDC)
            thread = threading.Thread(target=run_command, args=(IPERF_HOSTS[i], "startIperf.sh " + IPERF_SERVER[i] + " " + str(DURATION) + " " + speed))
            thread.daemon = True                          
            thread.start()
        except:
            print("unable to start thread")

    time.sleep(DURATION + 1)
    for thread in threads:
        thread.join()

    subprocess.call("stty sane", shell=True)

def random_iperf():
    print("Please enter the number of iterations:")
    itr = input(">")
    try:
        itr = int(itr)
    except:
        print(WARNING + "Please enter a number" + ENDC)
        return
    print("Performing " + str(itr) + " iterations, " + str(DURATION) + " seconds long each for a total test time of " + str(DURATION * itr) + " seconds")
    print(OKGREEN + "Starting iperf sessions on 2 threads [10.0.0.1 -> 10.0.0.3] and [10.0.0.2 -> 10.0.0.4]" + ENDC)

    for i in range(itr):
        iperf_exec(str(random.randrange(int(GIGABIT))))


def menu():
    print("Please choose an option:")
    print("d: Default options")
    print("r: Random test")
    print("m: Manual mode")
    print("q: quit")
    res = input(">")
    if res == "d":
        default_iperf()
    elif res == "r":
        random_iperf()
    elif res == "m":
        print("Functionality coming soon...")
    elif res == "q":
        return
    else:
        print(WARNING + "Not a valid option, please try again." + ENDC)
        menu()
    menu()

def main():
    atexit.register(goodbye)
    start_servers(HOSTS)
    print(OKBLUE + "\n   ____  _   _  ____   _____  \n  / __ \| \ | |/ __ \ / ____| \n | |  | |  \| | |  | | (___   \n | |  | | . ` | |  | |\___ \  \n | |__| | |\  | |__| |____) | \n  \____/|_| \_|\____/|_____/  \n" + ENDC)
    
    print(BOLD + "There are currently " + str(len(HOSTS)) + " hosts available:" + ENDC)
    for i in range(len(HOSTS)):
        print("Host: " + HOSTS[i])
    print("The duration variable is currently set to " + str(DURATION) + " seconds. Change this in config.py")
    menu()   
    

    #input("Press Enter to quit...")

if __name__ == "__main__":
   main()


#, '-t', '"export PATH=/usr/local/jdk/bin:/usr/kerberos/sbin:/usr/kerberos/bin:/usr/local/sbin:usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/opt/cpanel/composer/bin:/usr/local/easy/bin:/usr/local/bin:/usr/X11R6/bin:/root/bin && sleep 1 && cd traffic && ls"'