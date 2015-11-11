################################################################################
# user.py                                                                      #
# Class for representing user nodes on the BATMAN Simulator. Each user has an  #
# IP, a listing of nearest neighbors, individual broadcast times, directions   #
# of links (one-way or bi-directional), and queues for sending and receiving   #
# OGMs and packets.                                                            #
#                                                                              #
# Brittany McGarr                                                              #
# CPE 400 Computer Networking Fall 2015                                        #
################################################################################


import ogm as ogm


class User:
    # Constructor method
    def __init__(self, ip = "0.0.0.0", castTime = 1, direction = False):
        self.IP = ip
        self.allNet = {}
        self.neighbors = []
        self.broadcastTime = castTime
        self.timeToCast = 0
        self.directional = direction
        self.sendQueue = []
        self.receiveQueue = []
        self.queueLimit = 1000
        self.receivedOGMs = {}
        self.sequence = 0
        self.keepAlive = 10

    # Create and broadcast OGMs to all neighbors
    def broadcastOGMs(self, deltaTime):
        # Check for the broadcast time and broadcast if timestep is reached
        if deltaTime >= self.broadcastTime:
            # Create an OGM for each neighbor and place in the send queue
            outgoingOGM = ogm.OGM(origIP = self.IP, sendIP = self.IP, seq = self.sequence,
                                  ttl = self.keepAlive, direction = self.directional)
            for count in range(0, len(self.neighbors)):
                self.sendQueue.append(outgoingOGM)

            # Increment the sequence number
            self.sequence += 1

    # Receive the first OGM from the queue and populate neighbors
    def receiveOGM(self):
        if len(self.receivedOGMs) > 0:
            ogm = self.receivedOGMs.pop(0)

            # Check for self-returning OGMs and uni-directional communication (ver 0.2)
            if ogm.senderIP == self.IP or ogm.directional:
                return False

            # Check the originator and sender IPs
            if ogm.originatorIP == ogm.senderIP and ogm.originatorIP:
                # If they matched, the OGM goes directly to a neighbor, check the list
                found = False
                for index in self.neighbors:
                    if index.IP == ogm.originatorIP:
                        found = True

                # If the found flag was not triggered, a new neighbor was detected
                if not found:
                    self.neighbors.append(self.allNet[ogm.originatorIP])

            # Check the received OGMs if this is the latest sequence number
            if self.receivedOGMs[ogm.originatorIP].sequence > ogm.sequence:
                return False
            else:
                self.receivedOGMs[ogm.originatorIP] = ogm

            # Additionally, this OGM must be forwarded through the network
            ogm.TTL -= 1

            # Check for a live packet
            if ogm.TTL > 0:
                # Replace the sender's IP with the current user's and broadcast
                ogm.senderIP = self.IP
                ogm.directional = self.directional

                for index in self.neighbors:
                    if ogm.originatorIP is not index.IP:
                        self.sendQueue.append(ogm)
