#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='10.0.1.101/24', defaultRoute="h1-eth0")
    h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='10.0.2.102/24', defaultRoute="h2-eth0")
    h3 = self.addHost('h3',mac='00:00:00:00:00:03',ip='10.0.3.103/24', defaultRoute="h3-eth0")
    srvr1 = self.addHost('srvr1',mac='00.00.00.00.00.04',ip='10.0.4.104/24',defaultRoute="srvr1-eth0")
    uTH1 = self.addHost('uTH1',mac='00:00:00:00:00:05',ip='128.114.50.10/24', defaultRoute="uTH1-eth0")
    
    # Create a switch. No changes here from Lab 1.
    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    s3 = self.addSwitch('s3')
    center4 = self.addSwitch('center4')
    core5 = self.addSwitch('core5')
    
    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    self.addLink(s1,h1, port1=8, port2=0)
    self.addLink(s2,h2, port1=9, port2=0)
    self.addLink(s3,h3, port1=10, port2=0)
    self.addLink(center4,srvr1, port1=11, port2=0)
    self.addLink(core5, uTH1, port1=99, port2=0)
    self.addLink(s1,core5)
    self.addLink(s2,core5)
    self.addLink(s3,core5)
    self.addLink(center4,core5)
 
def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller = RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
