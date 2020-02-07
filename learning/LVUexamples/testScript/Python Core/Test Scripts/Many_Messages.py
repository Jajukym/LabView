# coding=utf-8
starttime = time.perf_counter()
script_update("Starting wait...")

dmm = 0
for i in range(1000):
    # time.sleep(0.01)
    dmm = x_get_dmm_voltage_reading()
    script_update(str(i) + ": DMM Reading - " + str(dmm))
	
elapsed = time.perf_counter() - starttime
script_update("Time elapsed: " + str(elapsed))
