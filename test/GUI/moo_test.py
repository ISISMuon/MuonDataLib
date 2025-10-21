import unittest
import numpy as np
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.GUI.moo import View
from dash._utils import AttributeDict

from dash._callback_context import context_value as cv
from contextvars import copy_context
import dash.testing as dash_duo
import time

def test_1(dash_duo):
        v = View()
        dash_duo.start_server(v)
        dash_duo.wait_for_page()
        dash_duo.find_element('#btn-1').click()
        time.sleep(1)
        assert (dash_duo.find_element('#container').text == f'You last clicked button with ID btn-1')
        assert (dash_duo.find_element('#container-no-ctx').text == f'button 1: 1 & button 2: None')


def test_2(dash_duo):
        v = View()
        dash_duo.start_server(v)
        dash_duo.wait_for_page()
        dash_duo.find_element('#btn-2').click()
        time.sleep(1)
        assert (dash_duo.find_element('#container').text == f'You last clicked button with ID btn-2')
        assert (dash_duo.find_element('#container-no-ctx').text == f'button 1: None & button 2: 1')


# needed to install dash[testing] and selenium
    
