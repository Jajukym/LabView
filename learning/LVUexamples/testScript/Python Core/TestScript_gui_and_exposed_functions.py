# coding=utf-8


"""
TestScript_gui_and_exposed_functions.py
Here's an example GUI driver for connecting to LabVIEW over the TCP/IP
connection. We use the TestScript_connector module.

Usage: start the LabVIEW Scripting Example.vi first, then run
this.

Notice that we need know nothing about the actual TCP/IP connection
in this module. We just need the connector message class,
which is the LVPythonConnectorMessage class, and the
names of the right queues to enqueue on:

ts.q_python_to_LabVIEW - queue for the state machine controlling
    the essentially python-to-LabVIEW directed messages.
ts.q_caller_gui - queue that the caller (driver) should use
    for its state machine in interacting with the communicators.
ts.q_script_update - queue that updates the user as to what's going on.

In addition, there are a couple of boolean variables important to this
file:

ts.loop_continue - boolean variable to tell all queued state machines
    to exit, including the q_caller_gui.
ts.script_running - Array of booleans this file controls to tell
    whether a python script with a particular script_id is running or
    not.
    
Function definitions:

def del_script_results(script_id: str) -> None:
def get_script_result(timeout: int=1) -> LVPythonConnectorMessage:
def send_message_to_LabVIEW() -> None:
def quit_gui() -> None:
def run_script() -> None:
def strip_list_string(list_of_a_string: str) -> str:

Spawned loops:

def consumer_loop() -> None:
def script_update_loop() -> None:
def scr_cmd_engine_loop() -> None:
def scr_runner_loop() -> None:

Exposed function definitions:
    
def action(command: str, data: list = None, timeout: int = 1) \
        -> LVPythonConnectorMessage:
def script_update(status: str) -> None:
def user_update(status: str) -> None:
def sleep(seconds: float) -> None:

GUI polling loop:

def pass_command_to_gui():
"""


""" --------------------    Import Statements    ------------------- """


import tkinter as tk                 # Our main GUI library.
from tkinter import filedialog       # To get files for running scripts.
# from tkinter.ttk import Scrollbar as Scrollbar  # For scrolling data.
import time                          # For timeouts.
import multiprocessing               # For local queues.
import queue                         # to catch queue exceptions
from copy import copy
# from os import linesep as linesep    # OS-dependent EOL char.
import os.path as path               # For path manipulations.
import os
import sys                           # For latest error.
import TestScript_connector as ts    # The connector.
from TestScript_connector import LVPythonConnectorMessage
import traceback                     # Get call stack.
import threading                     # Need this for spawning threads


""" -------------------    Constants and Setup    ------------------ """


# Define some constant test messages to send.
SEND_MSG_A = LVPythonConnectorMessage("Hello, LabVIEW!",
                                      ["Hello", "LabVIEW!"])
const_message = copy(SEND_MSG_A)

# Enqueue the initialize state.
ts.q_caller_gui.put(["A Initialize"])

# This is what we send back to the caller if there's a problem.
ERROR_MESSAGE = LVPythonConnectorMessage("Error", [])

# Make sure other loops in the TestScript_connector
# are well on their way.
# time.sleep(0.5)

# Queue for the script command engine:
q_scr_cmd_engine = multiprocessing.Queue()

# List for sending messages from the script command engine
# back to the functions that put items onto its queue.
l_scr_cmd_engine_result = []

# Mutex lock for result list
l_scr_cmd_engine_lock = threading.Lock()

# This queue is for script_id (thread_id) registration. When LabVIEW
# calls a script, it needs to register its thread_id as the script_id
# to Python.
q_scr_id_register = multiprocessing.Queue()

# Dedicated queue for running scripts
q_scr_runner = multiprocessing.Queue()

""" We will store all LabVIEW data into a list of dictionaries. 
    The get function will access this list of dictionaries.
    Example data: [{'Name':'voltage', 'Value':'0',
                 'Timestamp':'2017/04/27 12:44:33 pm'}]"""
LabVIEW_data = []

# Number of script abort messages sent. Needs to be on a thread-by-
# thread basis, so we use a dictionary. Index in via
# str(threading.get_ident())
number_abort_messages = {}

# Execute the application-specific function definitions dynamically.
# - mostly wrappers for the action function defined below.
with open("TestScript_application_specific_functions.py", 'r') as \
          my_file:
    data = my_file.read()
my_file.close()
exec(data, globals(), locals())


""" -------------------    Debugging Switches    ------------------- """


# Uncomment the second line to enable that debug.

gui_consumer_debug = False
# gui_consumer_debug = True

script_update_debug = False
# script_update_debug = True

script_command_engine_debug = False
# script_command_engine_debug = True

script_runner_debug = False
# script_runner_debug = True

function_debug = False
# function_debug = True

function_start_finish_debug = False
# function_start_finish_debug = True

loop_end_debug = False
# loop_end_debug = True


""" -----------    Storage, List, and String Functions    ---------- """


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


