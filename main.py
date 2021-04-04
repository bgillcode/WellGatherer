import time
import sys
import pychrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



def output_on_start(**kwargs):
    gottenOutput = kwargs

    filesize = os.path.getsize("a.txt")

    if filesize == 0:
        checkingFileSizeBoolean = False
    else:
        checkingFileSizeBoolean = True

    with open('a' + '.txt', 'a') as f:
        s = str(gottenOutput)
        if s.find('search?device_type=desktop&id=' + numberFromURL) != -1:
            print('URL for video found, storing...')

            try:
                if (checkingFileSizeBoolean == False):
                    newGottenURL = gottenOutput['request']['url']
                    f.write(str(newGottenURL.strip()))
                    checkingFileSizeBoolean = True
                    return
            except:
                pass




def output_on_end(**kwargs):
    gottenOutput2 = kwargs
