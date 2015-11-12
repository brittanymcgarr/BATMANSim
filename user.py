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
        # All network nodes convention: <key>IP : <value> User instance
        self.allNet = {}
        # Neighbors convention: User instances
        self.neighbors = []
        self.broadcastTime = castTime
        self.timeToCast = 0
        self.directional = direction
        # Send and receive queues should have OGM or packet (datagram)
        self.sendQueue = []
        self.receiveQueue = []
        self.queueLimit = 1000
        # Received OGMs convention: <key>IP : <value> User instance
        self.receivedOGMs = {}
        self.sequence = 0
        self.keepAlive = 10

    # Create and broadcast OGMs for all neighbors and stick in send queue
    def broadcastOGMs(self, deltaTime):
        # Check for the broadcast time and broadcast if time step is reached
        self.timeToCast += deltaTime

        # Create an OGM for each neighbor and place in the send queue
        if self.timeToCast >= self.broadcastTime:
            outgoingOGM = ogm.OGM(origIP = self.IP, sendIP = self.IP, seq = self.sequence,
                                  ttl = self.keepAlive, direction = self.directional)
            for neighbor in self.neighbors:
                outgoingOGM.nextHop = neighbor.IP
                self.sendQueue.append(outgoingOGM)

            # Increment the sequence number
            self.sequence += 1

            # Reset the Time to Cast
            self.timeToCast = 0

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
                        ogm.nextHop = index.IP
                        self.sendQueue.append(ogm)

    # Add unique neighbor to the user's listing (used for initial state and for altering in GUI)
    def addNeighbor(self, neighbor):
        found = False
        for each in self.neighbors:
            if each.IP == neighbor.IP:
                found = True

        if not found:
            self.neighbors.append(neighbor)

    # Remove a neighbor from the listing
    def removeNeighbor(self, neighbor):
        self.neighbors.remove(neighbor)

    # Time step function for keeping queues and OGMs
    def tick(self, deltaTime):
        # Update the send and receive queues
        for each in self.sendQueue:
            each.TTL -= deltaTime
            if each.TTL <= 0:
                self.sendQueue.remove(each)

        for each in self.receiveQueue:
            each.TTL -= deltaTime
            if each.TTL <= 0:
                self.receiveQueue.remove(each)

        for each in self.receivedOGMs:
            each.TTL -= deltaTime
            if each.TTL <= 0:
                ip = each.originatorIP
                for neighbor in self.neighbors:
                    if neighbor.IP == ip:
                        self.neighbors.remove(neighbor)