def del_script_results(script_id: str) -> None:
    """
    This function looks through the results list and deletes any that
    correspond to the thread's script_id. Used when a script exits, and 
    when it aborts.
    :param script_id: str
    :return: 
    """

    # The results list.
    global l_scr_cmd_engine_result
    global l_scr_cmd_engine_lock

    l_scr_cmd_engine_lock.acquire()

    # Just look through the list and compare script id's.
    for result in l_scr_cmd_engine_result:
        if script_id == str(result.script_id):
            l_scr_cmd_engine_result.remove(result)

    l_scr_cmd_engine_lock.release()


def get_script_result(timeout: int=1, python_message_id: int=0) \
        -> LVPythonConnectorMessage:
    """
    This function looks through the results list for timeout seconds,
    looking for any result corresponding to its script_id and
    python_message_id.
    :rtype: object
    :param timeout:
    :param python_message_id:
    :return: LVPythonConnectorMessage
    """

    # The results list.
    global l_scr_cmd_engine_result
    global l_scr_cmd_engine_lock
    global script_runner_debug

    # Get script_id once:
    script_id = threading.get_ident()

    if script_runner_debug:
        print("Looking for result on script_id " + str(script_id))
        print("Looking for result with message_id " +
              str(python_message_id))

    # Get the current time
    start_time = time.perf_counter()

    # While loop to continually poll list for result.
    while ts.loop_continue and ts.script_running[str(script_id)] and \
            ((time.perf_counter() - start_time < timeout) or
             0 >= timeout):

        l_scr_cmd_engine_lock.acquire()
        # Check list for relevant result:
        for result in l_scr_cmd_engine_result:
            if script_runner_debug:
                print("Looking at result: " + str(result))
                print("It has message_id: " +
                      str(result.get_message_id()))
                print("It has script_id: " +
                      str(result.script_id))
                print("First test result: " + str(script_id
                      == result.script_id))
                print("Second test result: " + str(python_message_id
                      == result.get_message_id()))
            if script_id == result.script_id and \
                    python_message_id == result.get_message_id():
                # Yank it out of the list and return the value.
                l_scr_cmd_engine_result.remove(result)
                l_scr_cmd_engine_lock.release()
                if script_runner_debug:
                    print("Got result: " + str(result))
                return result
        # return wasn't hit, so release() out here
        l_scr_cmd_engine_lock.release()
        time.sleep(0.001)

    # If we timed out, return None
    if time.perf_counter() - start_time >= timeout:
        elapsed = time.perf_counter() - start_time
        if script_runner_debug:
            print("Response timeout on thread " + str(script_id)
                  + " at " +
                  str("{:.3f}".format(elapsed) + "s"))
        raise RuntimeError('Timeout waiting for response from LabVIEW: '
                           + str('{:.3f}'.format(elapsed) + 's'))


""" ---------------------    Button Functions    ------------------- """


def send_message_to_LabVIEW() -> None:
    """ 
    Pass command onto the consumer.
    :rtype: None
    """
    global function_start_finish_debug

    if function_start_finish_debug:
        print("Start send_message_to_LabVIEW function.")

    ts.q_caller_gui.put(["send_message_to_LabVIEW"])

    if function_start_finish_debug:
        print("Stop send_message_to_LabVIEW function.")


def quit_gui() -> None:
    """
    Pass command onto the consumer.
    :rtype: None
    """
    global function_start_finish_debug

    if function_start_finish_debug:
        print("Start quit_gui function.")

    ts.q_caller_gui.put(["quit_gui"])

    if function_start_finish_debug:
        print("Stop quit_gui function.")


def run_script() -> None:
    """ 
    Pass command onto the consumer. 
    :rtype: None
    """
    global function_start_finish_debug
    global script_runner_debug
    global main_screen

    if function_start_finish_debug or script_runner_debug:
        print("Start run_script function.")

    # This is an absolute path. Strip to get filename.
    # Note that __file__ is this file's path.
    # Navigate to Test Scripts folder.
    this_files_path = path.dirname(path.abspath(__file__))

    # Tack on the Test Scripts sub-folder. Starting folder for dialog.
    initial_dir = path.join(this_files_path, "Test Scripts")

    # Dialog to get script to run.
    main_screen.filename = filedialog.askopenfilename(initialdir
                                                      =initial_dir,
                                                      title =
                                                      "Select Script:",
                                                      filetypes=
                                                      (("Python File",
                                                        "*.py"),
                                                       ("All Files",
                                                        "*.*")))

    # Read in script.
    with open(main_screen.filename, 'r') as my_script_file:
        script_data = my_script_file.readlines()
    my_script_file.close()

    ts.q_caller_gui.put(["run_script", [str(len(script_data))]
                         + script_data])

    if function_start_finish_debug or script_runner_debug:
        print("Stop run_script function.")


""" -------------------------    GUI Code    ----------------------- """


