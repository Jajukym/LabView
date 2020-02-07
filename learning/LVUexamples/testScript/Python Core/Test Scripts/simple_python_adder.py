# Use list comprehension to create a list of floats to sum up.
addends = [float(i) for i in locals()['arguments']]

script_update(str(sum(addends)))
