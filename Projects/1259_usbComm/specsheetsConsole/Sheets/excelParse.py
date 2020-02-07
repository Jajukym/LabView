def function(temp): #temp1 == device type temp2 == MCU
        import sys; #build system
        import openpyxl
        from openpyxl import load_workbook #EQF1259 source and to


        
        app = openpyxl.load_workbook("C:\\LabviewFiles\\LabView\\Projects\\1259_usbComm\\specSheets\\Sheets\\ConsoleProcedures.xlsx")#Read sheets
        eng = app["english"] #PIP database
        chi = app["chinese"]

        
        if (temp == "0"):
                return(eng["d2"].value) + ("\n") + (eng["e2"].value) + ("\n") + (eng["f2"].value)+ ("\n") + (eng["g2"].value)
        elif (temp == "1"):
                return(eng["e2"].value) + ("\n") + (eng["f2"].value)+ ("\n") + (eng["g3"].value)
        