def strip_list_string(list_of_a_string: str) -> str:
    """
    This function takes in a string made from a list of a string,
    and strips away the quotes and list markers.    
    :param list_of_a_string: 
    :return: 
    """
    global function_start_finish_debug

    if function_start_finish_debug:
        print("Start strip_list_string function.")

    if list_of_a_string.split("""['""")[0] != list_of_a_string:

        # It's really a list of a string.
        if function_start_finish_debug:
            print("Stop strip_list_string function.")
        return list_of_a_string.split("""['""")[1].split("""']""")[0]
    else:

        # It's just a string without the list and quote characters.
        if function_start_finish_debug:
            print("Stop strip_list_string function.")
        return list_of_a_string


if "__main__" == __name__:
    main_screen = tk.Tk()
    main_screen.title("TestScript Python Window")

    # Send a message to LabVIEW.
    S = tk.Button(main_screen, text="Send Message to LabVIEW",
                  command=send_message_to_LabVIEW,
                  height=1, width=25)
    S.pack()

    # Run a script.
    RS = tk.Button(main_screen, text="Run Script",
                   command=run_script, height=1,
                   width=25)
    RS.pack()

    # Label for LabVIEW-to-python sent messages.
    LtoPSentLabel = tk.Label(main_screen,
                             text="LabVIEW-to-Python Message:",
                             height=1, width=50)
    LtoPSentLabel.pack()

    # Actual LabVIEW-to-python sent messages.
    LtoPSent = tk.Label(main_screen,
                        text="",
                        height=5, width=50,
                        wraplength="3i", justify="left",
                        anchor="w")
    LtoPSent.pack()

    # Label for LabVIEW-to-python reply messages.
    LtoPReplyLabel = tk.Label(main_screen,
                              text="LabVIEW-to-Python Reply Message:",
                              height=1, width=50)
    LtoPReplyLabel.pack()

    # Actual LabVIEW-to-python reply messages.
    LtoPReply = tk.Label(main_screen,
                         text="",
                         height=5, width=50,
                         wraplength="3i",
                         justify="left", anchor="w")
    LtoPReply.pack()

    # Label for python-to-LabVIEW sent messages.
    PtoLSentLabel = tk.Label(main_screen,
                             text="Python-to-LabVIEW Message:",
                             height=1, width=50, borderwidth=1)
    PtoLSentLabel.pack()

    # Actual python-to-LabVIEW sent messages.
    PtoLSent = tk.Label(main_screen,
                        text="",
                        height=5, width=50,
                        wraplength="3i",
                        justify="left", anchor="w")
    PtoLSent.pack()

    # Label for python-to-LabVIEW reply messages.
    PtoLReplyLabel = tk.Label(main_screen,
                              text="Python-to-LabVIEW Reply Message:",
                              height=1, width=50, borderwidth=1)
    PtoLReplyLabel.pack()

    # Actual python-to-LabVIEW reply messages.
    PtoLReply = tk.Label(main_screen,
                         text="",
                         height=5, width=50,
                         wraplength="3i",
                         justify="left", anchor="w")
    PtoLReply.pack()

    # Label for routine status updates.
    statusUpdatesLabel = tk.Label(main_screen, text="Script Status",
                                  height=1, width=50,
                                  borderwidth=1)
    statusUpdatesLabel.pack()

    sU = tk.Label(main_screen,
                  text="",
                  height=5, width=50,
                  wraplength="3i",
                  justify="left",
                  anchor="w")
    sU.pack()

    """ 
    Actual routine status updates. Allow use to scroll with
    mouse wheel. Old code.
    
    sUScroll = Scrollbar(main_screen)
    sU = tk.Text(main_screen, height=5, width=50)
    sUScroll.configure(command=sU.yview)
    sU.configure(yscrollcommand=sUScroll.set)
    sU.pack()
    """

    # Quit the python side of the communicator.
    Q = tk.Button(main_screen, text="Quit Python",
                  command=quit_gui,
                  height=1, width=25)
    Q.pack()


""" ------------------------    GUI Loops    ----------------------- """


