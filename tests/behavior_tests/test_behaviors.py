import os, subprocess, time
from os.path import basename
import pytest
from driver import Driver

WAIT_SECS = 10

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
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('hello sender!')
    time.sleep(WAIT_SECS) # sleep to avoid interference from next test case

def test_bot_respond_to_simple_message_with_formatting(driver):
    driver.send_direct_message('hello_formatting')
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('_hello_ sender!')
    time.sleep(WAIT_SECS) # sleep to avoid interference from next test case

def test_bot_respond_to_simple_message_case_insensitive(driver):
    driver.send_direct_message('hEllO')
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('hello sender!')
    time.sleep(WAIT_SECS) # sleep to avoid interference from next test case

def test_bot_direct_message_with_at_prefix(driver):
    driver.send_direct_message('hello', tobot=True)
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('hello sender!')
    driver.send_direct_message('hello', tobot=True, colon=False)
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_direct_message('hello sender!')
    time.sleep(WAIT_SECS) # sleep to avoid interference from next test case

# [ToDo] Implement this test together with the file upload function
def test_bot_upload_file(driver):
    pass

# [ToDo] Needs to find a better way in validating file upload by URL
def test_bot_upload_file_from_link(driver):
    #url = 'http://www.mattermost.org/wp-content/uploads/2016/03/logoHorizontal_WS.png'
    #fname = basename(url)
    #driver.send_direct_message('upload %s' % url)
    pass

def test_bot_reply_to_channel_message(driver):
    driver.send_channel_message('hello')
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_channel_message('hello sender!')
    driver.send_channel_message('hello', colon=False)
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_channel_message('hello sender!')
    driver.send_channel_message('hello', space=False)
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_channel_message('hello sender!')
    driver.send_channel_message('hello', colon=False, space=False)
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_channel_message('hello channel!')
    time.sleep(WAIT_SECS) # sleep to avoid interference from next test case

def test_bot_listen_to_channel_message(driver):
    driver.send_channel_message('hello', tobot=False)
    time.sleep(WAIT_SECS) # sleep and wait test bot to respond
    driver.validate_bot_channel_message('hello channel!')
    time.sleep(WAIT_SECS) # sleep to avoid interference from next test case
