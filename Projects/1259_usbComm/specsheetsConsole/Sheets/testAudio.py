def audio(temp1, temp2, temp3): #temp1 == device type temp2 == MCU
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to
        temp2 == "0"
        temp3 == "0"
        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
        
        if (temp1 == "02" or temp1 == "04" or temp1 == "08" or temp1 == "10"): #jack input
            return(com["t3"].value)
        elif (temp1 == "20"): #headphone
            return(com["t3"].value)
        elif (temp1 == "40"): #BLE audio
            return(com["t4"].value)
        elif (temp1 == "80"): #TV audio
            return(com["t5"].value)
        elif (temp1 == "01"): #MYE audio
            return(com["t5"].value)
