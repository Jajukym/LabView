import MySQLdb.connections
import os
import sys
###ssl certs needed to connect to icons db
ssl = {'cert' : 'C:\labview db certs\client-cert.pem',
       'key': 'C:\labview db certs\client-key.pem',
       'ca': 'C:\labview db certs\ca.pem'}

###this is how python connects to the db
conn = MySQLdb.connections.Connection(
    host='iconqaapi.iconfitness.com',
    user='remote',
    passwd='IconQ@!2019!remote',
    port = 3306,
    db='LabVIEW',
    ssl = ssl    
)


###this is to catch the parameter when this .exe is run example(thispython.exe c:\test\log.txt) will store the location of log.txt
if len(sys.argv) > 1:
    filelocation = sys.argv[1]

##Swap these file comments out before its built
#file = open(filelocation)
file = open('C:\\logsConsole\\Test3 3ÔÂ-13-20_133116.txt')
f = file.read(-1)

sendarray = []
###headers need to be in this format example: "Time,Vendor_Name,PO,FW"
###And exact wording to the DB table
header = "Time,Inspection_Point,Vendor_Name,Vendor_Number,Inspector,Station,PO,PO_Line,Part_Name,Part_Number,Serial_Number,Cosmetic,Voltage,Current,Firmware,Calibrate,Display,KeyCode,BLEConnect,Speed,RPM,MaxSpeed,PWMFrequency,QuickSpeed,MaxPWM,Down,Up,ONE,Pulse,Fan,Audio,TV,USB,IdleCurrent,SurgeCurrent,QuickResistance,Decrease,Increase,Lowest,MinIncline,MaxIncline,QuickIncline,Down1,Up1,ZERO,CSAFE"

###This section is to open the file(log.txt) and send it into a text based array, and skips past the headers to the data
def Seek(f):
    skip = False
    tmp = ''
    a = []
    for i in f:
        if i == "\t" or i == "\n":
            a.append(tmp)
            tmp = ''
            continue
        else:
            tmp = tmp + i
            continue
    for i in range(100):
        a.pop(0)
        if a[0] == 'CSAFE ':  ###header needs to end in this string
            a.pop(0)
            a.pop(0)
            break
    return a

###This section will add the first row of data to a temp array and add failed to any missing headers and include a 'null' if the last space has a ''
def Upload(a):
    for i in a:
        if len(sendarray) == 46:
            if sendarray[0] == '':
                sendarray.pop(0)
                a.pop(0)
            if a[45] == None:
                a.append('')
            if sendarray[45] == '':
                sendarray[45] = 'NULL'
                a[45] = 'NULL'
                ###Sends the sql command to insert into the specified db
                cursor.execute("INSERT INTO LabVIEW.ConsoleTest (" + header + ") VALUES " + str(tuple(sendarray)))
                return (sendarray,a)
        if i != 'FAILED':
            sendarray.append(i)            
        elif i == 'FAILED':
            for j in range(46 - len(sendarray)):
                sendarray.append('FAILED')
                if (len(sendarray) != 46):
                    a.insert(len(sendarray),'FAILED')
            break
        continue
    try:
        if len(sendarray) == 46:
            cursor.execute("INSERT INTO LabVIEW.ConsoleTest (" + header + ") VALUES " + str(tuple(sendarray)))
    except Error as e:
        print('Error: ',e)
    finally:
        return (sendarray,a)
    return (sendarray,a)


###This section will remove the 29 items from (a) so you can send the next round into the Upload()
def pop45(a):
    try:
        for i in range(46):
            a.pop(0)
        return a
    finally:
        return a


###This is needed when you build it into an .exe file
if (__name__ == "__main__"):
    cursor = conn.cursor()      ###This just assigns the cursor for easier usage
    a = Seek(f)
    sendarray,a = Upload(a)
    while len(a) >=10:          ###This cycles throught the whole log.txt file
        sendarray = []
        a = pop45(a)
        sendarray,a = Upload(a)

    conn.commit()               ###This makes it permanant on the db
    conn.close()                ###Closes the connection to db






###Just some quick test copy paste commands
#cursor.execute("SELECT * FROM LabVIEW.Test LIMIT 20")      ###Basic select statment, remove/change "LIMIT 20" for bigger query
#cursor.fetchall()                                          ###Needed to see the "SELECT" command
#cursor.execute("INSERT INTO LabVIEW.Test (Tech,Serial) VALUES('eqd guy', 'kk1234567890123456')") ###Another example of INSERT command


### Reserved Space
