################################################################################
# ogm.py                                                                       #
# Class for containing the BATMAN Simulated OGM packets for neighbor discovery #
# and forwarding. The OGM is traditionally a 52-byte header containing the IP  #
# address of the originating node, the IP address of the last forwarding node, #
# a sequence number generated when the originator enters the network and upda- #
# ted at each round of sending, and a Time-To-Live (TTL) that decrements with  #
# each time step.                                                              #
#                                                                              #
# Brittany McGarr                                                              #
# CPE 400 Computer Networking Fall 2015                                        #
################################################################################


class OGM:
    # Constructor
    def __init__(self, origIP = "0.0.0.0", sendIP = "0.0.0.0", nextHop = "0.0.0.0", seq = 0,
                 ttl = 0, direction = False):
        self.originatorIP = origIP
        self.senderIP = sendIP
        self.nextHop = nextHop
        self.sequence = seq
        self.TTL = ttl
        self.directional = direction
