# coding=utf-8

"""
The exposed functions are:

def action(command: str, data: list = None, timeout: int = 1) \
        -> LVPythonConnectorMessage:
def script_update(status: str) -> None:
def user_update(status: str) -> None:
def sleep(seconds: float) -> None:

You would call them like this:
    action("voltage", "3")

Use the command

    sleep(5)
    
to sleep in the script for five seconds. Use the command

    script_update("Here's a little message to myself.")

to print something to the GUI.

The expression locals()['arguments'] produces a list of strings
supplied from the LabVIEW script call. 

"""


""" --- Setup --- """

script_update("Gonna wait for 2 seconds.")
sleep(2)

""" --- Main --- """

try:
    script_update("Expect print arguments here:")
    script_update(trim_string(str(locals()['arguments'])))
    script_update("Did we get printing?")
except:
    print("Got an error in the script:"
          + str(sys.exc_info()[0]))

""" --- Cleanup --- """

script_update("Gonna wait for 2 seconds.")
sleep(2)
script_update("Done with the script.")
