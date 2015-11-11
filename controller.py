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
