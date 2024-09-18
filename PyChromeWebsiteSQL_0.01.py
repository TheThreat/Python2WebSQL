from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
import psutil
import subprocess
import time
import win32api, win32con, win32gui, win32process

def get_powershell_pid():
    for process in psutil.process_iter():
        try:
            if process.name() == "powershell.exe":
                cmdline = process.cmdline()
                if any("python" in arg for arg in cmdline):  # Check if Python is involved
                    return process.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return None

def switch_to_app(pid):
    hwnd = win32gui.FindWindow(None, "powershell")
    thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
    if process_id == pid:
        win32gui.SetForegroundWindow(hwnd)
		
def click(x,y): # Used to select the SQL input field and click the run button
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

wdriver = webdriver.Chrome() # Used to interact with the web page

wdriver.get("https://www.sql-practice.com/")
wdriver.maximize_window()

time.sleep(0.5)
search = wdriver.find_element(By.XPATH, "//*[@class='start-btn']")
time.sleep(1)
search.click()

time.sleep(0.5)
click(400,301)

time.sleep(0.1)
keyboard = Controller()
keyboard.press(Key.ctrl)
keyboard.press('a')
keyboard.press(Key.backspace)
keyboard.release(Key.ctrl)
keyboard.release('a')
keyboard.release(Key.backspace)

time.sleep(0.2)
pwrPid = get_powershell_pid()
switch_to_app(pwrPid)

print(pwrPid, "------------------------")

elementText = (input("Enter an SQL query to solve the problem: "))
wdriver.switch_to.window(wdriver.current_window_handle)
wdriver.maximize_window()
time.sleep(0.5)
click(400,301)
element = wdriver.switch_to.active_element
element.send_keys(elementText)
time.sleep(0.5)
""" 
runButton = wdriver.find_element(By.XPATH, "//*[@class='data-v-255e1732']")
time.sleep(1)
runButton.click()
"""
click(50,210)
time.sleep(1)
# errorMess = wdriver.find_element(By.XPATH, "//*[@class='errorMessage']")
rightOrWrong = wdriver.find_element(By.XPATH, "//*[@class='ignore-darkmode answer-correct-box']")

print("Congratulations!")
time.sleep(60)