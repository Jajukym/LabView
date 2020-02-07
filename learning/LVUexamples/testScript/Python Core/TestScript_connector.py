# coding=utf-8


"""
TestScript_connector.py
This is the TestScript simple Python-to-LabVIEW-to-Python
connector module. We seek clear, simple code that allows us to send
messages back and forth. We will use the following python format:
    command|script_id|list of strings
for all messages in either direction. In LabVIEW, this will be
    command|Script ID|array of strings
The json package seamlessly translates from a Python list of strings
to and from a LabVIEW array of strings, so this is a good choice for
the message format. The pipe symbol | will be the separator. 
IMPORTANT: the programmer should never use the pipe symbol inside any
protocols built on top of this framework, nor should the programmer
use any single quotes, double quotes, or triple quotes inside a message.

This module is not responsible for setting up the messages, only
for handling the connection and sending and receiving the messages.
This module abstracts out all the TCP/IP communications handling, so
that outside modules only need the LVPythonConnectorMessage class,
and the essentially python-to-LabVIEW directed messages.
We use the q_caller_gui queue to do message handling. 

Outward-facing Variables:

q_python_to_LabVIEW - queue for the state machine controlling
    the essentially python-to-LabVIEW directed messages.
q_caller_gui - queue that the caller (driver) should use
    for its state machine in interacting with the communicators.
q_script_update - queue that updates the user as to what's going on.
loop_continue - boolean variable to tell all queued state machines
    to exit, including the q_caller_gui.
script_running - boolean variable to tell the user whether a Python
    script is running or not.

Class definition:

class LVPythonConnectorMessage(object):
    command: string
    data: list of strings

    def __init__(self: "LVPythonConnectorMessage",
                 command: str = "", data = None) -> None:
    def __str__(self: "LVPythonConnectorMessage") -> str:
    def light_reply_copy(self: "LVPythonConnectorMessage") -> \
            "LVPythonConnectorMessage":
    def pack_message(self: "LVPythonConnectorMessage") -> bytes:
    def unpack_message(self: "LVPythonConnectorMessage",
                       tcp_string: str) -> "LVPythonConnectorMessage":

Function definitions:

def close_tcp(socket_id: str) -> None:
def compute_timeout(number_of_bytes: int) -> float:
def connect_tcp(socket_id: str) -> None:
def decrement_loop_count() -> None:
def flush_queue(queue_name: multiprocessing.Queue) -> list:
def flush_socket(sock: socket.socket) -> str:
def increment_loop_count() -> None:
def keep_alive_loop() -> None:
def LabVIEW_to_python_message_handling_loop() -> None:    
def python_to_LabVIEW_message_handling_loop() -> None:
def read_tcp(sock: socket.socket, caller_source: str) \
        -> "LVPythonConnectorMessage":
def receive_all(sock: socket.socket, n: int) -> bytes:
def send_tcp(message: "LVPythonConnectorMessage",
             sock: socket.socket, caller_source: str) -> None:
def shutdown_test_loop_count() -> bool:
def spawn_thread(function_name: "function") -> None:
def startup_test_loop_count() -> bool:
def trim_string(string_to_trim: str) -> str:
"""


""" --------------------    Import Statements    ------------------- """


import json              # For packing and unpacking lists of strings.
import multiprocessing   # For queues and inter-loop communication.
import socket            # For handling TCP/IP connections.
import select            # For polling TCP/IP connections.
import sys               # For error handling
import threading         # For spawning off our parallel loops.
import queue                         # to catch queue exceptions
import time              # For controlling loop rates.
import tkinter as tk     # To get LabVIEW's url if it didn't call.
import ipaddress         # To test for valid IP addresses
import traceback         # allow traceback on exceptions


""" -------------------    Debugging Switches    ------------------- """


# Uncomment the second line to enable that debug.

get_tcp_address_debug = False
# get_tcp_address_debug = True

keep_alive_debug = False
# keep_alive_debug = True

LabVIEW_to_python_debug = False
# LabVIEW_to_python_debug = True

python_to_LabVIEW_debug = False
# python_to_LabVIEW_debug = True

read_tcp_debug = False
# read_tcp_debug = True

send_tcp_debug = False
# send_tcp_debug = True

close_tcp_debug = False
# close_tcp_debug = True

connect_tcp_debug = False
# connect_tcp_debug = True

function_start_finish_debug = False
# function_start_finish_debug = True

loop_end_debug = False
# loop_end_debug = True


""" -------------------    Constants and Setup    ------------------ """


# Avoid unknown variable warnings. python_to_LabVIEW_socket
# and LabVIEW_to_python_socket and keep_alive_socket
# must be global everywhere. Units are seconds.
socket.setdefaulttimeout(1)
socket_timeout = 1

# Initialize all three sockets, but don't connect yet.
python_to_LabVIEW_socket = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM)
LabVIEW_to_python_socket = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM)
keep_alive_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)

# If LabVIEW calls the code, just use localhost.
if 1 < len(sys.argv):
    if 'localhost' == sys.argv[1]:
        # Argument is non-empty: use it for the address.
        address = str(sys.argv[1])
    else:
        # Test for good IPv4 or IPv6 address.
        try:
            ipaddress.ip_address(str(sys.argv[1]))
            address = str(sys.argv[1])
        except ValueError:
            print("Not a valid IP address.")

