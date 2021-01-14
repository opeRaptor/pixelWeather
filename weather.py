import time, ntp, rgb, wifi, buttons, defines, system, random, urequests,utime
#from default_icons import animation_connecting_wifi, icon_no_wifi

#https://github.com/chubin/wttr.in/blob/master/lib/constants.py
WEATHER_SYMBOL = {
    "Unknown":             "✨",
    "Cloudy":              "☁️",
    "Fog":                 "🌫",
    "HeavyRain":           "🌧",
    "HeavyShowers":        "🌧",
    "HeavySnow":           "❄️",
    "HeavySnowShowers":    "❄️",
    "LightRain":           "🌦",
    "LightShowers":        "🌦",
    "LightSleet":          "🌧",
    "LightSleetShowers":   "🌧",
    "LightSnow":           "🌨",
    "LightSnowShowers":    "🌨",
    "PartlyCloudy":        "⛅️",
    "Sunny":               "☀️",
    "ThunderyHeavyRain":   "🌩",
    "ThunderyShowers":     "⛈",
    "ThunderySnowShowers": "⛈",
    "VeryCloudy": "☁️",
}
MOON_PHASES = (
    "🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"
)

def wttrin():
    wttrinAPI = 'http://wttr.in/?format="%t+%c:+%S+%s+%m"'
    while True:
        wttrinAPI = urequests.get(wttrinAPI)
        print("wttr.in HTTP request status Code:",wttrinAPI.status_code)
        #print(r.status_code)
        
        if wttrinAPI.status_code == 200:
            break
        else:
            # Hope it won't 500 a little later
            print("Bad response")
            time.sleep(5)

    #print("Data:",wttrinAPI.text)

    wttrin = wttrinAPI.text

    wttrinAPI.close()
    gc.collect()

    chunks = wttrin.split(' ')

    temp = chunks[0][1:]
    #print("temp:",temp)
    #temp = "-8dcc"
    if temp[0] == "+":
        temp = temp[1:]
    chunks[0] = temp[:-2]
    print("temp:",chunks[0])

    condition = chunks[1]
    print("condition:", condition)
    sunrise = chunks[2]
    print("sunrise:",sunrise)
    sunset = chunks[3]
    print("sunrise:",sunset)
    chunks[4] = chunks[4][:1]
    moonphase = chunks[4]
    print("moonphase:",moonphase)
    return chunks

def setTime():
    rtc = machine.RTC()

    print("Time before:",rtc.datetime())

    worldTimeAPI = "http://worldtimeapi.org/api/ip"
    while True:
        request = urequests.get(worldTimeAPI)
        print("WorldtimeAPI HTTP request status Code:",request.status_code)
        #print(r.status_code)
        
        if request.status_code == 200:
            break
        else:
            # Hope it won't 500 a little later
            print("Bad response")
            time.sleep(5)
    result = request.json()

    unixtime = result['unixtime']
    raw_offset = result["raw_offset"]

    localtime = time.localtime(unixtime)
    rtc.init(localtime)

    timezone = str('UTC-{}'.format(int(raw_offset/3600)))
    machine.nvs_setstr('system', 'timezone', timezone)
    rtc.timezone(timezone)

    print("Time   now:",rtc.now())
    print("Local time:",time.localtime())
    print("GMT   time:",time.gmtime())

UP, DOWN, LEFT, RIGHT = defines.BTN_UP, defines.BTN_DOWN, defines.BTN_LEFT, defines.BTN_RIGHT
A, B = defines.BTN_A, defines.BTN_B

def input_B(pressed):
    global direction
    direction = B

def callback_btn_UP(button_is_down):
    if button_is_down:
        global maxcolor, color
        col1 = random.randrange(0, maxcolor)
        col2 = random.randrange(0, maxcolor)
        col3 = random.randrange(0, maxcolor)
        msg = "Color RGB {}, {}, {}".format(col1, col2, col3)
        print(msg)
        color = (col1, col2, col3)

def callback_btn_LEFT(button_is_down):
    if button_is_down:
        global brightness
        if brightness > 3:
            brightness = brightness - 1
            rgb.brightness(brightness)
            msg = "Brightness {}".format(brightness)
            print(msg)

def callback_btn_RIGHT(button_is_down):
    if button_is_down:
        global brightness
        if brightness < 32:
            brightness = brightness + 1
            rgb.brightness(brightness)
            msg = "Brightness {}".format(brightness)
            print(msg)

def callback_btn_B(button_is_down):
    if button_is_down:
        print("callback_btn_B")
        global exit
        exit = 1

buttons.register(defines.BTN_UP, callback_btn_UP)
buttons.register(defines.BTN_LEFT, callback_btn_LEFT)
buttons.register(defines.BTN_RIGHT, callback_btn_RIGHT)
buttons.register(defines.BTN_B, callback_btn_B)

direction = 0
tries = 1
exit = 0
brightness = rgb.getbrightness()
rgb.background((0,0,0))
rgb.clear()
maxcolor = 180
color = (180, 180, 180)

