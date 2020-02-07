sleep(10)

dmm_read = x_get_dmm_voltage_reading()
script_update("DMM Reading: " + str(dmm_read))

sleep(10)
response = x_dialog_user(["Stand 1", "Stand 2", "Stand 3"])
script_update("User response was " + response)

sleep(10)

waveform = x_get_waveform_data()
script_update("Waveform Reading: " + trim_string(str(waveform)))

x_notify_user("Test complete!")