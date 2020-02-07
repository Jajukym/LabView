def pulse(temp1, temp2, temp3): #temp1 == device type temp2 == MCU
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to
        temp3 == "0"
        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
        
        if (temp1 == "02"): #hand
            return(com["r2"].value)
        if (temp1 == "04"): #thumb
            return(com["r3"].value)
        if (temp1 == "08" or temp1 == "10" or temp1 == "40" and temp2 == "0"): #chest
            return(com["r2"].value) + ("\n") + (com["r4"].value)
        if (temp1 == "22" and temp2 == "2"): #BLE console
            return(com["r2"].value) + ("\n") + (com["r5"].value)
        if (temp1 == "22" and temp2 == "1" or temp2 == "3"): #tablet console
            return(com["r2"].value) + ("\n") + (com["r6"].value)
