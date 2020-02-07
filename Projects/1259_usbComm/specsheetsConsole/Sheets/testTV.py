def tv(temp1, temp2, temp3): #temp1 == device type temp2 == MCU
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to
        temp3 == "0"
        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
        
        if (temp1 == "0" and temp2 == "80"): #Wolf tablet
            return(com["u2"].value)
        elif (temp1 == "1" and temp2 == "80"): #Home TV
            return(com["u3"].value)
        elif (temp1 == "1" and temp2 == "01"): #Club TV
            return(com["u4"].value)
