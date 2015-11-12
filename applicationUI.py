################################################################################
# applicationUI.py                                                             #
# Graphic User Interface (GUI) for the BATMAN Simulator. Creates and manages   #
# nodes and controller as directed by the user. Options include creating and   #
# initializing the node neighbors, displaying the network, displaying node     #
# values, running the controller, defining time steps, and allowing customized #
# node options such as simulating IP spoofing. Users may click to expand the   #
# OGM or node text, and time step narratives are displayed for reporting.      #
#                                                                              #
# Brittany McGarr                                                              #
# CPE 400 Computer Networking Fall 2015                                        #
################################################################################


from Tkinter import *
import controller
import ogm
import user


class ApplicationUI:
    # Constructor - Creates the viewing pane
    def __init__(self):
        # The controller handle
        self.controller = controller.Controller()

        # Create and store the window handle
        self.window = Tk()
        self.window.title("BATMAN Simulator ver 1.0")

        # Frame variables
        # Text field width and height
        console_width = 80
        console_height = 20
        canvas_width = 200
        canvas_height = 200

        # Button sizes
        entry_width = 20
        button_width = 50
        selection_width = 20

        # Display colors and entry fields
        self.colors = ("white", "black", "yellow", "red", "green", "blue", "#0e1927", "#ffd11a", "#00802b")
        self.castTime1_int = IntVar()
        self.castTime2_int = IntVar()
        self.castTime3_int = IntVar()
        self.castTime4_int = IntVar()
        self.neighbor1_str = StringVar()
        self.neighbor2_str = StringVar()
        self.neighbor3_str = StringVar()
        self.neighbor4_str = StringVar()
        self.neighbors_list = []
        self.neighbors1_list = []
        self.neighbors2_list = []
        self.neighbors3_list = []
        self.neighbors4_list = []
        self.timeStep_int = IntVar()

        # Piped messages for display
        self.messagePipe = ["Console Log:\n", ]

        # Create and store the frame handles
        self.left_frame = Frame(width=550, height=75, borderwidth=5)
        self.left_frame.grid(row=0, column=0)
        self.right_frame = Frame(width=550, height=75, borderwidth=5)
        self.right_frame.grid(row=0, column=1)
        self.foot_frame = Frame(width=1000, height=50, borderwidth=5)
        self.foot_frame.grid(row=1, column=0, columnspan=2)

        # Create the menu handle and populate with sub-menus
        self.menu = Menu(self.window)
        self.file_menu = Menu(self.menu)
        self.help_menu = Menu(self.menu)
        self.window.config(menu=self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.clearNetwork)
        self.file_menu.add_command(label="Open", command=self.loadNetwork)
        self.file_menu.add_command(label="Save", command=self.saveNetwork)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.window.quit)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="User Manual", command=self.showManual)

        # Create the console and canvas handles
        self.console = Text(self.right_frame, width=console_width, height=console_height,
                            background=self.colors[6], foreground=self.colors[0])
        self.console_scrollbar = Scrollbar(self.right_frame, command=self.console.yview)
        self.canvas = Canvas(self.foot_frame, width=canvas_width, height=canvas_height)
        self.print_button = Button(self.right_frame, text="Report Console", width=entry_width, command=self.printConsole)

        # Create the node button widgets
        self.node1_button = Button(self.left_frame, text="User Node 1", width=button_width, command=self.displayUserInput1)
        self.node2_button = Button(self.left_frame, text="User Node 2", width=button_width, command=self.displayUserInput2)
        self.node3_button = Button(self.left_frame, text="User Node 3", width=button_width, command=self.displayUserInput3)
        self.node4_button = Button(self.left_frame, text="User Node 4", width=button_width, command=self.displayUserInput4)

        # Create the entry and label widgets for IP addressing
        self.ip1_label = Label(self.left_frame, text="IP:", width=entry_width)
        self.ip1_entry = Entry(self.left_frame, width=entry_width)
        self.ip1_entry.insert(0, "0.0.0.0")

        self.ip2_label = Label(self.left_frame, text="IP:", width=entry_width)
        self.ip2_entry = Entry(self.left_frame, width=entry_width)
        self.ip2_entry.insert(0, "0.0.0.1")

        self.ip3_label = Label(self.left_frame, text="IP:", width=entry_width)
        self.ip3_entry = Entry(self.left_frame, width=entry_width)
        self.ip3_entry.insert(0, "0.0.0.2")

        self.ip4_label = Label(self.left_frame, text="IP:", width=entry_width)
        self.ip4_entry = Entry(self.left_frame, width=entry_width)
        self.ip4_entry.insert(0, "0.0.0.3")

        # Create the entry and label widgets for broadcast times
        self.castTime1_label = Label(self.left_frame, text="Broadcast Time:", width=entry_width)
        self.castTime1_entry = Entry(self.left_frame, width=entry_width, textvariable=self.castTime1_int)

        self.castTime2_label = Label(self.left_frame, text="Broadcast Time:", width=entry_width)
        self.castTime2_entry = Entry(self.left_frame, width=entry_width, textvariable=self.castTime2_int)

        self.castTime3_label = Label(self.left_frame, text="Broadcast Time:", width=entry_width)
        self.castTime3_entry = Entry(self.left_frame, width=entry_width, textvariable=self.castTime3_int)

        self.castTime4_label = Label(self.left_frame, text="Broadcast Time:", width=entry_width)
        self.castTime4_entry = Entry(self.left_frame, width=entry_width, textvariable=self.castTime4_int)

        # Create the neighbor listbox selections
        self.neighbor1_label = Label(self.left_frame, text="Neighbors:", width=entry_width)
        self.neighbor2_label = Label(self.left_frame, text="Neighbors:", width=entry_width)
        self.neighbor3_label = Label(self.left_frame, text="Neighbors:", width=entry_width)
        self.neighbor4_label = Label(self.left_frame, text="Neighbors:", width=entry_width)
        self.neighbor1_om = OptionMenu(self.left_frame, self.neighbor1_str, self.neighbors_list)
        self.neighbor2_om = OptionMenu(self.left_frame, self.neighbor2_str, self.neighbors_list)
        self.neighbor3_om = OptionMenu(self.left_frame, self.neighbor3_str, self.neighbors_list)
        self.neighbor4_om = OptionMenu(self.left_frame, self.neighbor4_str, self.neighbors_list)

        # Create the submission buttons
        self.addNbr1_button = Button(self.left_frame, text="Add Neighbor", width=selection_width, command=self.addNeighbor1)
        self.addNbr2_button = Button(self.left_frame, text="Add Neighbor", width=selection_width, command=self.addNeighbor2)
        self.addNbr3_button = Button(self.left_frame, text="Add Neighbor", width=selection_width, command=self.addNeighbor3)
        self.addNbr4_button = Button(self.left_frame, text="Add Neighbor", width=selection_width, command=self.addNeighbor4)
        self.add1_button = Button(self.left_frame, text="Add Node", width=selection_width, command=self.addUser1)
        self.add2_button = Button(self.left_frame, text="Add Node", width=selection_width, command=self.addUser2)
        self.add3_button = Button(self.left_frame, text="Add Node", width=selection_width, command=self.addUser3)
        self.add4_button = Button(self.left_frame, text="Add Node", width=selection_width, command=self.addUser4)

        # Create the simulation time entry and start simulation buttons
        self.timeStep_label = Label(self.left_frame, text="Run Time:", width=entry_width)
        self.timeStep_entry = Entry(self.left_frame, width=entry_width, textvariable=self.timeStep_int)
        self.start_button = Button(self.left_frame, text="Start Simulation", width=selection_width, command=self.runNetwork)
        self.report_button = Button(self.left_frame, text="Show Network", width=selection_width, command=self.reportConsole)

        # Add the widgets to the grid
        # Console
        self.console.grid(row=0, column=0)
        self.console_scrollbar.grid(row=0, column=1, sticky=N+S)
        self.console_scrollbar.config(command=self.console.yview)
        self.console.config(yscrollcommand=self.console_scrollbar.set)
        self.console.insert(END, self.messagePipe[0])
        self.print_button.grid(row=1, column=0, columnspan=2)

        # Node Buttons (Initial state)
        self.node1_button.grid(row=0, column=0, columnspan=2)
        self.node2_button.grid(row=1, column=0, columnspan=2)
        self.node3_button.grid(row=2, column=0, columnspan=2)
        self.node4_button.grid(row=3, column=0, columnspan=2)

        # Time step widgets
        self.timeStep_label.grid(row=4, column=0)
        self.timeStep_entry.grid(row=4, column=1)
        self.start_button.grid(row=5, column=0)
        self.report_button.grid(row=5, column=1)

    # Add a constructed user node to the system
    def addUser1(self):
        newUser = user.User(ip=self.ip1_entry.get(), castTime=self.castTime1_int.get())
        newUser.neighbors = self.neighbors1_list
        if self.controller.addUser(newUser):
            self.neighbors_list.append(newUser.IP)

    def addUser2(self):
        newUser = user.User(ip=self.ip2_entry.get(), castTime=self.castTime2_int.get())
        newUser.neighbors = self.neighbors2_list
        if self.controller.addUser(newUser):
            self.neighbors_list.append(newUser.IP)

    def addUser3(self):
        newUser = user.User(ip=self.ip3_entry.get(), castTime=self.castTime3_int.get())
        newUser.neighbors = self.neighbors3_list
        if self.controller.addUser(newUser):
            self.neighbors_list.append(newUser.IP)

    def addUser4(self):
        newUser = user.User(ip=self.ip4_entry.get(), castTime=self.castTime4_int.get())
        newUser.neighbors = self.neighbors4_list
        if self.controller.addUser(newUser):
            self.neighbors_list.append(newUser.IP)

    # Remove a user node from the system
    def removeUser(self):
        return True # STUB

    # Add a neighbor from a drop down listing
    def addNeighbor1(self):
        if self.neighbor1_str.get() in self.controller.network.keys():
            self.neighbors1_list.append(self.controller.network[self.neighbor1_str.get()])

    def addNeighbor2(self):
        if self.neighbor2_str.get() in self.controller.network.keys():
            self.neighbors2_list.append(self.controller.network[self.neighbor2_str.get()])

    def addNeighbor3(self):
        if self.neighbor3_str.get() in self.controller.network.keys():
            self.neighbors3_list.append(self.controller.network[self.neighbor3_str.get()])

    def addNeighbor4(self):
        if self.neighbor4_str.get() in self.controller.network.keys():
            self.neighbors4_list.append(self.controller.network[self.neighbor4_str.get()])

    # Remove a neighbor from the node
    def removeNeighbor(self):
        return True # STUB

    # Clear the network and restart
    def clearNetwork(self):
        self.controller.clear()

    # Print a report of the console log to a file
    def printConsole(self):
        fileOUT = open("report.txt", "w")
        for line in self.messagePipe:
            if not isinstance(line, basestring):
                outLine = ", ".join(line)
                fileOUT.write(outLine)
            else:
                fileOUT.write(line)
            fileOUT.write("\n")
        fileOUT.close()

    # Show the network state in the console
    def reportConsole(self):
        self.messagePipe.append(self.controller.report())
        self.console.insert(END, self.messagePipe[-1])
        self.messagePipe.append("\n")
        self.console.insert(END, self.messagePipe[-1])
        self.console.yview(END)

    # Save the current configuration to a file
    def saveNetwork(self):
        return True # STUB

    # Load a network configuration from a file
    def loadNetwork(self):
        return True # STUB

    # Draw the network in a canvas
    def drawNetwork(self):
        return True # STUB

    # Run the program for the specified time
    def runNetwork(self):
        if self.timeStep_int.get() > 0:
            self.controller.tick(self.timeStep_int.get())

    # User node drop down function displays
    def displayUserInput1(self):
        self.node1_button.grid(row=0, column=0, columnspan=2)
        self.ip1_label.grid(row=1, column=0)
        self.ip1_entry.grid(row=1, column=1)
        self.castTime1_label.grid(row=2, column=0)
        self.castTime1_entry.grid(row=2, column=1)
        self.neighbor1_label.grid(row=3, column=0)
        self.neighbor1_om.grid(row=3, column=1)
        self.addNbr1_button.grid(row=4, column=0)
        self.add1_button.grid(row=4, column=1)
        self.node2_button.grid(row=5, column=0, columnspan=2)
        self.hideUserInput1()
        self.node3_button.grid(row=6, column=0, columnspan=2)
        self.node4_button.grid(row=7, column=0, columnspan=2)
        self.timeStep_label.grid(row=8, column=0)
        self.timeStep_entry.grid(row=8, column=1)
        self.start_button.grid(row=9, column=0)
        self.report_button.grid(row=9, column=1)

    def displayUserInput2(self):
        self.node1_button.grid(row=0, column=0, columnspan=2)
        self.hideUserInput2()
        self.node2_button.grid(row=1, column=0, columnspan=2)
        self.ip2_label.grid(row=2, column=0)
        self.ip2_entry.grid(row=2, column=1)
        self.castTime2_label.grid(row=3, column=0)
        self.castTime2_entry.grid(row=3, column=1)
        self.neighbor2_label.grid(row=4, column=0)
        self.neighbor2_om.grid(row=4, column=1)
        self.addNbr2_button.grid(row=5, column=0)
        self.add2_button.grid(row=5, column=1)
        self.node3_button.grid(row=6, column=0, columnspan=2)
        self.node4_button.grid(row=7, column=0, columnspan=2)
        self.timeStep_label.grid(row=8, column=0)
        self.timeStep_entry.grid(row=8, column=1)
        self.start_button.grid(row=9, column=0)
        self.report_button.grid(row=9, column=1)

    def displayUserInput3(self):
        self.node1_button.grid(row=0, column=0, columnspan=2)
        self.hideUserInput3()
        self.node2_button.grid(row=1, column=0, columnspan=2)
        self.node3_button.grid(row=2, column=0, columnspan=2)
        self.ip3_label.grid(row=3, column=0)
        self.ip3_entry.grid(row=3, column=1)
        self.castTime3_label.grid(row=4, column=0)
        self.castTime3_entry.grid(row=4, column=1)
        self.neighbor3_label.grid(row=5, column=0)
        self.neighbor3_om.grid(row=5, column=1)
        self.addNbr3_button.grid(row=6, column=0)
        self.add3_button.grid(row=6, column=1)
        self.node4_button.grid(row=7, column=0, columnspan=2)
        self.timeStep_label.grid(row=8, column=0)
        self.timeStep_entry.grid(row=8, column=1)
        self.start_button.grid(row=9, column=0)
        self.report_button.grid(row=9, column=1)

    def displayUserInput4(self):
        self.node1_button.grid(row=0, column=0, columnspan=2)
        self.hideUserInput4()
        self.node2_button.grid(row=1, column=0, columnspan=2)
        self.node3_button.grid(row=2, column=0, columnspan=2)
        self.node4_button.grid(row=3, column=0, columnspan=2)
        self.ip4_label.grid(row=4, column=0)
        self.ip4_entry.grid(row=4, column=1)
        self.castTime4_label.grid(row=5, column=0)
        self.castTime4_entry.grid(row=5, column=1)
        self.neighbor4_label.grid(row=6, column=0)
        self.neighbor4_om.grid(row=6, column=1)
        self.addNbr4_button.grid(row=7, column=0)
        self.add4_button.grid(row=7, column=1)
        self.timeStep_label.grid(row=8, column=0)
        self.timeStep_entry.grid(row=8, column=1)
        self.start_button.grid(row=9, column=0)
        self.report_button.grid(row=9, column=1)

    # Clear the node input display for the specified node
    def hideUserInput1(self):
        self.ip2_label.grid_forget()
        self.ip2_entry.grid_forget()
        self.castTime2_label.grid_forget()
        self.castTime2_entry.grid_forget()
        self.neighbor2_label.grid_forget()
        self.neighbor2_om.grid_forget()
        self.addNbr2_button.grid_forget()
        self.add2_button.grid_forget()
        self.ip3_label.grid_forget()
        self.ip3_entry.grid_forget()
        self.castTime3_label.grid_forget()
        self.castTime3_entry.grid_forget()
        self.neighbor3_label.grid_forget()
        self.neighbor3_om.grid_forget()
        self.addNbr3_button.grid_forget()
        self.add3_button.grid_forget()
        self.ip4_label.grid_forget()
        self.ip4_entry.grid_forget()
        self.castTime4_label.grid_forget()
        self.castTime4_entry.grid_forget()
        self.addNbr4_button.grid_forget()
        self.neighbor4_label.grid_forget()
        self.neighbor4_om.grid_forget()
        self.add4_button.grid_forget()

    def hideUserInput2(self):
        self.ip1_label.grid_forget()
        self.ip1_entry.grid_forget()
        self.castTime1_label.grid_forget()
        self.castTime1_entry.grid_forget()
        self.neighbor1_label.grid_forget()
        self.neighbor1_om.grid_forget()
        self.addNbr1_button.grid_forget()
        self.add1_button.grid_forget()
        self.ip3_label.grid_forget()
        self.ip3_entry.grid_forget()
        self.castTime3_label.grid_forget()
        self.castTime3_entry.grid_forget()
        self.neighbor3_label.grid_forget()
        self.neighbor3_om.grid_forget()
        self.addNbr3_button.grid_forget()
        self.add3_button.grid_forget()
        self.ip4_label.grid_forget()
        self.ip4_entry.grid_forget()
        self.castTime4_label.grid_forget()
        self.castTime4_entry.grid_forget()
        self.neighbor4_label.grid_forget()
        self.neighbor4_om.grid_forget()
        self.addNbr4_button.grid_forget()
        self.add4_button.grid_forget()

    def hideUserInput3(self):
        self.ip1_label.grid_forget()
        self.ip1_entry.grid_forget()
        self.castTime1_label.grid_forget()
        self.castTime1_entry.grid_forget()
        self.neighbor1_label.grid_forget()
        self.neighbor1_om.grid_forget()
        self.addNbr1_button.grid_forget()
        self.add1_button.grid_forget()
        self.ip2_label.grid_forget()
        self.ip2_entry.grid_forget()
        self.castTime2_label.grid_forget()
        self.castTime2_entry.grid_forget()
        self.neighbor2_label.grid_forget()
        self.neighbor2_om.grid_forget()
        self.addNbr2_button.grid_forget()
        self.add2_button.grid_forget()
        self.ip4_label.grid_forget()
        self.ip4_entry.grid_forget()
        self.castTime4_label.grid_forget()
        self.castTime4_entry.grid_forget()
        self.neighbor4_label.grid_forget()
        self.neighbor4_om.grid_forget()
        self.addNbr4_button.grid_forget()
        self.add4_button.grid_forget()

    def hideUserInput4(self):
        self.ip1_label.grid_forget()
        self.ip1_entry.grid_forget()
        self.castTime1_label.grid_forget()
        self.castTime1_entry.grid_forget()
        self.neighbor1_label.grid_forget()
        self.neighbor1_om.grid_forget()
        self.addNbr1_button.grid_forget()
        self.add1_button.grid_forget()
        self.ip2_label.grid_forget()
        self.ip2_entry.grid_forget()
        self.castTime2_label.grid_forget()
        self.castTime2_entry.grid_forget()
        self.neighbor2_label.grid_forget()
        self.neighbor2_om.grid_forget()
        self.addNbr2_button.grid_forget()
        self.add2_button.grid_forget()
        self.ip3_label.grid_forget()
        self.ip3_entry.grid_forget()
        self.castTime3_label.grid_forget()
        self.castTime3_entry.grid_forget()
        self.neighbor3_label.grid_forget()
        self.neighbor3_om.grid_forget()
        self.addNbr3_button.grid_forget()
        self.add3_button.grid_forget()

    # Show the user manual
    def showManual(self):
        return True # STUB

# Debugging
if __name__ == '__main__':
    app = ApplicationUI()
    mainloop()