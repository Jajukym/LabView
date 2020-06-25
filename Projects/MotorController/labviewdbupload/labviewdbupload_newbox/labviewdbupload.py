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
file = open('C:\\logsController\\MC1648DLS May-18-20_151959.txt')
f = file.read(-1)

sendarray = []
###headers need to be in this format example: "Time,Vendor_Name,PO,FW"
header = "Time,Inspection_Point,Vendor_Name,Vendor_Number,Inspector,Station,PO,PO_Line,Part_Name,Part_Number,Serial_Number,FW,ILimit,IRcomp,Vsensor,Vload,tachSense,inclineSense,IRunning,Vpot_Mid,Vpot_Low,Vpot_High,IRcomp_Measure,Current_Limit,Foldback"

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
        if a[0] == 'Foldback ':
            a.pop(0)
            a.pop(0)
            break
    return a

###This section will add the first row of data to a temp array and add failed to any missing headers and include a 'null' if the last space has a ''
def Upload(a):
    for i in a:
        if len(sendarray) == 25:
            if sendarray[0] == '':
                sendarray.pop(0)
                a.pop(0)
            if a[24] == None:
                a.append('')
            if sendarray[24] == '':
                sendarray[24] = 'NULL'
                a[24] = 'NULL'
                ###Sends the sql command to insert into the specified db
                cursor.execute("INSERT INTO LabVIEW.ControllerTest1 (" + header + ") VALUES " + str(tuple(sendarray)))
                return (sendarray,a)
        if i != 'FAILED':
            sendarray.append(i)            
        elif i == 'FAILED':
            for j in range(25 - len(sendarray)):
                sendarray.append('FAILED')
                if (len(sendarray) != 25):
                    a.insert(len(sendarray),'FAILED')
            break
        continue
    try:
        if len(sendarray) == 25:
            cursor.execute("INSERT INTO LabVIEW.ControllerTest1 (" + header + ") VALUES " + str(tuple(sendarray)))
    except Error as e:
        print('Error: ',e)
    finally:
        return (sendarray,a)
    return (sendarray,a)


###This section will remove the 24 items from (a) so you can send the next round into the Upload()
def pop24(a):
    try:
        for i in range(25):
            a.pop(0)
        return a
    finally:
        return a


###This is needed when you build it into an .exe file
if (__name__ == "__main__"):
    cursor = conn.cursor()      ###This just assigns the cursor for easier usage
    a = Seek(f)
    sendarray,a = Upload(a)
    while len(a) >=25:          ###This cycles throught the whole log.txt file
        sendarray = []
        a = pop24(a)
        sendarray,a = Upload(a)

    conn.commit()               ###This makes it permanant on the db
    conn.close()                ###Closes the connection to db






###Just some quick test copy paste commands
#cursor.execute("SELECT * FROM LabVIEW.Test LIMIT 20")      ###Basic select statment, remove/change "LIMIT 20" for bigger query
#cursor.fetchall()                                          ###Needed to see the "SELECT" command
#cursor.execute("INSERT INTO LabVIEW.Test (Tech,Serial) VALUES('eqd guy', 'kk1234567890123456')") ###Another example of INSERT command


### Reserved Space
