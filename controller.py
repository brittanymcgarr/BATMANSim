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
            return True

    # Clear the network of current user nodes
    def clear(self):
        self.network.clear()
        self.lostOGMs = []

    # Report an array of IPs in the network
    def report(self):
        return self.network.keys()

    # Time step function for going through each user in the net and performing transportation
    def tick(self, deltaTime):
        timeDiff = 0
        # All actions performed by controller for each step in time
        while deltaTime > 0:
            deltaTime -= 1
            timeDiff += 1

            # Call user node tick functions
            for each in self.network:
                each.tick(timeDiff)

            # Generate OGMs for those that have met their time to cast
            for each in self.network:
                each.broadcastOGMs(timeDiff)

            # Transport one of the generated OGMs to their next hops
            for each in self.network:
                if len(each.sendQueue) > 0:
                    ogm = each.sendQueue.pop(0)

                    # Check the network for a valid IP corresponding to next hop
                    if ogm.nextHop in self.network:
                        destination = self.network[ogm.nextHop]
                        destination.receiveQueue.append(ogm)
                    else:
                        self.lostOGMs.append(ogm)

            # Retrieve an OGM from each user's receive queue
            for each in self.network:
                each.receiveOGM()


# Debugging
if __name__ == '__main__':
    testUser = user.User("0.0.0.1")
    testUser2 = user.User("0.0.0.2")
    testUser3 = user.User("0.0.0.3")
    controller = Controller()
    controller.addUser(testUser)
    print controller.network.keys()
    controller.addUser(testUser2)
    print controller.network.keys()
    controller.addUser(testUser3)
    print controller.network.keys()