def consumer_loop() -> None:
    """
    Begin queued state machine main loop. Data type is list:
    [state, LVPythonConnectorMessage]
    This loop is usually shut down by the keep_alive_loop or the user.
    This loop is governed by the queue ts.q_caller_gui.
    :rtype: None
    """

    global q_scr_cmd_engine
    global q_scr_runner
    global q_scr_id_register
    global const_message
    global gui_consumer_debug
    global function_start_finish_debug
    global script_runner_debug
    global loop_end_debug
    global q_gui

    if function_start_finish_debug:
        print("Start GUI consumer loop.")

    # For debug purposes.
    loop_counter = 0

    # Let everyone know this loop is running.
    ts.increment_loop_count()

    while ts.loop_continue:
        loop_counter += 1

        # The following get will usually error out. This is intentional.
        try:
            if gui_consumer_debug:
                print("gui_consumer counter at "
                      + str(loop_counter))
            q_message = ts.q_caller_gui.get(True, 1)

            # Separate out the state from the payload data.
            state = q_message[0]

            # If there's a payload, grab it; we don't want an
            # out-of-range error.
            q_data = q_message[1] if 1 < len(q_message) else None

            # Allow debugging.
            if gui_consumer_debug:
                print("GUI Consumer loop state = " + str(state) +
                      " data = " + str(q_data))

            if "A Initialize" == state:
                # Get everything started.
                pass

            elif "Blank" == state:
                # This case is for copying.
                ts.q_caller_gui.put(["Blank"])

            elif "Error" == state:
                # Try to print the error type.
                # GUI version:
                status_message = "Failure in caller GUI. " + \
                                 "We got error: " + str(q_data)
                user_update(status_message)

                # Start over.
                ts.q_caller_gui.put(["A Initialize"])

            elif "Exit" == state:
                # This function is needed, since otherwise the
                # loop would
                # sit here forever. Now we will get
                # back up to the top of
                # the loop and exit. This state is called only from
                # the keep_alive_loop.
                ts.loop_continue = False

            elif "LabVIEW-to-python Sent" == state:
                # We get the message (possibly a result)
                # from the communicator.
                q_gui.put(["ltop_sent_update",
                           trim_string(str(q_data))])
                try:
                    if " result" in q_data.command:
                        # The incoming message is the result of a
                        # python-to-
                        # LabVIEW command, because it contains the
                        # text " result". Relay the result to the
                        # script engine.
                        q_scr_cmd_engine.put([q_data.command,
                                              q_data])

                    elif "abort_script" == q_data.command:
                        # Abort a currently running Python script.
                        ts.script_running[str(q_data.script_id)] \
                            = False
                        del_script_results(str(q_data.script_id))

                    elif "HideWindow" == q_data.command:
                        # Hides the GUI window
                        q_gui.put(["hide_main_screen"])

                    elif "quit_python" == q_data.command:
                        # We quit all loops.
                        ts.q_caller_gui.put(["quit_gui"])

                    elif "run_script" == q_data.command:
                        # The incoming message is not the result of
                        # a python-to-LabVIEW command, because it
                        # does not end in the text " result". If
                        # it's a command to run a script,
                        # then send it to dedicated loop.

                        # Need to parse out code versus arguments.
                        size_of_code = int(q_data.data[0])
                        code_to_run = q_data.data[1:size_of_code+1]

                        # Flatten list into single string.
                        code_to_run = os.linesep.join(code_to_run)
                        arguments = q_data.data[size_of_code+1:]

                        # Debug prints:
                        if script_runner_debug:
                            print("Lines of code: " + str(size_of_code))
                            print("Code itself: " + code_to_run)
                            print("Arguments: " + str(arguments))

                        # Start the new thread dynamically.
                        my_script = threading.Thread(target =
                                                     scr_runner,
                                                     args =
                                                     [code_to_run,
                                                      arguments]
                                                     )
                        my_script.start()

                        # Now we need to get back the thread_id so
                        # that LabVIEW can register this script.
                        script_id = q_scr_id_register.get()
                        # Send registration message to LabVIEW.
                        reg_msg = LVPythonConnectorMessage(
                            "register", [],
                            script_id)
                        ts.q_python_to_LabVIEW.put(
                            ["Relay message to LabVIEW", reg_msg])

                    elif "ShowWindow" == q_data.command:
                        # Shows the GUI window
                        q_gui.put(["show_main_screen"])

                except:
                    # If for some reason q_data is not an
                    # LVPythonConnectorMessage type, then the above
                    # code will likely raise an exception. We're
                    # simply not interested in processing the error.
                    error_message = traceback.format_exc()

                    print("Got an error in the consumer loop:"
                          + error_message)

                    # Get error message back to user, if possible.
                    ts.q_caller_gui.put(["Error", error_message])

            elif "LabVIEW-to-python Reply" == state:
                # We get the reply Python sent back to LabVIEW.
                q_gui.put(["ltop_reply_update",
                           trim_string(str(q_data))])

            elif "python-to-LabVIEW Sent" == state:
                # We get the message Python sent to LabVIEW.
                q_gui.put(["ptol_sent_update",
                           trim_string(str(q_data))])

            elif "python-to-LabVIEW Reply" == state:
                # We get the LabVIEW reply back from the
                # communicator.
                q_gui.put(["ptol_reply_update",
                           trim_string(str(q_data))])

            elif "quit_gui" == state:
                # Quit everything.
                # ts.loop_continue = False
                # New code: tell LabVIEW to start its usual shutdown.
                quit_message = LVPythonConnectorMessage("quit_python",
                                                        [], -1)
                ts.q_python_to_LabVIEW.put(
                    ["Relay message to LabVIEW", quit_message])

            elif "run_script" == state:
                # The incoming message is not the result of
                # a python-to-LabVIEW command, because it
                # does not end in the text " result". If
                # it's a command to run a script,
                # then send it to dedicated loop.

                # Need to parse out code versus arguments.
                size_of_code = int(q_data[0])
                code_to_run = q_data[1:size_of_code + 1]

                # Flatten list into single string.
                code_to_run = os.linesep.join(code_to_run)
                arguments = q_data[size_of_code + 1:]

                my_script = threading.Thread(target =
                                             scr_runner,
                                             args =
                                             [code_to_run,
                                              arguments]
                                             )
                my_script.start()

                # Now we need to get back the thread_id so
                # that LabVIEW can register this script.
                script_id = q_scr_id_register.get()
                # Send registration message to LabVIEW.
                reg_msg = LVPythonConnectorMessage(
                    "register", [],
                    script_id)
                ts.q_python_to_LabVIEW.put(
                    ["Relay message to LabVIEW", reg_msg])

            elif "send_message_to_LabVIEW" == state:
                """ 
                This state uses the q_python_to_LabVIEW queue to 
                relay a message to LabVIEW.                
                """
                if isinstance(q_data, LVPythonConnectorMessage):
                    ts.q_python_to_LabVIEW.put(
                        ["Relay message to LabVIEW", q_data])
                else:
                    ts.q_python_to_LabVIEW.put(
                        ["Relay message to LabVIEW", const_message])

            else:
                # GUI version:
                status_message = \
                    "Oops, we enqueued a non-existent" \
                    + " state in the caller communicator loop." \
                    + str(state)
                user_update(status_message)
        except queue.Empty:
            # expected timeout
            pass
        except:
            if gui_consumer_debug:
                print("GUI consumer loop got error: ")
                traceback.print_exc(file=sys.stdout)

    # End while loop.
    # Good practice explicitly to close the queue.
    try:
        # Flush the queue before closing.
        ts.flush_queue(ts.q_caller_gui)
    except:
        pass

    # After the main screen is destroyed, let the user know in the
    # cli that the code is done executing. This may have already been
    # done, because we want all loops to be done. Throw away errors.
    # main_screen.quit()
    try:
        q_gui.put(["quit_main_screen"])
    except:
        pass

    # Let everyone else know this loop is done.
    ts.decrement_loop_count()

    if function_start_finish_debug or loop_end_debug:
        print("Stop gui consumer loop.")


