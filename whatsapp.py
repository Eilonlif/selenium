import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from time import sleep
from PIL import Image
import datetime
import re
import pyautogui


#  ------------------------ Set up Stuff ------------------------ #
def getUserAgent(ChromePath):  # Gets Computer's User-Agent
    driver = webdriver.Chrome(executable_path=ChromePath)  # Path WILL change on other computers
    driver.get("https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes")
    usragnt = driver.find_element_by_xpath("//*[@id=\"id_user_agent\"]").text
    driver.quit()
    return usragnt


def setup(head, UA, ChromePath):
    options = Options()
    if head:
        options.add_argument("--headless")
    options.add_argument(UA)
    driver = webdriver.Chrome(executable_path=ChromePath, options=options)  # Path WILL change on other computers
    driver.get('https://web.whatsapp.com/')
    print(f"Connecting to: {driver.current_url}...")
    whatsappLogin(driver, head)
    return driver


#  ---------------------- Whatsapp related ---------------------- #
def whatsappLogin(driver, head):
    if head:
        print("Displaying Screenshot... ")
        sleep(1)
        driver.save_screenshot("test.png")
        with Image.open("test.png") as img:  # Displaying the screenshot of the Qr code
            img.show()
            input("Please scan the Qr-code, Enter to continue...")
            img.close()
        os.system("rm test.png")  # Deleting screenshot
    else:
        input("Please scan the Qr-code, Enter to continue...")


def onlineCheck(driver, time, nChats):
    while True:
        for i in range(nChats):
            try:
                chat = driver.find_element_by_xpath(f"//*[@id=\"pane-side\"]/div[1]/div/div/div[{i}]/div/div/div[2]/div[1]/div[1]/span/span").text
                if inCon(str(chat), ConAry):
                    driver.find_element_by_xpath(f"//*[@id=\"pane-side\"]/div[1]/div/div/div[{i}]/div/div/div[2]/div[1]/div[1]/span/span").click()
                    sleep(5)
                    contactCheckOnline(chat, driver, ConAry)
            except selenium.common.exceptions.NoSuchElementException:
                pass
        sleep(time)


def contactCheckOnline(who, driver, conary):
    try:
        onOrOff = driver.find_element_by_xpath(f"//*[@id=\"main\"]/header/div[2]/div[2]/span").text
        if onOrOff in "onlineOnline":
            print(f"{who} is online!")
            conary[who] = f"{datetime.datetime.now()} "
    except selenium.common.exceptions.NoSuchElementException:
        print(f"last seen {who} at: {conary[who]}")


def inCon(who, conary):
    for name, value in conary.items():
        if who in name:
            return True
    return False


#  ------------------------ Zoom related ------------------------ #
def getZoomLink(time, driver, GegckoPath, nChats):
    while True:
        for i in range(nChats):
            try:
                tmp1 = driver.find_element_by_xpath(f"//*[@id=\"pane-side\"]/div[1]/div/div/div[{i}]/div/div/div[2]/div[1]/div[1]/div/span").text
                for e in ClsAry:
                    print(f"Chat name - {tmp1} : {e}")
                    if e in tmp1:
                        driver.find_element_by_xpath(f"//*[@id=\"pane-side\"]/div[1]/div/div/div[{i}]/div/div/div[2]/div[1]/div[1]/div/span").click()
                        sleep(5)
                        lastmsgs("zoom", driver, 50, GegckoPath)
            except selenium.common.exceptions.NoSuchElementException:
                pass
        sleep(time)


def lastmsgs(wrd, driver, msgs, GeckoPath):
    print("Going threw massages...")
    for i in range(msgs, 0, -1):
        try:
            tmp = driver.find_element_by_xpath(f"//*[@id=\"main\"]/div[3]/div/div/div[3]/div[{i}]/div/div/div/div[1]/div").text
            if wrd in tmp:
                getzoom(stripUrl(tmp), GeckoPath)
        except selenium.common.exceptions.NoSuchElementException:
            pass


def stripUrl(txt):
    return re.search("(?P<url>https?://[^\s]+)", txt).group("url")


def getzoom(link, GeckoPath):
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")  # Not necessary
    driver = webdriver.Firefox(executable_path=GeckoPath)  # Path WILL change on other computers
    driver.get(link)
    sleep(5)
    popUpEnter()


def popUpEnter():  # Enter on popUp
    pyautogui.keyDown("Enter")
    pyautogui.keyUp("Enter")


chromeDriverPath = "/usr/local/bin/chromedriver 2"  # Chrome driver path
geckoDriverPath = "/usr/local/bin/geckodriver"      # Fire-Fox driver path


ConAry = {"ContactName": f"{datetime.datetime.now()}"}
ClsAry = ["GroupName"]

userAgent = getUserAgent(chromeDriverPath)
onlineCheck(setup(False, userAgent, chromeDriverPath), 20, 200)
# getZoomLink(5*60, setup(True, userAgent, chromeDriverPath), geckoDriverPath, 200)
