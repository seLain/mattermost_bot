import os, subprocess, time
import pytest
from driver import Driver

'''
Function to run a bot for testing in subprocess
'''
def _start_bot_process():
    args = ['python', 'tests/behavior_tests/run_bot.py',]
    return subprocess.Popen(args)

@pytest.fixture(scope='module')
def driver():
    driver = Driver()
    driver.start()
    p = _start_bot_process()
    driver.wait_for_bot_online()
    yield driver
    p.terminate()

'''
Empty test to ensure fixture start_test will be executed
'''
def test_bot_get_online(driver):
    pass

#########################################################
# Actual test cases bellow
#########################################################

def test_bot_respond_to_simple_message(driver):
    driver.send_direct_message('hello')
    time.sleep(5) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('hello sender!')

def test_bot_respond_to_simple_message_with_formatting(driver):
    driver.send_direct_message('hello_formatting')
    time.sleep(5) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('_hello_ sender!')

def test_bot_respond_to_simple_message_case_insensitive(driver):
    driver.send_direct_message('hEllO')
    time.sleep(5) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('hello sender!')

def test_bot_direct_message_with_at_prefix(driver):
    driver.send_direct_message('hello', tobot=True)
    time.sleep(5) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('hello sender!')
    driver.send_direct_message('hello', tobot=True, colon=False)
    time.sleep(5) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('hello sender!')