# If the python code is not called directly by LabVIEW, then we need
# the user to specify the LabVIEW machine's IP address.
else:
    # GUI code to obtain LabVIEW machine's IP address.

    root = tk.Tk()

    # Prompt for the user to enter the IP address.
    main_label = tk.Label(root, text='IP Address for LabVIEW Server')
    main_label.pack()

    # String entry box to get the IP address.
    main_string_entry = tk.Entry(root, text='', justify=tk.CENTER,
                                 width=28)
    main_string_entry.pack()

    # Make this string entry box get the focus.
    main_string_entry.focus_set()

    # Default will be localhost, but typing in anything will immediately
    # show up in the string entry box.
    main_string_entry.insert(0, 'localhost')
    main_string_entry.selection_range(0, tk.END)

    def on_enter(event=None):
        """
        This function gets the string entry, and quits this tiny GUI.
        :param: event: A throw-away argument, because we want to be able
                        to call this function on button click or when
                        the user hits Enter.
        :return: 
        """
        global address
        global main_string_entry
        global root

        # Get the string in the Entry widget.
        temp_address = main_string_entry.get()
        # Assign the result to the global variable 'address'.
        if '' == temp_address:
            address = 'localhost'
        else:
            address = temp_address
        # Close the GUI and exit.
        root.withdraw()
        root.quit()

    # Make sure the KP Enter or Return key locks in the address.
    root.bind('<Return>', on_enter)
    root.bind('<KP_Enter>', on_enter)
    root.title('')
    # Run the little GUI.
    root.mainloop()

# Assign the ports.
if 5 <= len(sys.argv):
    # Get port numbers from the command-line arguments.
    keep_alive_port = int(sys.argv[2])
    LabVIEW_to_python_port = int(sys.argv[3])
    python_to_LabVIEW_port = int(sys.argv[4])

else:
    # Define the default port numbers for each of the three connections.
    # Here we didn't have enough arguments to get the port numbers.
    keep_alive_port = 9007
    LabVIEW_to_python_port = 9008
    python_to_LabVIEW_port = 9009

# If debugging turned on, print address.
if get_tcp_address_debug:
    print(str(address))

# We are using a standard Windows carriage return line feed termination
# sequence. This should work regardless of platform.
LINE_ENDING = "\r\n"

# This is the python-to-LabVIEW queue, for handling messages.
q_python_to_LabVIEW = multiprocessing.Queue()

# The calling code must have a queued state machine that uses
# this queue name as its own.
q_caller_gui = multiprocessing.Queue()

# This queue allows either communication direction to update the user
# as to its status, without bogging down the q_caller_gui queue.
q_script_update = multiprocessing.Queue()

# This queue is for smart shutdown. The PtoL loop will send a message
# when all loops but itself have finished, and then enqueue to this
# queue. The main Python file eats this value before calling
# sys.exit(0). It will only ever have one element on it.
q_quit = multiprocessing.Queue(1)

# Boolean loop shutdown variable.
loop_continue = True

# Dictionary consisting of thread_id (script_id): boolean pairs.
script_running = {}

# Description of the number of running loops
loops_running = 0

# Number of loops we need running
required_loops = 7

# Stuff needed to maintain correct python_message_id's for all classes.
python_message_id_lock = threading.Lock()
# We will always increment before using, so this value should always
# be positive.
current_python_message_id = 0


""" -------------------------    Classes    ------------------------ """


class LVPythonConnectorMessage(object):
    """
    We encapsulate the basic data (command, data) necessary for a 
    TCP/IP message we can send to and from LabVIEW. We just need an
    initializer, a packer, and an unpacker for methods.
    
    command: string
    script_id: int32
    LabVIEW_server_id: string
    python_message_id: int32
    data: list of strings
    """

    global function_start_finish_debug
    global LINE_ENDING


    def __init__(self: "LVPythonConnectorMessage",
                 command="", data=None, script_id=0,
                 python_message_id=0) -> None:
        """
        We initialize the class with the inputs: the command
        string and the data list-of-strings.
        :param command: See below for descriptions.
        :param data:
        :param script_id:
        :param python_message_id:
        """

        global function_start_finish_debug

        if function_start_finish_debug:
            print("Start __init__ function for class.")

        self.command = command

        # Uniquely determined by Python, and it equals the thread id.
        self.script_id = script_id

        # The LabVIEW_server_id is completely static for any instance of
        # TestScript. We just need to pass it back all the time,
        # because the LabVIEW side, if multi-server, will need it.
        # The LabVIEW_server_id will always be ip address:keep-alive
        # port. For example: localhost:9007
        self.LabVIEW_server_id = str(address) + ":" + \
            str(keep_alive_port)

        # The python_message_id allows for customers to do exception
        # handling in their scripts, without confusion as to which
        # result corresponds to which action.
        self.python_message_id = python_message_id

        # The payload.
        self.data = [] if data is None else data

        if function_start_finish_debug:
            print("Stop __init__ function for class.")


    def __str__(self: "LVPythonConnectorMessage") -> str:
        """
        Provide the standard str functionality. 
        :param self: usual self object.
        :rtype: str: This is the string representation of the object.
        """

        return self.command + " | " + \
            str(self.script_id) + " | " + \
            self.LabVIEW_server_id + " | " + \
            str(self.python_message_id) + " | " + \
            str(self.data)


    def assign_message_id(self: "LVPythonConnectorMessage") -> None:
        """
        This function accesses the current_message_id global variable
        and assigns a new python_message_id to the self class.
        :return:
        """

        global python_message_id_lock
        global current_python_message_id

        # Protect current_python_message_id from other accessors.
        python_message_id_lock.acquire()

        # Always make sure the python_message_id > 0
        current_python_message_id += 1
        self.python_message_id = current_python_message_id

        # Let someone else get a python_message_id.
        python_message_id_lock.release()


    def get_message_id(self: "LVPythonConnectorMessage") -> int:
        """
        This is just an accessor for the message id, which we need to
        correlate when we get results back.
        :return: self.python_message_id
        """

        return self.python_message_id


    def light_reply_copy(self: "LVPythonConnectorMessage") -> \
            "LVPythonConnectorMessage":
        """
        This is a light copy. We get the command and script_id, but not
        the data. This is useful for the tcp replies. Note that the
        command has the string " reply" appended to it.
        :param self: usual self object
        "rtype: LVPythonConnectorMessage: This is the copied object.
        """

        # Get new instance of current class, with only the command and
        # script_id and python_message_id inserted. The
        # LabVIEW_server_id should be auto-generated when the __init__
        # magic function is called.
        return self.__class__(command=self.command + " reply",
                              script_id=self.script_id,
                              python_message_id=self.python_message_id)


    def pack_message(self: "LVPythonConnectorMessage") -> bytes:
        """
        This function packs the internal data into a single bytes
        object suitable for sending over the TCP/IP connection.
        We use the json dumps function to pack the data into a single
        string. This is a good choice, since LabVIEW has mirror
        functions on its end.
        :param self: usual self object.
        :rtype: bytes: A bytes object suitable for sending over TCP/IP.
        """

        global LINE_ENDING

        """
        return bytes(self.command + "|" + 
                     str(self.script_id) + "|"
                     + self.LV_server_id + "|"
                     + str(self.python_message_id) + "|"
                     + json.dumps(self.data)
                     + LINE_ENDING, encoding='UTF-8')
        """
        return bytes(self.command, encoding='UTF-8') + \
            bytes("|", encoding='UTF-8') + \
            bytes(str(self.script_id), encoding='UTF-8') + \
            bytes("|", encoding='UTF-8') + \
            bytes(self.LabVIEW_server_id, encoding = 'UTF-8') + \
            bytes("|", encoding = 'UTF-8') + \
            bytes(str(self.python_message_id), encoding = 'UTF-8') + \
            bytes("|", encoding = 'UTF-8') + \
            bytes(json.dumps(self.data), encoding='UTF-8') + \
            bytes(LINE_ENDING, encoding='UTF-8')


    def unpack_message(self: "LVPythonConnectorMessage",
                       tcp_string: str) -> "LVPythonConnectorMessage":
        """
        This function takes the TCP/IP string read from the connection,
        and unpacks it into the class's internal data: the command
        string and the data list-of-strings. We use the json loads
        command to get the list-of-strings from the single string.
        :param self: usual self object.
        :param tcp_string: The string we got over TCP/IP to convert.
        :return: A LVPythonConnectorMessage object.
        """

        global LINE_ENDING
        global function_start_finish_debug

        if function_start_finish_debug:
            print("Start unpack_message function for class.")

        # The command is everything before the first pipe symbol |
        self.command = tcp_string.split("|")[0]
        # Get the script_id as the second element in the array.
        self.script_id = int(tcp_string.split("|")[1])
        # Get the LV_server_id as the third element in the array.
        self.LabVIEW_server_id = tcp_string.split("|")[2]
        # Get the python_message_id as the fourth element in the array.
        self.python_message_id = int(tcp_string.split("|")[3])
        # Split at the second |, and don't include the carriage return
        # line feed at the end.
        temp_string = tcp_string.split("|")[4].split(LINE_ENDING)[0]
        # temp_string += "]"
        try:
            self.data = json.loads(temp_string)
        except ValueError:
            q_caller_gui.put(["Error",
                              "Didn't get expected list of strings: "
                              + self.command + " data: "
                              + temp_string])

        if function_start_finish_debug:
            print("Stop unpack_message for class.")

        return self


