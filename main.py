import time
import sys
import pychrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import sys
import subprocess
import shlex
import json
import urllib.request
from clint.textui import progress
import argparse
import os

# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument for the URL
parser.add_argument("--url", "-u", help="Set URL")
parser.add_argument("--end", "-e", help="Will loop through all relevant media on the page and retrieve it up until the selected amount (e.g. -e 5)")


# Read arguments from the command line
args = parser.parse_args()

# Set the argument for what to look for here in the URL
checkForContent = ""
endMedia = 0

# Check for --url
if args.url:
    if str(args.url).strip().find(checkForContent) != -1:
        episodeTypeCheck = True
    urlInputted = str(args.url)

# Check for --end (of media)
if args.end:
    if str(args.end).strip() != -1:
        try:
            endMedia = int(args.end)
        except:
            print('Ending given must be a number')
            print('Exiting script, please try again')
            sys.exit()


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


if endPageRange != 0:



    def retrieveVideoInfoAndDownload():
        options = webdriver.ChromeOptions()
        options.add_argument("--remote-debugging-port=8000")
        options.add_argument("--headless")
        options.add_argument("--log-level=3")

        print('\n=================================================================================')
        print('Waiting for video information to be loaded, this process can take up to 1 minute.')
        print('=================================================================================')

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(10) # seconds
        driver.find_elements_by_class_name("detailed-info")

        dev_tools = pychrome.Browser(url="http://localhost:8000")
        tab = dev_tools.list_tab()[0]
        tab.start()

        print('\n=================================================================================')
        print('Waiting for video information to be loaded, this process can take up to 1 minute.')
        print('=================================================================================')

        driver.get(urlInputted)

        tab.call_method("Network.emulateNetworkConditions",
                        offline=False,
                        latency=100,
                        downloadThroughput=9375,
                        uploadThroughput=3125,
                        connectionType="cellular3g")

        tab.call_method("Network.enable", _timeout=20)
        ss2 = tab.set_listener("Network.requestWillBeSent", output_on_start)
        ss = tab.set_listener("Network.responseReceived", output_on_end)

        try:
            driver.get(urlInputted)
            time.sleep(15)
        finally:
            driver.quit()

        with open('a.txt', 'r') as f:
            try:
                newURLObtained = f.read()
                r = requests.get(newURLObtained)
                with open(r'' + 'temp_video' + '.json', 'wb') as g:
                    g.write(r.content)
                print('JSON written')
                time.sleep(2.4)

            except:
                print('==Error: URL was not found')


        print('== Parsing JSON')
        with open('temp_video.json') as json_file:
            data = json.load(json_file)

            print('\n=========================')
            print('STARTING VIDEO DOWNLOAD')
            print('==========================')

            for i in data['objects']:
                try:
                    videoDownloadURL = i['download_url']
                    videoName = i['name']
                    print('Video URL: ' + videoDownloadURL)
                    print('Video Name: ' + videoName)#
                    videoNameBackslashes = videoName.replace(' ', '\ ')
                    print('Downloading video: ' + videoName + '.mp4' + ' from: ' + videoDownloadURL)
                    r = requests.get(videoDownloadURL, stream=True)
                    path = videoName + '.mp4'
                    with open(path, 'wb') as f:
                        total_length = int(r.headers.get('content-length'))
                        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                            if chunk:
                                f.write(chunk)
                                f.flush()
                    time.sleep(1)
                except KeyError:
                    print('not found')


    retrieveVideoInfoAndDownload()

else:
    # To do