def script_update_loop() -> None:
    """
    This loop provides the ability for the LabVIEW-to-python
    communicator, or the python-to-LabVIEW communicator, to push
    status update messages to the UI, whatever that is. 
    We simply enqueue a string, and print it out. The caller worries
    about exactly what string to enqueue. We will implement this
    differently depending on the kind of GUI.
    This is a very simple queued state machine on the q_script_update
    queue.
    :rtype: None
    """

    global q_scr_cmd_engine  # Queue for the script command engine.
    global script_update_debug
    global function_start_finish_debug
    global loop_end_debug

    if function_start_finish_debug:
        print("Start script_update_loop.")

    # For debug purposes.
    loop_counter = 0

    # Let everyone know this loop is running.
    ts.increment_loop_count()

    while ts.loop_continue:
        loop_counter += 1

        if script_update_debug:
            print("script update counter at " + str(loop_counter))

        # The following get will usually timeout. We throw away
        # the exception raised, because we want to make sure this
        # loop exits when loop_continue goes false.
        try:
            # Initialize string accumulator.

            q_message = ts.q_script_update.get(True, 1)
            internal_message = str(q_message[0] + "\n")
            # We got one message if queue.Empty didn't trigger,
            # wait 0.1s for
            # more messages to accumulate and get via while loop below

            time.sleep(0.1)
            # To improve performance, get a lot of messages
            # all at once, and send them in one fell swoop.
            while not ts.q_script_update.empty():

                q_message = ts.q_script_update.get(False)
                internal_message = internal_message \
                    + str(q_message[0]) + "\n"
                # Put in debugging.
                if script_update_debug:
                    print("Status update info: " + str(q_message))

            # Update the GUI.
            q_gui.put(["su_update", trim_string(internal_message)])

            # Update LabVIEW. Do this the same way the action
            # works, and the query function works. See if this fixes
            # the bug re: interfering with the keep-alive loop.
            update_message = LVPythonConnectorMessage(
                    "update_status", [internal_message], -1)
            if script_update_debug:
                print("q_scr_cmd_engine script_update: "
                      + str(update_message))
            q_scr_cmd_engine.put(["Command LabVIEW",
                                 update_message])

        except queue.Empty:
            if script_update_debug:
                print("Script update queue timeout.")
            pass
        except:
            if script_update_debug:
                print("Script update loop got error: "
                      + traceback.format_exc())

    # End while loop.    
    # Good practice explicitly to close the queue.
    try:
        # Flush the queue before closing.
        ts.flush_queue(ts.q_script_update)
    except:
        pass

    # Let everyone else know this loop is done.
    ts.decrement_loop_count()

    if function_start_finish_debug or loop_end_debug:
        print("Stop script_update_loop.")


