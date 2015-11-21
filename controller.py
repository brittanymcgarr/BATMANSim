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
import time


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
                # Retrieve an OGM from each user's receive queue
                for key, value in self.network.iteritems():
                    value.receiveOGM()

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


# Debugging - Test system and report directly to file
if __name__ == '__main__':
    controller = Controller()
    user1 = user.User(ip="192.164.0.1", castTime=5)
    user2 = user.User(ip="192.164.0.2", castTime=5)
    user3 = user.User(ip="192.164.0.3", castTime=5)

    user1.neighbors.append(user2)
    user2.neighbors.append(user1)
    user3.neighbors.append(user2)

    controller.addUser(user1)
    controller.addUser(user2)
    controller.addUser(user3)

    messages = []

    messages.append("\n\nRun Time: 6000 msec\n\n")
    controller.tick(60)
    messages.append(controller.reportString())

    for node in controller.network:
        messages.append(controller.network[node].reportString())

    fileOUT = open("report" + "_" + time.strftime("%d%m%Y%H%M"), "w")

    for line in messages:
        if not isinstance(line, basestring):
            outLine = ", ".join(line)
            fileOUT.write(outLine)
        else:
            fileOUT.write(line)

        fileOUT.write("\n")

    fileOUT.close()
