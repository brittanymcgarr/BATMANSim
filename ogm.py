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
    def __init__(self, origIP="0.0.0.0", sendIP="0.0.0.0", nextHop="0.0.0.0", seq=0,
                 ttl=10, direction=False, payload=""):
        self.originatorIP = origIP
        self.senderIP = sendIP
        self.nextHop = nextHop
        self.sequence = seq
        self.TTL = ttl
        self.directional = direction
        self.traceroute = [self.senderIP]
        self.data = payload

    # Report the OGM to a string
    def reportString(self):
        oIP = "Originator IP: " + str(self.originatorIP) + "\n"
        sendIP = "Sender IP: " + str(self.senderIP) + "\n"
        nHop = "Next hop: " + str(self.nextHop) + "\n"
        seq = "Sequence Number: " + str(self.sequence) + "\n"
        ttl = "TTL: " + str(self.TTL) + "\n"
        direction = "Uni-Directional? " + str(self.directional) + "\n\n"

        return oIP + sendIP + nHop + seq + ttl + direction
