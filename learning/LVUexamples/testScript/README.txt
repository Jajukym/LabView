TestScript 1.3.0

TestScript has been written to be as framework-independent as possible,
so you should be able to drop it into your LabVIEW codebase with very
little effort. Everything in the TS.lvlib you generally shouldn’t 
touch, unless you find a need (let us know, please!). You can see how
the 
    Scripting Example.vi 
handles messages back and forth. In the 
    Scripting Example.vi, 
the key place where user-defined functions are 
handled is in the case structure following the Dequeue function 
(tied to the callback VI, which you will need to customize for your 
message-handling mechanism), where you have the x_dialog_user case, the 
x_get_waveform_data case, and so on. That’s where you would put your 
logic on the LabVIEW side. There are various vi’s in the Methods 
virtual folder of TS.lvlib that you’ll need to call at appropriate 
moments, just like in the example. 
On the Python side, you would change the 
    Python Core\TestScript_application_specific_functions.py 
file. Mostly, user-defined functions are just going to be wrappers 
for the action function, which is defined in the 
    TestScript_gui_and_exposed_functions.py 
file. The idea is to create functions so that your scripts are as 
bare-bones as possible: no imports, no function definitions. You just 
code your script! And, since Python handles conditionals and looping 
with a very easy-to-understand syntax, you have the advantage of 
scripting in one of the easiest scripting languages out there. It’ll 
require minimal training to get your scripts up and running! Also, 
note that all scripts you write should be in the Test Scripts folder, 
which should be next to the 
    TestScript_gui_and_exposed_functions.py 
file. All that said, please let us know at 
    TestScript@winemantech.com 
if you’re having trouble creating your own functions: we’d love to 
help you out!


Glossary

TestScript: the Python/LabVIEW Connector
LabVIEW: a basic LabVIEW file is a *.vi file, which stands for
    "virtual instrument". It is a graphical programming language 
    managed by National Instruments
Python: a programming language originated by Guido van Rossum in 1991,
    and has now grown to an immense popularity due to its
    inter-operability, easy-to-read syntax, and utility for data 
    science. The basic file is a *.py file.
LabVIEW Server: a piece of LabVIEW code that handles the TCP connections
    with Python as well as the messaging to and from the main LabVIEW
    application.
Callback (CB):  the code the LabVIEW server runs that sends a message
    from the LabVIEW Server to the LabVIEW application.
Message Handler: LabVIEW code in the LabVIEW application that retrieves
    actions and script updates from Python and sends responses to the
    LabVIEW Server.
Run Script: when the LabVIEW code sends a message to Python telling it
    to run a script.
LabVIEW Queues: interfaces between the Message Handler and the LabVIEW
    Server. The "pylvq" is directed from the LabVIEW Server to the
    Message Handler. The "LvPy" queue is directed from the Message
    Handler to the LabVIEW Server.
Action: A Python-to-LabVIEW message with an automatic reply from the
    LabVIEW Server and a response from the Message Handerl.
Script Update: A Python-to-LabVIEW message with an automatic reply from
    the LabVIEW Server.
Response: Python actions wait until the LabVIEW Application sends this
    message back to Python, optionally with a payload.

    
Note on fonts: for best viewing, add the following lines to the
[LabVIEW] section of your LabVIEW.ini file:

appFont="Segoe UI" 13
systemFont="Segoe UI" 13
dialogFont="Segoe UI" 13
CurrentFont="Segoe UI" 13
FPFont="0" 13
BDFont="0" 13


Changelog:

TestScript 1.0.0: Original Release.

- Connectivity
- Scripting
- Python GUI

TestScript 1.0.1: Cleaned up Release.

- Added "Launch Python" button filter to prevent starting Python 
  multiple times
- Cleaned up Scratch folder

TestScript 1.0.2: A Few Bug Fixes.

- Fixed Python GUI bugs
- Bound regular Enter key and Return key the same
- Improved LabVIEW time stamp formatting
- Fixed Clear Status button functionality

TestScript 1.0.3: Speed and Timing Bug Fixes.

- Improved overall performance
- Made LabVIEW dialogs asynchronous to prevent unwanted timeouts
- Split python-to-LabVIEW event handling loop away from UI to prevent
  blocking.
- Added example for array handling

TestScript 1.1.0: Focus on Message Speed.

- Switched to blocking queues for performance
- Switched to queue-based status updates for performance
- Eliminated many waits for performance
- Added optional boolean in action function to turn off its updates
- Changed sys.exc calls to traceback.print_exc calls for better 
  debugging
- Python tkinter GUI stops much faster now
- Changed some times to allow faster tkinter performance
- Switched to hybrid mode for TCP messaging: if messages are smaller
  than 8182 bytes, use the old peek method. Otherwise, use a new
  method relying on prepended message size. This allows the user to 
  transmit up to 2 GB messages, but retains the performance of the old
  system for many small messages. This is paired with dynamic socket
  timeouts so that messages have enough time to get across.
- Status updates use trimmed strings for speed. 
- All reply messages gut the data out of them for speed.
- Switched to single TCP Write for performance. 

TestScript 1.1.1: A Few Bug Fixes.

- Fixed starting bug: messages enqueued before
  TestScript_gui_and_exposed_functions.py loops started were being
  ignored. 