""" ------------------------    Functions    ----------------------- """


def close_tcp(socket_id: str) -> None:
    """
    This function simply closes the TCP/IP connection. 
    :param socket_id: A string identifying the socket to close.
    :return: 
    """

    # Grab the socket global variables.
    global python_to_LabVIEW_socket
    global LabVIEW_to_python_socket
    global keep_alive_socket
    # We need these debug flags:
    global python_to_LabVIEW_debug
    global LabVIEW_to_python_debug
    global keep_alive_debug
    global function_start_finish_debug
    global close_tcp_debug

    if function_start_finish_debug or close_tcp_debug:
        print("Start close_tcp function.")

    try:
        # Only print if correct debugging flag is high.
        # Attempt to close the indicated socket.

        if "python_to_LabVIEW" == socket_id:
            python_to_LabVIEW_socket.close()
            if python_to_LabVIEW_debug or close_tcp_debug:
                print("python-to-LabVIEW close_tcp successful.")
        elif "LabVIEW_to_python" == socket_id:
            LabVIEW_to_python_socket.close()
            if LabVIEW_to_python_debug or close_tcp_debug:
                print("LabVIEW-to-python close_tcp successful.")
        elif "keep_alive" == socket_id:
            keep_alive_socket.close()
            if keep_alive_debug or close_tcp_debug:
                print("keep-alive close_tcp successful.")
        else:
            pass

        """ Old Way. 
        if this_socket.fileno() == python_to_LabVIEW_socket.fileno():
            this_socket.close()
            if python_to_LabVIEW_debug:
                print("python-to-LabVIEW close_tcp successful.")
        elif this_socket.fileno() == LabVIEW_to_python_socket.fileno():
            this_socket.close()
            if LabVIEW_to_python_debug:
                print("LabVIEW-to-python close_tcp successful.")
        elif this_socket.fileno() == keep_alive_socket.fileno():
            this_socket.close()
            if keep_alive_debug:
                print("keep-alive close_tcp successful.")
        else:
            pass
        """

    except:
        # The socket might not be good. Just print the sys.exc_info
        # message if any debug flag is high.
        if python_to_LabVIEW_debug or LabVIEW_to_python_debug \
                or keep_alive_debug or close_tcp_debug:
            print("close_tcp got error: " + traceback.format_exc())
        else:
            pass

    if function_start_finish_debug or close_tcp_debug:
        print("Stop close_tcp function.")


def compute_timeout(number_of_bytes: int) -> float:
    """
    This function returns a reasonable socket timeout for transmitting
    the number of bytes (input). We use the same function on the LabVIEW
    side. The minimum timeout will be 9 s.
    :param number_of_bytes:
    :return: timeout in seconds for the socket
    """
    bytes_per_second = 16000
    return max(9.0, number_of_bytes / bytes_per_second)


