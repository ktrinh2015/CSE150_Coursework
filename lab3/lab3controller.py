# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, EthAddr
import pox.lib.packet as pkt

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection
    
    self.macToPort = {}
    # This binds our PacketIn event listener
    connection.addListeners(self)
  
  def flood (self, packet_in):
    msg = of.ofp_packet_out(data = packet_in)
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg)

  def create_rule (self, packet, dest):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.actions.append(of.ofp_action_output(port = dest))
    self.connection.send(msg)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.    
    dest = self.macToPort.get(packet.dst)
    if packet.find('tcp') and packet.find('ipv4'):
       if dest is not None:
          self.create_rule(packet, dest)
       else:
          self.flood(packet_in)
    
  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    self.macToPort[packet.src] = event.port 
    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

  def _handle_ConnectionUp (self, event):
    
     msg = of.ofp_flow_mod()
     msg.priority = 33001 
     if msg.match.nw_proto == 6: 
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        event.connection.send(msg)
      
     msg = of.ofp_flow_mod()
     msg.match.in_port = 1
     msg.priority = 33001
     msg.match.dl_type = 0X0800
     if msg.match.nw_proto == 1:
        msg.match.dl_src = EthAddr("00:00:00:00:00:01")
        msg.match.dl_dst = EthAddr("00:00:00:00:00:04")
        msg.actions.append(of.ofp_action_output(port = 4))
        event.connection.send(msg)
 
     msg = of.ofp_flow_mod()
     msg.match.in_port = 4
     msg.priority = 33001
     msg.match.dl_type = 0X0800
     if msg.match.nw_proto == 1:
        msg.match.dl_src = EthAddr("00:00:00:00:00:04")
        msg.match.dl_dst = EthAddr("00:00:00:00:00:01")
        msg.actions.append(of.ofp_action_output(port = 1))
        event.connection.send(msg)

     msg = of.ofp_flow_mod()
     msg.priority = 50000
     msg.match.dl_type = 0X0806
     msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
     event.connection.send(msg)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
