#!/usr/bin/env python                                                                                                                                                                                                                                                              [1/114]
                                                                                                                                                                                                                                                                                          
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.log import lg, info
from mininet.node import Node
from mininet.topolib import TreeTopo
from mininet.util import waitListening

class CustomTopo(Topo):
    def __init__(self, bw=1e3, **opts):
        super(CustomTopo, self).__init__(**opts)

        s = [self.addSwitch('s%d' % n) for n in range(1, 4)]
        h = [self.addHost('h%d' % n) for n in range(1, 5)]

        self.addLink(s[0], s[1], bw=bw)
        self.addLink(s[0], s[2], bw=bw)
        self.addLink(s[2], s[1], bw=bw)

        self.addLink(h[0], s[0], bw=bw)
        self.addLink(h[1], s[0], bw=bw)
        self.addLink(h[2], s[1], bw=bw)
        self.addLink(h[3], s[1], bw=bw)

def connectToRootNS( network, switch, ip, routes ):
    """Connect hosts to root namespace via switch. Starts network.
      network: Mininet() network object
      switch: switch to connect to root namespace
      ip: IP address for root namespace node
      routes: host networks to route to"""
    # Create a node in root namespace and link to switch 0
    root = Node( 'root', inNamespace=False )
    intf = network.addLink( root, switch ).intf1
    root.setIP( ip, intf=intf )
    # Start network that now includes link to root namespace
    network.start()
    # Add routes from root ns to hosts
    for route in routes:
        root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

def sshd( network, cmd='/usr/sbin/sshd', opts='-D',
          ip='10.123.123.1/32', routes=None, switch=None ):
    """Start a network, connect it to root ns, and run sshd on all hosts.
       ip: root-eth0 IP address in root namespace (10.123.123.1/32)
       routes: Mininet host networks to route to (10.0/24)
       switch: Mininet switch to connect to root namespace (s1)"""
    if not switch:
        switch = network[ 's1' ]  # switch to use
    if not routes:
        routes = [ '10.0.0.0/24' ]
    connectToRootNS( network, switch, ip, routes )
    for host in network.hosts:
        host.cmd( cmd + ' ' + opts + '&' )
    info( "*** Waiting for ssh daemons to start\n" )
    for server in network.hosts:
        waitListening( server=server, port=22, timeout=5 )

    info( "\n*** Hosts are running sshd at the following addresses:\n" )
    for host in network.hosts:
        info( host.name, host.IP(), '\n' )
    info( "\n*** Type 'exit' or control-D to shut down network\n" )
    CLI( network )
    for host in network.hosts:
        host.cmd( 'kill %' + cmd )
    network.stop()

if __name__ == '__main__':
    net = Mininet(topo=CustomTopo(),
                  controller=RemoteController,
                  cleanup=True,
                  autoSetMacs=True,
                  autoStaticArp=True,
                  link=TCLink)
    net.start()
    sshd( net )
    net.pingAll()
