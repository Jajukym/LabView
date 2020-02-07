def cosmetic(temp1, temp2, temp3): #temp1 == device type temp2 == MCU
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to
        
        temp3 == "0"

        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
               
        if (temp1 == "0" and temp2 == "2"): #BLE TREAD
            return(com["d2"].value) + ("\n") + (com["e2"].value)
        elif (temp1 == "0" and temp2 != "2"): #TABLET TREAD
            return(com["d2"].value) + ("\n") + (com["e3"].value)
        elif (temp1 != "0" and temp2 == "2"): #BLE AEROBIC
            return(com["e2"].value)
        elif (temp1 != "0" and temp2 != "2"): #TABLET AEROBIC
            return(com["e3"].value)
