'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()


class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")
        
        
    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):
        
        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this 
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)
        
        """ Add your logic here """
	if dpid == '00-00-00-00-00-01':
            # Update the low bandwidth path h1 -> h3
            in_port = 3
            out_port = 1
            
            lb_fm1 = of.ofp_flow_mod()
            lb_fm1.match.in_port = in_port
            lb_fm1.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(lb_fm1)
            
            # Update the low bandwidth path h3 -> h1
            in_port = 1
            out_port = 3
            
            lb_fm2 = of.ofp_flow_mod()
            lb_fm2.match.in_port = in_port
            lb_fm2.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(lb_fm2)
            
            # Update the high bandwidth path h2 -> h3
            in_port = 4
            out_port = 2
            
            hb_fm1 = of.ofp_flow_mod()
            hb_fm1.match.in_port = in_port
            hb_fm1.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(hb_fm1)
            
            # Update the high bandwidth path h3 -> h2
            in_port = 2
            out_port =4
            
            hb_fm2 = of.ofp_flow_mod()
            hb_fm2.match.in_port = in_port
            hb_fm2.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(hb_fm2)
        
        elif dpid == '00-00-00-00-00-02' or dpid == '00-00-00-00-00-03':
            
            # Update the midway path for Switches 2 and 3 
            in_port = 1
            out_port = 2
            
            mid_fm1 = of.ofp_flow_mod()
            mid_fm1.match.in_port = in_port
            mid_fm1.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(mid_fm1)
            
            # Update the midway path for Switches 2 and 3 
            in_port = 2
            out_port = 1
            
            mid_fm2 = of.ofp_flow_mod()
            mid_fm2.match.in_port = in_port
            mid_fm2.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(mid_fm2)
        
        elif dpid == '00-00-00-00-00-04':
            
            # Update the low bandwidth path h1 -> h3
            in_port = 3
            out_port = 1
            
            lb_fm3 = of.ofp_flow_mod()
            lb_fm3.match.in_port = in_port
            lb_fm3.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(lb_fm3)
            
            # Update the low bandwidth path h3 -> h1
            in_port = 1
            out_port = 3
            
            lb_fm4 = of.ofp_flow_mod()
            lb_fm4.match.in_port = in_port
            lb_fm4.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(lb_fm4)
            
            # Update the high bandwidth path h2 -> h3
            in_port = 4
            out_port = 2
            
            hb_fm3 = of.ofp_flow_mod()
            hb_fm3.match.in_port = in_port
            hb_fm3.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(hb_fm3)
            
            # Update the high bandwidth path h3 -> h2
            in_port = 2
            out_port =4
            
            hb_fm4 = of.ofp_flow_mod()
            hb_fm4.match.in_port = in_port
            hb_fm4.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(hb_fm4)
            
        

        

def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