def connect_tcp(socket_id: str) -> None:
    """
    This function connects to the LabVIEW side via TCP/IP.
    :param socket_id: A simple string indicating which socket to open.
                    Possible values:    python_to_LabVIEW,
                                        LabVIEW_to_python,
                                        keep_alive
    :return: 
    """

    # loop_continue to make sure code exits promptly.
    global loop_continue

    # The IP address of the LabVIEW machine.
    global address

    # Need the ports, which we will use depending on the socket_id
    # input.
    global python_to_LabVIEW_port
    global LabVIEW_to_python_port
    global keep_alive_port

    # We will assign the local variable this_socket depending on the
    # socket_id input.
    global python_to_LabVIEW_socket
    global LabVIEW_to_python_socket
    global keep_alive_socket

    # We need these debug flags:
    global connect_tcp_debug
    global function_start_finish_debug
    global socket_timeout

    if function_start_finish_debug:
        print("Start connect_tcp function.")

    # Initialize the connected boolean.
    connected = False

    # Align port and socket variable to the correct socket.
    if "python_to_LabVIEW" == socket_id:
        this_socket = python_to_LabVIEW_socket
        port = python_to_LabVIEW_port
    elif "LabVIEW_to_python" == socket_id:
        this_socket = LabVIEW_to_python_socket
        port = LabVIEW_to_python_port
    elif "keep_alive" == socket_id:
        this_socket = keep_alive_socket
        port = keep_alive_port
    else:
        this_socket = None
        port = None
        if connect_tcp_debug:
            print("No-man's land?")

    if connect_tcp_debug:
        print(str(socket_id) + " " + str(port))

    # Loop until we're completely connected.
    loop_counter = 0

    # We'll go with 10 retries, and see how that works.
    retries = 0

    while loop_continue and (not connected) and 1000 > retries:
        retries += 1
        if connect_tcp_debug:
            print("connect_tcp counter at "
                  + str(loop_counter) + " and loop_continue = "
                  + str(loop_continue) + " and connected = "
                  + str(connected) + " for port " + str(port))
            loop_counter += 1

        try: 
            # First close the socket.
            this_socket.close()
        except:
            pass

        # Here we attempt to create the connection.
        try:
            start_time = time.perf_counter()
            this_socket = socket.create_connection((address, port), 0.1)

            if connect_tcp_debug:
                print("Trying to connect to " + socket_id)
                print("Time to connect: "
                      + str(time.perf_counter() - start_time))

            # Test there and back with 8 bytes.
            this_socket.sendall(b'Testing.')
            testing_string = str(this_socket.recv(8), encoding='UTF-8')

            # See if it worked.
            if "Testing." != testing_string:
                if connect_tcp_debug:
                    print("Didn't get the Testing. handshake. Got: ")
                    print(testing_string)
                raise Exception("Didn't get the Testing. handshake.")
            connected = True
            if connect_tcp_debug:
                print(socket_id + " is connected!")

        except:
            # Only print if correct debugging flag is high:
            connected = False
            # If we're on the tenth retry, raise the exception back
            # to the caller, and call it quits.
            if 1000 <= retries:
                if function_start_finish_debug:
                    print("Stop connect_tcp function.")
                # We failed to connect: exit the function.
                raise Exception("Exceeded max number of connect "
                                "retries.")
            else:
                # We'll keep trying. If we're debugging, print error.
                if connect_tcp_debug:
                    print("connect_tcp got error: "
                          + traceback.format_exc())

    # We have successfully connected, so push the socket out to the
    # correct global variable.
    if "python_to_LabVIEW" == socket_id:
        python_to_LabVIEW_socket = this_socket
    elif "LabVIEW_to_python" == socket_id:
        LabVIEW_to_python_socket = this_socket
    elif "keep_alive" == socket_id:
        keep_alive_socket = this_socket
    if function_start_finish_debug:
        print("Stop connect_tcp function.")


def decrement_loop_count() -> None:
    """
    This function is an atomic action to decrement the loop count, so
    that we don't try to restart Python until the previous instance is
    completely gone.
    :return:
    """

    global loops_running

    loops_running -= 1


def flush_queue(queue_name: multiprocessing.Queue) -> list:
    """
    This function simply gets from the queue until it is empty. 
    It returns all the elements in the queue.
    :param queue_name: The queue to flush.
    :rtype: list: A list containing all elements on the queue at
                    flush time.
    """

    global loop_continue
    global function_start_finish_debug

    if function_start_finish_debug:
        print("Start flush_queue function.")

    # Set up the list.
    return_list = []

    # Keep going until the queue is empty.
    while (not queue_name.empty()) and loop_continue:
        try:
            # Get an element off the queue and put it into the list.
            return_list.append(queue_name.get())
        except:
            pass

    if function_start_finish_debug:
        print("Stop flush_queue function.")

    # Return a list containing all the queue elements.
    return return_list


def flush_socket(sock: socket.socket) -> str:
    """
    This function reads all the data in the socket until it times out,
    and the timeout is set extremely small. It returns all the data
    read.
    :param sock:
    :return: bytes: the data read out.
    """

    # Get initial timeout to restore later.
    initial_timeout = sock.gettimeout()

    # Want this function to execute FAST.
    sock.settimeout(0.0)

    # Initialize read_bytes, in case receive doesn't work.
    read_bytes = b''

    try:
        read_bytes = sock.recv(999999)
    except:
        pass

    # Restore initial timeout.
    sock.settimeout(initial_timeout)

    # Convert to string and return.
    return str(read_bytes, encoding='UTF-8')


def increment_loop_count() -> None:
    """
    This function is an atomic action to increment the loop count, so
    that we don't try to do anything with the connector until every
    loop is operational.
    :return:
    """

    global loops_running

    loops_running += 1


