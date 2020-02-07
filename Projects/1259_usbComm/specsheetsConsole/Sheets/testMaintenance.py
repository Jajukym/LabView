def maintenance(temp1, temp2, temp3): #temp1 == displayType temp2 == deviceType temp3 == buttonType
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to


        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
        
        if (temp1 == "0"): #Tablet Console
            return(com["i2"].value) + ("\n") + (com["j2"].value) + ("\n") + (com["k2"].value) + ("\n") + (com["l2"].value)
        elif (temp1 != "0" and temp2 == "0" and temp3 == ""): #BLE TREAD
            return(com["i5"].value) + ("\n") + (com["k5"].value) + ("\n") + (com["l5"].value)
        elif (temp1 != "0" and temp2 == "0" and temp3 == "08"): #BLE TREAD WITH INCLINE
            return(com["i5"].value) + ("\n") + (com["j5"].value) + ("\n") + (com["k5"].value) + ("\n") + (com["l5"].value)
        elif (temp1 != "0" and temp2 != "0" and temp3 == "01"): #BLE AEROBIC ON_RESET
            return(com["i9"].value) + ("\n") + (com["k9"].value) + ("\n") + (com["l8"].value)
        elif (temp1 != "0" and temp2 != "0" and temp3 == "09"): #BLE AEROBIC ON_RESET WITH INCLINE
            return(com["i9"].value) + ("\n") + (com["j8"].value) + ("\n") + (com["k9"].value) + ("\n") + (com["l8"].value)
        elif (temp1 != "0" and temp2 != "0" and temp3 == "02"): #BLE AEROBIC SETTINGS
            return(com["i8"].value) + ("\n") + (com["k8"].value) + ("\n") + (com["l8"].value)
        elif (temp1 != "0" and temp2 != "0" and temp3 == "10"): #BLE AEROBIC SETTINGS WITH INCLINE
            return(com["i8"].value) + ("\n") + (com["l8"].value) + ("\n") + (com["k8"].value) + ("\n") + (com["l8"].value)
        elif (temp1 != "0" and temp2 == "14" and temp3 == "08"): #FreeMotion FENDER
            return(com["i6"].value) + ("\n") + (com["j6"].value) + ("\n") + (com["k6"].value) + ("\n") + (com["l6"].value)
