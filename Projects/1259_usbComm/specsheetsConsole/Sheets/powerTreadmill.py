def treadmill(temp1, temp2, temp3): #temp1 == device type temp2 == MCU
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to

        temp2 == "0"
        temp3 == "0"
        
        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
               
        if (temp1 == "0"): #BLE TREAD
            return(com["f4"].value)
        elif (temp1 == "1" or temp1 == "2" or temp1 == "3" or temp1 == "4" or temp1 == "5" or temp1 == "6" or temp1 == "7" or temp1 == "8" or temp1 == "9" or temp1 == "10" or temp1 == "11" or temp1 == "12" or temp1 == "13" or temp1 == "14"): #2100
            return(com["f2"].value)
        elif (temp1 == "15" or temp1 == "16" or temp1 == "17" or temp1 == "18" or temp1 == "19"): #5100
            return(com["f3"].value)
        elif (temp1 == "21" or temp1 == "22"): #olympus
            return(com["f5"].value)
        elif (temp1 == "23" or temp1 == "24"): #rhymebus
            return(com["f18"].value)
