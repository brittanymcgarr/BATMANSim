################################################################################
# controller.py                                                                #
# Main controller of the network for simulated BATMAN. Creates the user nodes, #
# adds to the listing, and performs transportations between lines. Interfaces  #
# with the view class to display data.                                         #
#                                                                              #
# Brittany McGarr                                                              #
# CPE 400 Computer Networking Fall 2015                                        #
################################################################################


import ogm
import user


class Controller:
    # Constructor
    def __init__(self):
        # Network will be a dictionary referenced by IP addresses
        self.network = {}
        self.lostOGMs = []

    # Add users to the network based on given user node
    def addUser(self, newUser):
        # Check that the user is unique
        if newUser.IP in self.network.keys():
            return False
        else:
            self.network[newUser.IP] = newUser
            self.updateNetwork()
            return True

    # Remove user from the network
    def removeUser(self, exitUser):
        # Check if the prompted user is in the network and proceed
        if exitUser.IP in self.network.keys():
            del self.network[exitUser.IP]
            self.updateNetwork()

    # Update the all net dictionary of each node when a new node enters
    def updateNetwork(self):
        for key, value in self.network.iteritems():
            value.allNet = self.network

    # Clear the network of current user nodes
    def clear(self):
        self.network.clear()
        self.lostOGMs = []

    # Report an array of IPs in the network
    def report(self):
        return self.network.keys()

    # Report a string of current IPs and OGMs in the system
    def reportString(self):
        report = "Network:\n"

        for key, value in self.network.iteritems():
            report += "IP: " + str(key) + "\n"

        report += "\nLost OGMS:\n"
        for index in self.lostOGMs:
            report += "OGM source IP: " + str(index.senderIP) + "Sequence: " + str(index.sequence) + "\n"

        return report

    # Time step function for going through each user in the net and performing transportation
    def tick(self, deltaTime):
        timeDiff = 0
        # All actions performed by controller for each step in time
        while deltaTime > 0:
            # Call user node tick functions
            for key, value in self.network.iteritems():
                value.tick(timeDiff)

            deltaTime -= 1
            timeDiff += 1

            if deltaTime > 0:
                # Generate OGMs for those that have met their time to cast
                for key, value in self.network.iteritems():
                    value.broadcastOGMs(timeDiff)

            deltaTime -= 1
            timeDiff += 1

            if deltaTime > 0:
                # Transport one of the generated OGMs to their next hops from each node
                for key, value in self.network.iteritems():
                    if len(value.sendQueue) > 0:
                        outgoingOGM = value.sendQueue.pop(0)
                        # Check the network for a valid IP corresponding to next hop
                        if outgoingOGM.nextHop in self.network.keys():
                            destination = self.network[outgoingOGM.nextHop]
                            destination.receiveQueue.append(outgoingOGM)
                        else:
                            self.lostOGMs.append(outgoingOGM)

            deltaTime -= 1
            timeDiff += 1

            if deltaTime > 0:
                # Retrieve an OGM from each user's receive queue
                for key, value in self.network.iteritems():
                    value.receiveOGM()