def scr_cmd_engine_loop() -> None:
    """
    This loop provides the ability for the LabVIEW-to-python
    communicator to process scripts written in
    python. The scripts will include function
    calls that interact only with this loop. This loop, in turn, will
    interact with the script_update_loop and the consumer_loop to 
    update the GUI. 
    Since the queued state machine here will not directly interact with
    the wrc module, we need not define the queue in that module.
    The controlling queue will be q_scr_cmd_engine.
    Defined functions:
        set - sets the value of a variable in LabVIEW.
        get - gets the value of a variable in LabVIEW.
        query - first sets, then gets the value of a variable in
                    LabVIEW.
    :rtype: None
    """

    global q_scr_cmd_engine
    global l_scr_cmd_engine_result
    global l_scr_cmd_engine_lock
    global script_command_engine_debug
    global function_start_finish_debug
    global loop_end_debug

    if function_start_finish_debug:
        print("Start scr_cmd_engine_loop.")

    # Make sure to run the initialize state.
    q_scr_cmd_engine.put(["A Initialize"])

    # For debug purposes.
    loop_counter = 0

    # Let everyone know this loop is running.
    ts.increment_loop_count()

    while ts.loop_continue:
        loop_counter += 1

        # Make sure the loop does not eat up CPU time unnecessarily.
        try:
            q_message = q_scr_cmd_engine.get(True, 1)
            if script_command_engine_debug:
                print("script command engine counter at "
                      + str(loop_counter) + ": " + str(q_message))

            # Separate out the state from the payload data.
            state = q_message[0]

            # If there's a payload, grab it, but we don't want an
            # out-of-range error.
            q_data = q_message[1] if 1 < len(q_message) else None

            # Do debugging here:
            if script_command_engine_debug:
                print("Script command engine state: " + str(state) +
                      " And data: " + str(q_data))

            if "A Initialize" == state:
                # Get everything started.
                pass

            elif "Blank" == state:
                # This case is for copying.
                ts.q_caller_gui.put(["Blank"])

            elif "Command LabVIEW" == state:
                # Here we call the communicator's queue with the
                # msg:
                ts.q_python_to_LabVIEW.put(["Relay message"
                                            + " to LabVIEW",
                                            q_data])

            elif "set result" == state or "action result" == state:
                # Now we need to pass back to our function, via
                # the reply queue, the result from the LabVIEW op.
                l_scr_cmd_engine_lock.acquire()
                l_scr_cmd_engine_result.append(q_data)
                l_scr_cmd_engine_lock.release()
                if script_command_engine_debug:
                    print("Script command engine put " + str(q_data))
                    print(" into the result list.")
                    print("Whole result list is: " +
                          str(l_scr_cmd_engine_result))

            else:
                print("Oops, got to a non-state in the" +
                      " script engine: " + str(state) + ".")

        except queue.Empty:
            # expected timeout
            pass
        except:
            if script_command_engine_debug:
                print("Script command engine got error: "
                      + traceback.format_exc())

    try:
        # Flush the queues before closing.
        ts.flush_queue(q_scr_cmd_engine)
        l_scr_cmd_engine_result.clear()
    except:
        pass

    # Let everyone else know this loop is done.
    ts.decrement_loop_count()

    if function_start_finish_debug or loop_end_debug:
        print("Stop scr_cmd_engine_loop function.")


def scr_runner(script_to_run: str, script_to_run_data: tuple) \
        -> None:
    """
    This function's sole purpose in life is to run a
    script. It gets the lines of the script from the first argument,
    the arguments to the script from the second argument,
    and attempts to execute that python script.
    :return: None
    """

    global q_scr_runner
    global l_scr_cmd_engine_result
    global l_scr_cmd_engine_lock
    global script_runner_debug
    global function_start_finish_debug
    global number_abort_messages
    global q_scr_id_register

    # Convert to list.
    if script_runner_debug:
        print("scr_runner function called with script: "
              + script_to_run)
        print("scr_runner function called with data: " +
              str(script_to_run_data))

    if function_start_finish_debug:
        print("Start scr_runner_loop.")

    # For debug purposes.
    loop_counter = 0

    # Register thread_id as script_id:
    script_id = threading.get_ident()
    q_scr_id_register.put(script_id)

    # script_to_run_data is a list, and any elements past
    # the zeroth element are arguments to be passed onto the
    # script via the locals() dictionary.

    # Do debugging here:
    if script_runner_debug:
        print("Script runner info: "
              + str(script_to_run)
              + str(script_to_run_data))

    # Initialize the list so we don't get artifacts.
    arguments = None

    if 0 < len(script_to_run_data):
        # All the elements are the arguments. We assume they've been
        # split out earlier.
        arguments = script_to_run_data
    else:
        arguments = None

    try:
        # Execute the python code in the file dynamically.
        # The arguments to the script should be available in
        # the locals() environment as "arguments".
        ts.script_running[str(script_id)] = True
        number_abort_messages[str(script_id)] = 0

        # Execute the script with the current environment's
        # globals and locals.
        exec(script_to_run, globals(), locals())
        if not ts.script_running[str(script_id)]:
            # Script was aborted.
            script_update("Script aborted.")

    except:
        if not ts.script_running[str(script_id)]:
            # Script was aborted, or not running for some reason.
            user_update("Script aborted. " + traceback.format_exc())
        else:
            # Script stopped before its flag went low. This needs to be
            # a user_update.
            user_update("Got an error in the script runner loop: "
                        + traceback.format_exc())
        if script_runner_debug:
            print("Got an error in the script runner loop: "
                  + traceback.format_exc())
            print(str(script_to_run_data))

    # Regardless of how the script finished, it's finished:
    ts.script_running[str(script_id)] = False

    if function_start_finish_debug:
        print("Stop scr_runner_loop.")


