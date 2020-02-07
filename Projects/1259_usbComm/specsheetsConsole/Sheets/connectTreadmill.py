def treadmill(temp1, temp2, temp3):
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook
        temp2 == "0"
        temp3 == "0" #prevents requirement for special VI to handle only one variable
        #EQF1259 source and to
        app = openpyxl.load_workbook("C:\\specsheetsConsole\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        com = app["combine"]
       

        if (temp1 == "0"):
            return(com["b8"].value)#TREAD_TACH/tread3
        elif (temp1 == "1" or temp1 == "2" or temp1 == "3" or temp1 == "4" or temp1 == "5" or temp1 == "6" or temp1 == "7" or temp1 == "8" or temp1 == "9" or temp1 == "10" or temp1 == "11" or temp1 == "12" or temp1 == "13" or temp1 == "14"): #PB_INC
            return(com["b2"].value)
        elif (temp1 == "15" or temp1 == "16" or temp1 == "17" or temp1 == "18" or temp1 == "19"): #PB_INC
            return(com["b3"].value)
        elif (temp1 == "20"):
                return(com["b5"].value)#MC5150/boston1
        elif (temp1 == "21" or temp1 == "22"):
                return(com["b4"].value)#club
        elif (temp1 == "23" or temp1 == "24"):
                return(com["b19"].value)#club pfc
