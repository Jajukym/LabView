# get the first argument string in the argument array
string_arg = locals()['arguments'][0]

# split up that string at commas; a string "1,2,3" becomes list
# [1, 2, 3]
mylist = string_arg.split(",")

# convert string representations to numeric (float)
for i in range(len(mylist)):
    mylist[i] = float(mylist[i])
    
# add 1 to each item
mylist = [item + 1 for item in mylist]

# Send data back using x_notify_user
x_notify_user(str(mylist))

# Alternately, implement your own return function in
# TestScript_application_specific_functions.py and catch the special
# return case in LabVIEW.