""" ---------------------    Exposed Functions    ------------------ """


def action(command: str, data: list = None, timeout: int = 1,
           update: bool = True) \
        -> LVPythonConnectorMessage:
    """
    This is an exposed function that allows the user to
    set a variable in LabVIEW corresponding, typically, to a hardware
    output.
    :param command: str
    :param data: str
    :param timeout: int
    :param update: bool
    :rtype: LVPythonConnectorMessage
    """

    global q_scr_cmd_engine         # To the script command engine.
    global l_scr_cmd_engine_result  # From the script command engine.
    global function_start_finish_debug
    global function_debug

    if function_start_finish_debug:
        print("Start action.")

    # Just to be on the safe side, get the thread_id as script_id.
    script_id = threading.get_ident()

    result = LVPythonConnectorMessage("Script aborted.", [])

    if not ts.script_running[str(script_id)]:
        if function_debug:
            print("Script aborted.")
        return result

    # If update is high, let user know we are starting the action.
    if update:
        script_update("Starting action with:"
                      + " command = " + command
                      + " and data = " + trim_string(str(data))
                      + " with timeout = " + str(timeout))

    # Scrub input data to make sure it is a list of strings.
    if None is not data:
        data = [str(i) for i in data]

    # 1. Package up data into LVPythonConnectorMessage type.
    # 2. Send to script engine.
    # 3. Get message reply back from LabVIEW via the script engine.
    send_msg = LVPythonConnectorMessage(command, data, script_id)
    send_msg.assign_message_id()

    # For debugging:
    if function_debug:
        print("starting action: " + str(send_msg))
    try:
        q_scr_cmd_engine.put(["Command LabVIEW", send_msg])
    except:
        print("Exception in queue put")
    try:
        # timeout here should be adjusted to reflect the physical
        # process your action is taking.
        # Need to loop through list and only remove relevant items
        # for this script_id (thread_id) and python_message_id.
        result = get_script_result(timeout, send_msg.get_message_id())

        # Debugging:
        if function_debug:
            print("Action result is: " + str(result))
    except queue.Empty:
        # Timed out.
        script_update("Timed out waiting for LabVIEW response"
                      + " in command " + command)
        if function_start_finish_debug or function_debug:
            print("Stop action. Queue empty exception.")

        # Send exception to the caller.
        raise
    except:
        script_update("Got an error in the action command " + command
                      + ": " + traceback.format_exc())
        if function_start_finish_debug or function_debug:
            print("Stop action. General exception.")
        raise

    # Test result. If the phrase "- Error" appears in any
    # of the data portions of result, then we need to return
    # that string, and raise an error. It is the job of the script
    # to handle the error.
    # Let the GUI know we finished successfully.
    for test_string in result.data:
        if "- Error" in test_string:
            script_update(trim_string(test_string))

            # Enable debugging.
            if function_debug:
                print(str(test_string))
            if function_start_finish_debug:
                print("Stop action. - Error in test_string.")
            raise ValueError(test_string)

    # script_update("Finished action successfully.")
    if function_start_finish_debug or function_debug:
        print("Stopped action successfully.")
    return result


def script_update(status: str) -> None:
    """
    This is simply a wrapper for the ts.q_script_update.put function.
    This function, though, needs to be called from within a script,
    unlike the user_update function.
    :param status: str
    :return: None
    """
    global function_start_finish_debug
    global number_abort_messages

    # Get the thread id as script_id, for use later:
    script_id = threading.get_ident()

    if function_start_finish_debug:
        print("Start script_update function.")

    if ts.script_running[str(script_id)]:
        ts.q_script_update.put([str(script_id) + " " + status])
    elif number_abort_messages[str(script_id)] < 1:
        # Only do this once per script. The script might have lots
        # of script_update calls in it. We pass on any past the first
        # one past the abort.
        ts.q_script_update.put([str(script_id) + " Script aborted."])
        number_abort_messages[str(script_id)] += 1

    if function_start_finish_debug:
        print("Stop script_update function.")