def keep_alive_loop() -> None:
    """
    This function wraps a loop that keeps the TCP/IP connection alive
    by periodically (every 5 seconds) sending a heartbeat signal.
    Note that the keep-alive signal is all python-to-LabVIEW directed,
    which makes sense since the LabVIEW side is viewed as the server.
    We will let the keep_alive_loop close the TCP/IP connection, as
    well as all the other loops (python-to-LabVIEW, LabVIEW-to-python,
    and the various spawned loops.)
    :rtype: None
    """

    # Need the keep_alive_socket variables and the
    # loop_continue variable,
    # both defined above in the Setup Statements section.
    # Also need some debug variables.
    # The script_running variable is what we'll send to LabVIEW
    # periodically.

    global keep_alive_socket
    global loop_continue
    global q_caller_gui
    global q_script_update
    global keep_alive_debug
    global function_start_finish_debug
    global loop_end_debug
    global script_running

    if function_start_finish_debug:
        print("Start keep_alive_loop.")

    # A couple of constants for coding convenience: the loop rate
    # throttles this loop so it doesn't take all CPU time.
    keep_alive_loop_rate = 1.0  # Units are seconds.

    # The message is what we're going to send along to the LabVIEW
    # side so everyone knows the connection is alive.
    get_message = LVPythonConnectorMessage("Else", [])

    # For debug purposes.
    loop_counter = 0

    # Let everyone know this loop is now running.
    increment_loop_count()

    # Debugging for timeouts
    ka_start_time = time.perf_counter()

    # Enter keep_alive loop.
    while loop_continue:
        if keep_alive_debug:
            print("keep_alive counter at "
                  + str(loop_counter) + " and time is "
                  + str(time.perf_counter() - ka_start_time))
            loop_counter += 1

        # We send back to LabVIEW the info as to whether a script is
        # running or not.
        keep_alive_message = \
            LVPythonConnectorMessage("I'm alive! " +
                                     str(startup_test_loop_count()),
                                     [str(script_running)])

        try:
            # Try to send and get the keep-alive message.
            send_tcp(keep_alive_message, keep_alive_socket,
                     "keep_alive")

            # Debugging only.
            if keep_alive_debug:
                print("Keep-alive sent message is: "
                      + trim_string(str(keep_alive_message)))
            get_message.command = "Else"

            # We continue the keep-alive loop:
            # Make sure loop does not eat up CPU time unnecessarily.
            # Make sure keep-alive loop is interruptable.
            start_time = time.perf_counter()

            # Sleep for small periods of time. Note that the time.time
            # function is deprecated. We use the time.perf_counter
            # function instead. This loop waits for keep_alive_loop_rate
            # seconds.
            while loop_continue and \
                    (time.perf_counter() - start_time
                        < keep_alive_loop_rate):
                time.sleep(0.01)

            # We timed out on the wait above. This means we should
            # keep going.
            if loop_continue:
                # Try to get the reply from LabVIEW.
                get_message = read_tcp(keep_alive_socket, "keep_alive")

                # Debugging only. Print out useful stuff.
                if keep_alive_debug:
                    print("Keep-alive received message is: "
                          + trim_string(str(get_message)))
                    status_message_data = get_message.data
                    status_message = ["Keep-alive data from" +
                                      " LabVIEW is ",
                                      status_message_data]
                    q_script_update.put(status_message)

        except:
            # Something went wrong in the send_tcp or the read_tcp.
            flush_string = flush_socket(keep_alive_socket)
            if keep_alive_debug:
                print("Keep-alive Exception caught "
                      + traceback.format_exc() + flush_string)
            try:
                q_caller_gui.put(["Error",
                                  """Failure in keep-alive. 
                                  We got error:"""
                                  + traceback.format_exc()])

                # Try to close and reconnect.
                close_tcp("keep_alive")
                connect_tcp("keep_alive")

            # Ignore all errors.
            except:
                if keep_alive_debug:
                    print("Keep-alive Exception caught "
                          + traceback.format_exc())
                # Stop everything: reconnect failed.
                loop_continue = False

    # Cleanup after keep_alive loop ends. close_tcp() has its own
    # error handling, no need to do it here.
    close_tcp("keep_alive")

    # Make sure all other loops exit, ignoring errors.
    loop_continue = False

    # Let everyone else know this loop is done.
    decrement_loop_count()

    if function_start_finish_debug or loop_end_debug:
        print("Stop keep_alive_loop.")


def LabVIEW_to_python_message_handling_loop() -> None:
    """ 
    This function wraps a loop that implements a 
    simple try-to-get-and-reply loop. This loop handles all the
    TCP/IP for receiving a message from LabVIEW and sending a reply.
    :rtype: None
    """

    # Need the TCP/IP socket variable and the loop_continue variable,
    # both defined above in the Setup Statements section.
    # We need the
    # q_caller_gui queue object to pass messages back to this
    # module's caller. Also need a debug switch.

    global LabVIEW_to_python_socket
    global loop_continue
    global q_caller_gui
    global LabVIEW_to_python_debug
    global function_start_finish_debug
    global loop_end_debug

    if function_start_finish_debug:
        print("Start LabVIEW_to_python function.")

    # Begin regular tcp/ip loop, very parallel to what the new LabVIEW
    # code is doing. Don't need any queues at all here.
    # We will need a queue for the python-to-LabVIEW communicator.
    # The loop_counter is for debug.
    loop_counter = 0

    # Let everyone know this loop is running.
    increment_loop_count()

    # Keep going while the loop_continue boolean is high.
    while loop_continue:
        if LabVIEW_to_python_debug:
            print("LabVIEW_to_python counter at "
                  + str(loop_counter))
            loop_counter += 1

        try:
            # Try to get a message. This will time out frequently.
            temp_message = read_tcp(LabVIEW_to_python_socket,
                                    "LabVIEW_to_python")

            if LabVIEW_to_python_debug:
                print("LabVIEW-to-python got message: "
                      + trim_string(str(temp_message)))

            # Test to see if we got a real message.
            # If we have a real message...
            if None is not temp_message:

                # Need two different messages: one to reply back
                # to LabVIEW, and one to forward on to the caller.
                # Don't want to copy data back to caller.
                reply_message = temp_message.light_reply_copy()

                # Propagate message back to LabVIEW and the caller.
                # Here we send the message back to LabVIEW, with
                # the string " reply" appended to the command.
                send_tcp(reply_message, LabVIEW_to_python_socket,
                         "LabVIEW_to_python")

                # reply_message is what we sent back to LabVIEW
                # to acknowledge that we got it.
                q_caller_gui.put(["LabVIEW-to-python Reply",
                                  reply_message])

                # temp_message is the actual message we got from
                # LabVIEW.
                q_caller_gui.put(["LabVIEW-to-python Sent",
                                  temp_message])

                # Go ahead and shut everything down if we got a
                # quit_python message. This is so we don't try to
                # re-connect if the TestScript server is being
                # run continuously.
                if "quit_python" == temp_message.command:
                    loop_continue = False
            
        except socket.timeout:
            # We expect timeout errors here all the time.
            # Throw them away: flush the socket.
            flush_string = flush_socket(LabVIEW_to_python_socket)
            if LabVIEW_to_python_debug:
                print("Flushed " + flush_string)

        except:
            # General exceptions - attempt to reconnect.
            flush_string = flush_socket(LabVIEW_to_python_socket)
            if LabVIEW_to_python_debug:
                print("LabVIEW-to-python got error: "
                      + traceback.format_exc() + flush_string)
                print("Attempting to reconnect" +
                      " LabVIEW to Python socket")
            try:
                # Try to close and reconnect.
                close_tcp("LabVIEW_to_python")
                connect_tcp("LabVIEW_to_python")
            except:
                # Allow the loop to continue trying until loop_continue
                # is lowered by the keep_alive abort
                pass

    # Cleanup after LabVIEW_to_python loop ends. close_tcp() has its own
    # error handling, no need to do it here.
    close_tcp("LabVIEW_to_python")

    # Let everyone else know this loop is done.
    decrement_loop_count()

    if function_start_finish_debug or loop_end_debug:
        print("Stop LabVIEW_to_python function.")


