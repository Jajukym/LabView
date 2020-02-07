def aerobic(temp1, temp2, temp3): #temp1 == device type temp2 == MCU
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to

        temp3 == "0"

        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
               
        if (temp1 == "0" and temp2 == "0"): #Basic_Bike just batteries and resistance
            return(com["f8"].value)
        elif (temp1 == "0" and temp2 != "0"): #Basic_Bike resistance and tach
            return(com["f9"].value)
        elif (temp1 == "1" or temp1 == "2" or temp1 == "3" or temp1 == "12" or temp1 == "13"): #PB_INC
            return(com["f3"].value)
        elif (temp1 == "4" or temp1 == "5" or temp1 == "6" or temp1 == "7" or temp1 == "10" or temp1 == "11"): #PB_INC
            return(com["f4"].value)
        elif (temp1 == "8" or temp1 == "9"): #PB_INC
            return(com["f5"].value)
