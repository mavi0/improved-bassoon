#!/usr/bin/env python

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.log import setLogLevel


class TowerTopo( Topo ):
    """Create a tower topology"""

    def build( self, k=4, h=6 ):
        spines = []
        leaves = []
        hosts = []

        # Create the two spine switches
        spines.append(self.addSwitch('s1'))
        spines.append(self.addSwitch('s2'))
        spines.append(self.addSwitch('s3'))
        spines.append(self.addSwitch('s4'))

        # Create two links between the spine switches
        self.addLink(spines[0], spines[1])
        self.addLink(spines[1], spines[2])
        self.addLink(spines[2], spines[0])
        self.addLink(spines[1], spines[3])
        self.addLink(spines[2], spines[3])

        
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        self.addLink(h1, spines[0])
        self.addLink(h2, spines[3])

topos = { 'tower': TowerTopo }

def run():
    topo = TowerTopo()
    net = Mininet( topo=topo, controller=RemoteController, autoSetMacs=True )
    net.start()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