def python_to_LabVIEW_message_handling_loop() -> None:
    """ 
    This function wraps a loop that implements a simple
    try-to-send-and-get-reply loop. This loop handles all the
    TCP/IP for sending a message to LabVIEW and getting back the reply.
    :rtype: None
    """

    # Need the TCP/IP socket variable and the loop_continue variable,
    # both defined above in the Setup Statements section.
    # We need the q_python_to_LabVIEW object,
    # so that we can insert messages into this loop, and we need the
    # q_caller_gui queue object to pass messages back to this
    # module's caller.
    # Also need a couple of debug switches.

    """ --- Setup --- """

    global python_to_LabVIEW_socket
    global loop_continue
    global q_caller_gui
    global q_python_to_LabVIEW
    global python_to_LabVIEW_debug
    global function_start_finish_debug
    global loop_end_debug

    if function_start_finish_debug:
        print("Start python_to_LabVIEW function.")

    # This is what we send back to the caller if there's a problem.
    error_message = LVPythonConnectorMessage("Error", [])

    # Begin queued state machine main loop. Data type is list:
    # [state, LVPythonConnectorMessage]
    # This loop is always shut down by the keep_alive_loop.
    # loop counter is just for debug.
    loop_counter = 0

    # Initialize q_message
    q_message = None

    # Let everyone know this loop is running.
    increment_loop_count()

    """ --- Main --- """

    # Enter loop, shut down only by the global boolean.
    while loop_continue:

        try:  # mainly for send_tcp and read_tcp functions.
            if python_to_LabVIEW_debug:
                print("python_to-LabVIEW counter at "
                      + str(loop_counter))
                loop_counter += 1

            if None is q_message:
                # Get the message from the queue. If q_message
                # is not None, we have a retry - use the old one.
                try:
                    q_message = q_python_to_LabVIEW.get(True, 1)
                except queue.Empty:
                    q_message = None
                    pass
                except:
                    raise

            if python_to_LabVIEW_debug:
                print("python-to-LabVIEW q message is " +
                      trim_string(str(q_message)))

            if None is not q_message:
                # If there's a message to send, grab it; we don't want
                # an out-of-range error.
                send_message = q_message[1] if 1 < len(q_message) \
                    else None

                # Copy the most important parts. Don't copy the data,
                # as it might be huge. It's unnecessary.
                reply_message = send_message.light_reply_copy()

                # Try to send the message.
                send_tcp(send_message, python_to_LabVIEW_socket,
                         "python_to_LabVIEW")

                # For debugging only:
                if python_to_LabVIEW_debug:
                    print("python-to-LabVIEW tried to send " +
                          trim_string(str(send_message)))
                    print("python_to_LabVIEW socket timeout: " +
                          str(python_to_LabVIEW_socket.gettimeout()))

                # We expect LabVIEW to reply back with a slightly
                # altered message.
                read_message = read_tcp(python_to_LabVIEW_socket,
                                        "python_to_LabVIEW")

                # Should only execute business logic if the full
                # round-trip took place.
                q_caller_gui.put(["python-to-LabVIEW Sent",
                                  send_message])

                # Test to see if the reply back was good.
                if reply_message.command != read_message.command:
                    # Had a problem somewhere.
                    reply_message = error_message

                # Now we pass the reply on to the caller.
                q_caller_gui.put(["python-to-LabVIEW Reply",
                                  reply_message])

                # Sending was successful if we get here: write None.
                q_message = None

        except:

            # Clear buffer.
            flush_string = flush_socket(python_to_LabVIEW_socket)

            if python_to_LabVIEW_debug:
                print("python-to-LabVIEW got error")
                traceback.print_exc()
                print("python_to_LabVIEW socket timeout: " +
                      str(python_to_LabVIEW_socket.gettimeout()) +
                      flush_string)
                print("Attempting to reconnect" +
                      " python to LabVIEW socket")
            try:
                # Had errors above. Try to reconnect.
                close_tcp("python_to_LabVIEW")
                connect_tcp("python_to_LabVIEW")

            except:
                # Allow the loop to continue trying until loop_continue
                # is lowered by the keep_alive abort
                pass

            if python_to_LabVIEW_debug:
                print("attempting to re-enqueue " 
                      + trim_string(str(q_message)))

    """ --- Cleanup --- """

    shutdown_start_time = time.perf_counter()

    # This loop waits until the other loops have quit, or until a
    # two-second timeout.
    while not shutdown_test_loop_count() and \
            time.perf_counter() - shutdown_start_time < 2:

        if python_to_LabVIEW_debug:
            print(str(shutdown_test_loop_count()))

        # Make sure we're not using heavy processing.
        time.sleep(0.010)

    if python_to_LabVIEW_debug:
        print(str(shutdown_test_loop_count()))

    # Do the wrap-up code now.
    quit_message = LVPythonConnectorMessage("python_quit", [], -1)

    # Wrap in try clause, throw away exceptions.
    try:
        # Let LabVIEW know the other loops are gone.
        # Need to set loop_continue = True to allow sending and
        # reading on the TCP connection.
        loop_continue = True
        send_tcp(quit_message, python_to_LabVIEW_socket,
                 "python_to_LabVIEW")

        if python_to_LabVIEW_debug:
            print("Successful sending.")

        # Read the reply, but we're not interested in it, except for
        # debugging.
        reply_message = read_tcp(python_to_LabVIEW_socket,
                                 "python_to_LabVIEW")

        if python_to_LabVIEW_debug:
            print(str(reply_message))

    except:

        if python_to_LabVIEW_debug:
            print("Had an exception trying to send LV the quit msg.")

    # Good practice explicitly to close the queue.
    try:
        # Flush the queue. Python will collect garbage.
        flush_queue(q_python_to_LabVIEW)
    except:
        pass

    # Cleanup after LabVIEW_to_python loop ends. close_tcp() has its own
    # error handling, no need to do it here.
    close_tcp("python_to_LabVIEW")

    # Now signal to the main Python file that it can exit.
    q_quit.put(True)

    if function_start_finish_debug or loop_end_debug:
        print("Stop python_to_LabVIEW function.")


