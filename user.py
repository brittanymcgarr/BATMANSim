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
import time


class User:
    # Constructor method
    def __init__(self, ip="0.0.0.0", castTime=1, direction=False):
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

        # Received OGMs convention: <key>IP : <value> OGM instance
        self.receivedOGMs = {}
        self.sequence = 0
        self.keepAlive = 180

    # Create and broadcast OGMs for all neighbors and stick in send queue
    def broadcastOGMs(self, deltaTime):
        # Check for the broadcast time and broadcast if time step is reached
        self.timeToCast += deltaTime

        # Create an OGM for each neighbor and place in the send queue
        if self.timeToCast % self.broadcastTime == 0:
            for neighbor in self.neighbors:
                outgoingOGM = ogm.OGM(origIP=self.IP, sendIP=self.IP, seq=self.sequence,
                                      ttl=self.keepAlive, direction=self.directional)
                outgoingOGM.nextHop = neighbor.IP
                self.sendQueue.append(outgoingOGM)

            # Increment the sequence number
            self.sequence += 1

            # Reset the Time to Cast
            self.timeToCast = 0

    # Receive the first OGM from the queue and populate neighbors
    def receiveOGM(self):
        if len(self.receiveQueue) > 0:
            incomingOGM = self.receiveQueue.pop(0)

            # Check for self-returning OGMs and uni-directional communication (ver 0.2)
            if incomingOGM.senderIP == self.IP or incomingOGM.directional:
                return False

            # Update the trace route listing (just IP address)
            incomingOGM.traceroute.append(self.IP)

            # Check the originator and sender IPs
            if incomingOGM.originatorIP == incomingOGM.senderIP:
                # If they matched, the OGM goes directly to a neighbor, check the list
                found = False
                for index in self.neighbors:
                    if index.IP == incomingOGM.originatorIP:
                        found = True

                # If the found flag was not triggered, a new neighbor was detected
                if not found:
                    self.neighbors.append(self.allNet[incomingOGM.originatorIP])

            # Check the received OGMs if this is the latest sequence number
            if incomingOGM.originatorIP in self.receivedOGMs.keys():
                if self.receivedOGMs[incomingOGM.originatorIP].sequence > incomingOGM.sequence:
                    return False
                else:
                    self.receivedOGMs[incomingOGM.originatorIP] = incomingOGM
            else:
                self.receivedOGMs[incomingOGM.originatorIP] = incomingOGM

            # Additionally, this OGM must be forwarded through the network
            incomingOGM.TTL -= 1

            # Check for a live packet
            if incomingOGM.TTL > 0:
                # Replace the sender's IP with the current user's and broadcast
                incomingOGM.senderIP = self.IP
                incomingOGM.directional = self.directional

                for index in self.neighbors:
                    if incomingOGM.originatorIP is not index.IP:
                        outgoingOGM = incomingOGM
                        outgoingOGM.nextHop = index.IP
                        self.sendQueue.append(outgoingOGM)

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

    # Report current state to string
    def reportString(self):
        ip = "IP: " + str(self.IP) + "\n"
        bct = "OGM Interval Time: " + str(self.broadcastTime) + "\n"
        direction = "Uni-Directional Link: " + str(self.directional) + "\n"
        seq = "Sequence: " + str(self.sequence) + "\n"

        # Report IPs of neighbors
        totNeighbors = "Neighbors: "
        for neighbor in self.neighbors:
            totNeighbors += str(neighbor.IP) + " "
        totNeighbors += "\n"

        # Report Send queue
        totSending = "Send Queue:\n"
        for send in self.sendQueue:
            totSending += "Sequence: " + str(send.sequence) + " "
        totSending += "\n"

        # Report Receive Queue
        totReceiving = "Received Queue:\n"
        for receipt in self.receiveQueue:
            totReceiving += "Sender: " + str(receipt.senderIP) + " Sequence: " \
                            + str(receipt.sequence) + "\n"
        totReceiving += "\n"

        # Repeat for OGMs
        totOGMs = "Network Topology: "
        for ogmIndex in self.receivedOGMs:
            totOGMs += str(self.receivedOGMs[ogmIndex].originatorIP) + " "
        totOGMs += "\n\n"

        return ip + bct + direction + seq + totNeighbors + totSending + totReceiving + totOGMs

    # The sequel of the hit action film: reportString()
    def reportFile(self):
        fileOUT = open(str(self.IP) + "_" + time.strftime("%d%m%Y"), "w")

        ip = "IP: " + str(self.IP) + "\n"
        fileOUT.write(ip)
        bct = "Broadcast Time: " + str(self.broadcastTime) + "\n"
        fileOUT.write(bct)
        direction = "Bi-Directional Link: " + str(self.directional) + "\n"
        fileOUT.write(direction)
        seq = "Sequence: " + str(self.sequence) + "\n"
        fileOUT.write(seq)

        # Report IPs of neighbors
        totNeighbors = "Neighbors: "
        for neighbor in self.neighbors:
            totNeighbors += str(neighbor.IP) + " "
        totNeighbors += "\n"
        fileOUT.write(totNeighbors)

        # Repeat for OGMs
        totOGMs = "Received OGMs: "
        for ogmIndex in self.receivedOGMs.keys():
            totOGMs += str(ogmIndex) + " "
        totOGMs += "\n"
        fileOUT.write(totOGMs)

        fileOUT.close()

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

        for key, value in self.receivedOGMs.iteritems():
            value.TTL -= deltaTime
            if value.TTL <= 0:
                ip = value.originatorIP
                for neighbor in self.neighbors:
                    if neighbor.IP == ip:
                        self.neighbors.remove(neighbor)