def user_update(status: str) -> None:
    """
    This is simply a wrapper for the ts.q_script_update.put function.
    Unlike the script_update function, this function doesn't care
    whether it's being called in a script or not. 
    :param status: str
    :return: None
    """
    global function_start_finish_debug

    if function_start_finish_debug:
        print("Start user_update function.")

    ts.q_script_update.put([status])

    if function_start_finish_debug:
        print("Stop user_update function.")


def sleep(seconds: float) -> None:
    """
    This is an exposed function that allows for a modified sleep
    on a 10ms edge that will break out if loop_continue goes false or
    if the user aborts the script.
    :param seconds: float - seconds to wait
    :return: None
    """

    # Get the thread id as script_id, for use later:
    script_id = threading.get_ident()

    if not ts.script_running[str(script_id)]:
        return None

    if function_start_finish_debug:
        print("Start sleep function.")

    start_time = time.perf_counter()

    # Sleep for small periods of time. Note that the time.time
    # function is deprecated. We use the time.perf_counter
    # function instead. This loop waits for 'seconds' seconds.
    while ts.loop_continue and ts.script_running[str(script_id)] and \
            time.perf_counter() - start_time < seconds:
        time.sleep(0.005)

    if function_start_finish_debug:
        print("Stop sleep function.")


""" -------------------------    Cleanup    ------------------------ """


if "__main__" == __name__:

    # Start the loops in separate threads.
    ts.spawn_thread(consumer_loop)
    ts.spawn_thread(script_update_loop)
    ts.spawn_thread(scr_cmd_engine_loop)

    # Hide the GUI if the connection is over localhost. Otherwise,
    # show it.
    if 'localhost' == ts.address:
        main_screen.withdraw()

    # and start the GUI. We need a way to make the GUI functions all
    # happen inside the main thread. Use a queue to do this.
    q_gui = multiprocessing.Queue()

    # Let everyone know we're running.
    ts.increment_loop_count()

    def pass_command_to_gui():
        """
        This is a simple queue consumer to manage q_gui. All we ever do
        here is pass things on to the GUI.
        :return: 
        """
        global gui_consumer_debug
        global main_screen
        global LtoPReply
        global LtoPSent
        global PtoLReply
        global PtoLSent
        global sU

        # We expect a list of two strings: command, payload. Sometimes
        # there will not be a payload. It might be a list of one.
        if ts.loop_continue:
            try:
                while not q_gui.empty():
                    # Simply poll the queue. We expect it to time out
                    # most of the time.
                    q_message = q_gui.get(True, 0.1)
                    if gui_consumer_debug:
                        print(str(q_message))

                    # The first element is always the command.
                    command = q_message[0]

                    # Some GUI process expect a parameter, such as a
                    # message or payload. Just take first 200 chars.
                    if 1 < len(q_message):
                        payload = q_message[1]
                        if gui_consumer_debug:
                            print("GUI Command was " + str(command) +
                                  " and payload was " + str(payload))
                        # The direct GUI manipulations happen here.
                        if "ltop_sent_update" == command:
                            LtoPSent.config(text=str(payload))
                        elif "ltop_reply_update" == command:
                            LtoPReply.config(text=str(payload))
                        elif "ptol_sent_update" == command:
                            PtoLSent.config(text=str(payload))
                        elif "ptol_reply_update" == command:
                            PtoLReply.config(text=str(payload))
                        elif "su_update" == command:
                            sU.config(text=str(payload))
                            """ Old code.
                            # Put the new message in and scroll to
                            # bottom.
                            sU.insert('end', strip_list_string(payload)
                                      + linesep)
                            sU.see('end')
                            """
                        else:
                            pass

                    # These GUI commands don't have any parameters.
                    else:
                        if "show_main_screen" == command:
                            main_screen.deiconify()
                        elif "hide_main_screen" == command:
                            main_screen.withdraw()
                        elif "quit_main_screen" == command:
                            main_screen.withdraw()
                            main_screen.quit()
                            main_screen.destroy()
                        else:
                            pass

            # We timed out on the q.get function: throw the exception
            # away.
            except:
                pass
            # This command basically iterates the function call.
            main_screen.after(50, pass_command_to_gui)

        # Time to exit.
        else:
            main_screen.withdraw()
            main_screen.quit()
            main_screen.destroy()


    # Start the after function to process GUI commands.
    main_screen.after(50, pass_command_to_gui)

    # Make clicking the red X equal to Quit button, for graceful
    # shutdown.
    main_screen.protocol("WM_DELETE_WINDOW", quit_gui)

    # Start the GUI main loop.
    main_screen.mainloop()

    # Let everyone else know this loop is done.
    ts.decrement_loop_count()

    if loop_end_debug:
        print("Exited main GUI loop.")

    # Don't exit until the TestScript_connector.py file is done.
    # Definitely not interested in the exception possibly raised here.
    try:
        ts.q_quit.get(True, 3)
    except:
        pass

    # Once the GUI main loop is done, exit the system.
    sys.exit(0)