while not wifi.status():
    rgb.setfont(rgb.FONT_6x3)
    trietext = "Try: {}".format(tries)
    print(trietext)
    rgb.text(trietext, (50, 50, 50), (0, 0))
    time.sleep(1)
    data, size, frames = animation_connecting_wifi
    rgb.clear()
    rgb.framerate(3)
    rgb.gif(data, (12, 0), size, frames)
    wifi.connect()
    if wifi.wait():
        rgb.clear()
        rgb.framerate(20)
    else:
        msg = "No wifi"
        print(msg)
        #rgb.scrolltext(msg, (50, 50, 50), (0, 0))
        #time.sleep(5)
        rgb.clear()
        rgb.framerate(20)
        data, frames = icon_no_wifi
        rgb.image(data, (12, 0), (8,8))
        time.sleep(3)
        rgb.clear()
    time.sleep(3)
    tries = tries + 1

######################################################################3
setTime()
#######################################################################

rgb.setfont(rgb.FONT_7x5)
#rgb.setfont(rgb.FONT_6x3)

rgb.clear()
rgb.framerate(1)

while not exit == 1:
    #showcolon = not showcolon
    #th = time.strftime("%H",rtc.now())
    #tm = time.strftime("%M")
    
    weather = wttrin()

    sunrise = sum(int(x) * 60 ** i for i, x in enumerate(reversed(weather[2].split(':'))))
    timeNow= sum(int(x) * 60 ** i for i, x in enumerate(reversed(time.strftime("%H:%M:%S",rtc.now()).split(':'))))
    sunset= sum(int(x) * 60 ** i for i, x in enumerate(reversed(weather[3].split(':'))))

    print("sunrise:",sunrise)
    print("timenow:",timeNow)
    print("sunset:",sunset)
    
    
    if sunrise < timeNow and timeNow < sunset:
        output = "{}".format(weather[0])+"C"
    else:
        output = "{}".format(weather[0])+"C"

    data = [0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff,
          0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff,
          0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x808080ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x808080ff, 0x000000ff, 0x000000ff, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff,
          0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0xffffffff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff, 0x000000ff]
    
    icon = ([0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00])
    data = ([0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00])

    snow = ([0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00], 0, 0, 9, 8, 7)
    
    icon = ([0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0x5c5d75ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00])
    
    
    data, size, frames = snow

    rgb.clear()
    rgb.framerate(2)  # This makes the animation run at 2 frames per second
    rgb.gif(data, (12, 0), size, frames)
    #rgb.gif(snow,pos=(22,-1), size=(9, 8),frames=3)
    #rgb.gif(data, pos=(22, -1), size=(8, 8), frames=4)
	
    rgb.text(output, color, (1, 0))

    time.sleep(5)
    
system.reboot()

#C1tqFfOfwD7_Ws18QLCBHnRHEUTH0l_sVCNuc9DR2ZY
#curl -X GET https://api-tokyochallenge.odpt.org/api/v4/odpt:Train?acl:consumerKey=C1tqFfOfwD7_Ws18QLCBHnRHEUTH0l_sVCNuc9DR2ZY
#curl -X GET https://api-tokyochallenge.odpt.org/api/v4/odpt:Station?odpt:stationTitle.en=Horikirishōbuen&acl:consumerKey=C1tqFfOfwD7_Ws18QLCBHnRHEUTH0l_sVCNuc9DR2ZY
#https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?dc:stationitle=東京&acl:consumerKey=C1tqFfOfwD7_Ws18QLCBHnRHEUTH0l_sVCNuc9DR2ZY
#https://api-tokyochallenge.odpt.org/api/v4/odpt.StationTimetable:Keisei.Main.Horikirishobuen?acl:consumerKey=C1tqFfOfwD7_Ws18QLCBHnRHEUTH0l_sVCNuc9DR2ZY

# def wttrin2():
#     wttrinAPI = "http://wttr.in/?format=j1"
#     worldTimeAPI = "http://worldtimeapi.org/api/ip"

#     #list(dumbstreamjson.from_url('http://%s/basket/%s/search/%s/json' % (woezel_domain, device_name, query),keys=['name', 'slug', 'category', 'revision']))
#     out = list(dumbstreamjson.from_url(worldTimeAPI,keys=['unixtime']))
#     print(out)
#     #for item in dumbstreamjson.from_url(wttrinAPI, keys=["current_condition"]):
#     #    print(item['temp_c'])


# def wttrin():
#     wttrinAPI = "http://wttr.in/?format=j1"
#     request = urequests.get(wttrinAPI)
#     result = request.json()

#     temp = result["current_condition"]["temp_c"]
#     weather = result["current_condition"]["weatherDesc"]["value"]

#     moonPhase = result["weather"]["astronomy"]["moon_phase"]
#     sunRise = result["weather"]["astronomy"]["sunrise"]
#     sunSet = result["weather"]["astronomy"]["sunset"]

#     print(temp,weather)
#     print(moonPhase,sunRise,sunSet)