# coding=utf-8

"""
test_sub_asf.py
This module contains application specific functions (the
 'asf' in the filename) for a
particular project as a sub-module.
Try to avoid making changes to the other
python files.
These functions will be exposed to the end-user as what they
call to interact with our application.  Most if not all of the calls
in here will be wrappers for the 'action' function.

Function definitions:

def x_dialog_user(selection_list: list) -> str:
"""


def x_dialog_user(selection_list: list) -> str:
    """
    Dialog box for user.
    :param selection_list: 
    :return: 
    """

    selection_return = action("x_dialog_user", selection_list, 300)
    sleep(0.1)
    return selection_return.data[0]
