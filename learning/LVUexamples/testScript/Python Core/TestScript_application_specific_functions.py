# coding=utf-8


"""
TestScript_application_specific_functions.py
This module contains application specific functions for a
particular project.  Try to avoid making changes to the other
python files.
These functions will be exposed to the end-user as what they
call to interact with our application.  Most if not all of the calls
in here will be wrappers for the 'action' function.

Function definitions:

def app_specific_import(filename: str, app_globals: dict = globals(),
                        app_locals: dict = locals()) -> None:
def x_get_dmm_voltage_reading() -> float:
def x_notify_user(message_to_user: str) -> None:
def x_get_waveform_data() -> list:
def x_LabVIEW_test(iteration: str) -> float:
def x_simple_LabVIEW_adder(addends: list, update: bool = True) -> float:
"""


def app_specific_import(filename: str, app_globals: dict = globals(),
                        app_locals: dict = locals()) -> None:
    """
    This function makes importing sub-modules easy. They have to be
    aware of the "action" function defined in the
    TestScript_gui_and_exposed_functions.py file.

    Call it like this:

    app_specific_import("my_module.py")

    :param filename: The filename string of the module to import.
    :param app_globals: globals context dictionary.
    :param app_locals: locals context dictionary.
    :return: Doesn't return anything.
    """

    with open(filename, 'r') as my_file:
        data = my_file.read()
    my_file.close()
    exec(data, app_globals, app_locals)


# Allows you to organize your application specific functions
# into sub-modules. Call them like this: (the 'asf' stands for
# 'application-specific functions')
app_specific_import("TestScript_sub_asf.py")


def x_get_dmm_voltage_reading() -> float:
    """
    Example code for a customer exposed function
    :return: The DMM voltage reading.
    """

    voltage_return = action("x_get_dmm_voltage_reading", None, 2)

    return float(voltage_return.data[0])


def x_notify_user(message_to_user: str) -> None:
    """
    Dialog called with one item list will return immediately with
    intent on LabVIEW side to just
    display the message
    :param message_to_user: 
    :return: 
    """

    action("x_dialog_user", [message_to_user], timeout=30)
    return None


def x_get_waveform_data() -> list:
    """
    This function returns a LabVIEW waveform.
    :rtype: list: the LabVIEW waveform. 
    """

    waveform_return = action("x_get_waveform_data", timeout=2)
    wave_float = [float(i) for i in waveform_return.data]
    return wave_float


def x_LabVIEW_test(iteration: str) -> float:
    return_value = action("x_LabVIEW_test", [iteration], 5, False)
    return float(return_value.data[0])


def x_simple_LabVIEW_adder(addends: list, update: bool = True) -> float:
    """
    This function is a simple exerciser for the x_simple_LabVIEW_adder
    function.
    It shows a simple example of Python telling LabVIEW to do something.
    :param addends: the numbers to be added
    :param update: whether to send the script_update call in the
        action function.
    :return:
    """

    return_value = action("x_simple_LabVIEW_adder", addends, 1, update)
    return float(return_value.data[0])