def read_tcp(sock: socket.socket, caller_source: str) \
        -> "LVPythonConnectorMessage":
    """
    This function first peeks at the TCP/IP buffer to see if there
    is anything there, and then tries to parse what is there, if there
    is something there, into the standard format.
    :param sock: The socket from which to read.
    :param caller_source: The function that calls this function, for
                            debug purposes.
    :return: LVPythonConnectorMessage: We return this object.
    """

    global loop_continue
    global LINE_ENDING
    global read_tcp_debug
    global function_start_finish_debug

    if function_start_finish_debug or read_tcp_debug:
        print("Start read_tcp caller = " + caller_source)

    # Here's our temporary message holder.
    temp_message = LVPythonConnectorMessage("command", ["data"])

    # This value allows us to peek at the buffer before actually
    # reading from it.
    receive_flags = socket.MSG_PEEK

    # Boolean to let us know whether we've read a message or not.
    have_we_read = False

    # Loop counter is for debug purposes.
    loop_counter = 0

    # Enter the loop:
    while (not have_we_read) and loop_continue:
        if read_tcp_debug:
            print("read_tcp counter at " + str(loop_counter) + " for "
                  + caller_source)
            loop_counter += 1
        try:

            # Set timeout for 10-byte prepended size info
            sock.setblocking(0)

            # Begin new prepended message code.
            ready = select.select([sock], [], [], 0.5)
            if ready[0]:
                raw_message_length = sock.recv(10, receive_flags)
                message_length = int(str(raw_message_length,
                                     encoding='UTF-8'))
                if read_tcp_debug:
                    print("Message length is: " + str(message_length))
                                           
                if 8192 - 10 > message_length:  # Short message: peek

                    # Old code for reading - still best for shorter
                    # messages.
                    # Peek at the TCP data before taking it out of the
                    # buffer.
                    read = str(sock.recv(8192, receive_flags),
                               encoding='UTF-8')
                    termination_index = read.find(LINE_ENDING)

                    # Print the termination index.
                    if read_tcp_debug:
                        print("Found termination index at: "
                              + str(termination_index))

                    # If termination sequence was found, read up to and
                    # including the termination sequence.
                    # If it was not found, raise a socket timeout
                    # exception.
                    if 0 < termination_index:

                        # We now know exactly how many characters to
                        # read.
                        read = str(sock.recv(termination_index
                                             + len(LINE_ENDING))[10:],
                                   encoding='UTF-8')
                        if read_tcp_debug:
                            print("We read short message: " + read)

                        have_we_read = True
                    # End of Old Code for reading.

                else:
                    # New code for reading.
                    # Set the socket's timeout based on number of bytes:
                    sock.settimeout(compute_timeout(message_length))

                    # Print if debugging:
                    if read_tcp_debug:
                        print("Message length is: " +
                              str(message_length))
                        print("Socket timeout is: " +
                              str(sock.gettimeout()))

                    # Read that many bytes now, decode into string from
                    # bytes object.
                    read = receive_all(sock,
                                       message_length
                                       + 10)[10:].decode()

                    have_we_read = True

                # If we've not read, let the loop come around again.
                if have_we_read:

                    # Print raw bytes:
                    if read_tcp_debug:
                        print(trim_string(read))

                    # Return the command and data (without the trailing
                    # newline and carriage return)
                    temp_message.unpack_message(read)

                    if read_tcp_debug:
                        print("Message received was: "
                              + trim_string(str(temp_message))
                              + " for caller = " + caller_source
                              + " at loop "
                              + str(loop_counter))

                    # Usual debug printing.
                    if function_start_finish_debug or read_tcp_debug:
                        print("Stop read_tcp: successful read."
                              + " for caller = "
                              + caller_source
                              + " at loop "
                              + str(loop_counter))

                    # We're done reading. Success!
                    return temp_message

        except:
            # We ran into an issue somewhere. Let the caller handle
            # the exception.
            if read_tcp_debug:
                print("General exception in read_tcp.  Error: "
                      + traceback.format_exc()
                      + "\nCaller source: "
                      + caller_source + " " + str(sock) + " at "
                      + str(loop_counter))
            raise

    if function_start_finish_debug or read_tcp_debug:
        print("Stop read_tcp function. Shouldn't get here?")
        print("have_we_read = " + str(have_we_read) +
              " and loop_continue = "
              + str(loop_continue) + ". Caller was " + caller_source +
              " and at " + str(loop_counter))


