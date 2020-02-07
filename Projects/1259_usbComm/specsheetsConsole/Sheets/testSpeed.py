def PWM_Tach(temp1, temp2, temp3): #temp1 == device type temp2 == MCU
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to
        temp2 == "0"
        temp3 == "0"
        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
        
        if (temp1 == "0"): #Treadmill
            return(com["m2"].value)
        elif (temp1 == "1"): #Bike/Elyptical
            return(com["n2"].value)
        elif (temp1 != "2"): #Rower
            return(com["n2"].value)
        
