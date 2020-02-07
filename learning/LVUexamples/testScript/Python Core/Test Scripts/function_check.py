dmm_read = x_get_dmm_voltage_reading()
script_update("DMM Reading: " + str(dmm_read))

sleep(1)
response = x_dialog_user(["Copper", "Iron", "Manganese", "Uranium"])
script_update("User response was " + response)

sleep(1)

waveform = x_get_waveform_data()
script_update("Waveform Reading: " + trim_string(str(waveform)))

sleep(1)

iteration = x_LabVIEW_test("3")
script_update("Called x_LabVIEW_test with '3' and got back " 
              + str(iteration))
              
sleep(1)              
sum = x_simple_LabVIEW_adder([3, 4])
script_update("Called x_simple_LabVIEW_adder with [3, 4] and got back "
              + str(sum))
 
sleep(1)

x_notify_user("Test complete!")