def receive_all(sock: socket.socket, n: int) -> bytes:
    """
    Grabs the biggest amount of data possible at each step.
    :param sock:
    :param n:
    :return:
    """
    global read_tcp_debug
    global loop_continue
    
    # Helper function to receive n bytes or return None if EOF is hit.
    data = b''
    start_time = time.perf_counter()
    # data = sock.recv(n)
    
    while len(data) < n and loop_continue:
        packet = sock.recv(n - len(data))
        if not packet:
            return b''
        data += packet

    if read_tcp_debug:
        used_time = time.perf_counter() - start_time
        # print("Number of socket reads was: " + 
        #       str(number_of_iterations))
        print("Execution time was " + str(used_time))

    return data


def send_tcp(message: "LVPythonConnectorMessage",
             sock: socket.socket, caller_source: str) -> None:
    """
    This function will send the command and data to the script handler.
    :param message: What to send.
    :param sock: The socket on which to send the message.
    :param caller_source: The function that's calling this function, for
                            debug purposes.
    :return: 
    """

    global loop_continue
    global send_tcp_debug
    global function_start_finish_debug

    if function_start_finish_debug or send_tcp_debug:
        print("Start send_tcp function.")

    # This will be our message to send. We'll try to set it equal
    # to the message parameter and pack it.
    to_send = None

    # A boolean to indicate whether we've successfully sent our
    # message or not.
    have_we_sent = False

    # Counter is for debug purposes.
    loop_counter = 0

    # A counter for the number of retries we've attempted.
    retries = 0

    while (not have_we_sent) and loop_continue:
        if send_tcp_debug:
            print("send_tcp counter at " + str(loop_counter)
                  + " for " + str(caller_source))
            loop_counter += 1
        try:
            # We try to pack the message. If there's an error, we've got
            # bigger problems.
            to_send = message.pack_message()

            # Old sending code:
            # sock.sendall(to_send)

            # Now prepending message size.
            size_string = "%010d" % len(to_send)
            message_bytes = bytes(size_string, encoding='UTF-8') + \
                to_send

            if send_tcp_debug:
                print("Message to send is: " +
                      trim_string(str(message_bytes)))
                print("Message length is: " + str(len(to_send)))
                print("Socket timeout is: " +
                      str(compute_timeout(len(to_send))))

            # Set the socket timeout based on the message length
            sock.settimeout(compute_timeout(len(to_send)))

            # Always include tcp/ip operations in a try block, as we
            # could get an error.
            sock.sendall(message_bytes)

            # If we get here, the send worked.
            have_we_sent = True

            # If we didn't get an error, then we're done. Go back.
            if function_start_finish_debug or send_tcp_debug:
                print("Stop send_tcp function.")
            return

        except:

            # Got an error. Close and try to re-connect.
            q_caller_gui.put(
                ["Error", "Failure sending. We got error:"
                 + traceback.format_exc()
                 + ". Trying to reconnect."
                 + str(to_send)])

            # We allow 1 retry.
            if 1 > retries:
                retries += 1

                # Try to close and reconnect.
                close_tcp(caller_source)
                connect_tcp(caller_source)

            else:
                # Couldn't reconnect. Raise the exception to the
                # caller.
                if function_start_finish_debug or send_tcp_debug:
                    print("Stop send_tcp function.")
                raise

    if function_start_finish_debug or send_tcp_debug:
        print("Stop send_tcp function.")

    # We didn't return, so we must have timed out.
    raise socket.timeout


def shutdown_test_loop_count() -> bool:
    """
    This function tests to see if all but one loop is still running.
    Once this is the case, that one loop (the
    python_to_LabVIEW_message_handling_loop) will send a 'python_quit'
    message to LabVIEW, and then enqueue a message on the q_quit
    queue, and then exit.
    :param
    :return: Should return True if number of loops is less than or
            equal to 1.
    """

    global loops_running

    return loops_running <= 1


def spawn_thread(function_name: "function") -> None:
    """
    This function simply spawns off the input function name as a 
    separate thread. Wrapping this into a function allows us to 
    ignore the separate syntax.
    :param function_name: The function (loop) to be spawned.
    :return: 
    """

    global function_start_finish_debug

    if function_start_finish_debug:
        print("Start spawn_thread.")

    # Spawn off thread here.
    my_thread = threading.Thread(target=function_name)
    my_thread.start()

    if function_start_finish_debug:
        print("Stop spawn_thread.")


def startup_test_loop_count() -> bool:
    """
    This function tests to see if all necessary loops are running.
    :return: loops_running >= required_loops
    """

    global loops_running
    global required_loops

    return loops_running >= required_loops


def trim_string(string_to_trim: str) -> str:
    """
    This function sizes the output down to 200 chars at most, with
    the beginning and the end included, and ellipses used if any
    truncation occurred.
    :param string_to_trim: str
    :return: the trimmed string.
    """

    if 200 < len(string_to_trim):
        return string_to_trim[:145] + " ... " + string_to_trim[-50:]
    else:
        return string_to_trim		


""" -------------------------    Cleanup    ------------------------ """


# Initialize the tcp/ip connections.
kathread = threading.Thread(target=connect_tcp("keep_alive"))
plthread = threading.Thread(target=connect_tcp("python_to_LabVIEW"))
lpthread = threading.Thread(target=connect_tcp("LabVIEW_to_python"))

kathread.start()
plthread.start()
lpthread.start()
if connect_tcp_debug:
    print("Connection threads started")
plthread.join()
lpthread.join()
kathread.join()
if connect_tcp_debug:
    print("Connection threads joined")

# Start the three main loops in the same order as the socket
# connections.
spawn_thread(keep_alive_loop)
spawn_thread(python_to_LabVIEW_message_handling_loop)
spawn_thread(LabVIEW_to_python_message_handling_loop)
