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

                time.sleep(1)
            except KeyError:
                print('not found')


retrieveVideoInfoAndDownload()
