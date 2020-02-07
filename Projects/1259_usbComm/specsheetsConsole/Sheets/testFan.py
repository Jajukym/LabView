def fan(temp1, temp2, temp3): #temp1 == device type temp2 == MCU
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to
        temp2 == "0"
        temp3 == "0"
        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
                
        if (temp1 == "1" or temp1== "2"): #2-pin or 3-pin fans
            return(com["s2"].value)
        elif (temp1 == "4"): #2-pin and 3-pin fan
            return(com["s3"].value)
