def aerobic(temp1, temp2, temp3):
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook
        temp2 == "0"
        temp3 == "0" #prevents requirement for special VI to handle only one variable
        #EQF1259 source and to
        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
        

        if (temp1== "0"):
                return(com["c8"].value)#basic bike/bike1 other options available
        elif (temp1 == "1" or temp1 == "2" or temp1 == "3" or temp1 == "10" or temp1 == "11"): #PB_INC
            return(com["b10"].value)
        elif (temp1 == "4" or temp1 == "5" or temp1 == "6" or temp1 == "7" or temp1 == "10" or temp1 == "11"): #PB_INC_485
            return(com["b11"].value)
        elif (temp1 == "8" or temp1 == "9"):#freemotion
                return(com["b13"].value)
        