- Added 8-byte handshake when TCP connection is started, including 
  error handling.
- Added queue list to documentation.
- Fixed shutdown bug: if Python goes away during a script, TestScript
  now handles this more intuitively.

TestScript 1.1.2: Focus on Startup and Shutdown Speed.

- Startup is much faster, even on Linux. Fixed this by looking at
  the create_connection timeout, as well as wiring a False to the 
  Resolve Remote Address in Create Listener.vi. 
- Shutdown is faster on Windows. Fixed this by allowing inner loop
  inside the LabVIEW-to-Python loop in Server.vi to exit on
  quit_python command, as well as an error condition.
- Added the ability to define the ports used, both on the LabVIEW side
  and on the Python side via command-line interface.
- Added simple LabVIEW adder example, and simple Python adder example.
- Now scrubbing data input on action function to simplify script syntax.
- Fixed race condition on continuous running by forcing Close.vi to wait
  until the server is down before exiting.
- Added two minimal working examples of TestScript: 
  Simple Scripting Example - Add on LabVIEW Side.vi, which has three
  numbers in the Python script simple_lv_adder.py that it sends to 
  LabVIEW for adding.
  Simple Scripting Example - Add on Python Side.vi, which allows the 
  user to type in an array of numbers, add them up on the Python side,
  and return the result to LabVIEW.
- Changed Close.vi: loop to test shutdown now has 5000 iteration max.
- Got rid of Initialize global variable.
- Fixed reconnect bugs: not calling close_tcp correctly, and increased
  number of retries to 1000 (equivalent to 100 seconds).
- Added 1 sec wait to TS.lvlib:Shutdown Python Connector.vi. This 
  greatly improves performance when running an example continuously
  (constantly starting and stopping Python). 
  
TestScript 1.1.3: Focus on Stability, Especially When Started and
Stopped Many Times.

- TestScript now has a smarter shutdown: it lets LabVIEW know when it
  has mostly shutdown. This allows faster re-starting of TestScript
  and fewer edge effects.
- All Send/Reply cycles are completely paired, and viewed as atomic.
  No business logic is allowed to happen unless both messages go through
  correctly.
- Recreating listener on larger variety of network errors, not just 
  62 and 66. Added Error 267 handling in Launch Python Connector for
  better error message. 
- TCP connection more uniform across loops. Changed exception handling
  on Python side to mirror LabVIEW side more closely.
- Now sending script errors back to user if possible.
- Now flushing TCP buffers on both LabVIEW and Python sides in case of
  errors.
- LabVIEW TCP reads are now more parallel to the Python versions.  
- Using select.select to poll sockets for data. 
- Fixed possible memory leak by explicitly closing TCP refnums in
  the LabVIEW server.
- Fixed Quit Python issue when quitting from the tkinter GUI.  
- Tightened up LabVIEW code to eliminate all coercion dots, and closing
  all refnums. 
  
TestScript 1.2.0: Multiserver. TestScript may be instantiated any
number of times, with different combinations of IP addresses and ports,
of course. 

- Each server is identified with a customer-provided Server Alias.
- Internally, a server/Python instance combination is identified with
  the string IP Address:Keep-Alive Port (e.g., "localhost:9007"). This
  is called the LabVIEW Server ID. The LabVIEW Server ID now travels on 
  every message. There is a function that will produce the Server Alias
  given the LabVIEW Server ID.
- The base connector message also includes a Python Message ID, which,
  for each Python instance, is a unique message identifier. This allows
  the customer to use try/except clauses in scripts without worrying
  if the result from a previous step could count as the result of a 
  subsequent step.

TestScript 1.3.0: Performance efficiency gain, sub-modules, increased
documentation, flexibility in script locations.

- TestScript now polls the Python GUI much less frequently; this will 
  not be noticed since the Python GUI is more for debugging than 
  anything else. The result of the lower polling rate is a far lower CPU 
  usage. 
- Also, the TestScript_application_specific_functions.py file has an
  addition function defined in it which allows developers to organize
  their application-specific functions into submodules. Calling the 
  app_specific_import function like this: 
  app_specific_import("my_functions.py") allows developers to write
  application-specific functions in a more modular fashion.
- TestScript now ships with additional documentation in the 
  form of a pdf file illustrating graphically the relationship among
  the different pieces of TestScript and the developer's code. This is
  the Visual Explanation.pdf file.
- Moved Initialize Python Global Variables into private: no need for
  the developer to worry about this. Did not change API of Get Status.
- Added Synchronous Dialog example that is simpler to use than the 
  existing one. Also changed the Dialog Example.vi to poll the Stop
  variable so that it is not orphaned if TestScript stops.
- Changed the script launching mechanism to allow scripts to live 
  anywhere accessible to the side that is launching the script. So if 
  you are launching a script from LabVIEW, then the machine running 
  LabVIEW must have access to the script. If you are launching a script
  from Python, then the machine running Python must have access to the
  script. Note that, while starting a script from LabVIEW allows you
  to call a script with arguments, calling from Python does not.
- Improved script debugging by sending exceptions to LabVIEW more
  robustly. 
- Fixed subtle bug for medium-sized messages: if CRLF wasn't coming in,
  logic was ragged. Now we let the read loop come around again with a
  no-op.  