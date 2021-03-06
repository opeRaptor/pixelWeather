import time, rgb, wifi, system, urequests
#https://github.com/badgeteam/ESP32-platform-firmware/blob/cdc6e4bd0759a58f8fe2310efd41775060a456c5/firmware/python_modules/campzone2019/default_icons.py
from default_icons import animation_connecting_wifi, icon_no_wifi

#https://stackoverflow.com/questions/3018313/algorithm-to-convert-rgb-to-hsv-and-hsv-to-rgb-in-range-0-255-for-both

#https://github.com/chubin/wttr.in/blob/master/lib/constants.py
# WEATHER_SYMBOL = {
#     "Unknown":             "✨",
#     "Cloudy":              "☁️",
#     "Fog":                 "🌫",
#     "HeavyRain":           "🌧",
#     "HeavyShowers":        "🌧",
#     "HeavySnow":           "❄️",
#     "HeavySnowShowers":    "❄️",
#     "LightRain":           "🌦",
#     "LightShowers":        "🌦",
#     "LightSleet":          "🌧",
#     "LightSleetShowers":   "🌧",
#     "LightSnow":           "🌨",
#     "LightSnowShowers":    "🌨",
#     "PartlyCloudy":        "⛅️",
#     "Sunny":               "☀️",
#     "ThunderyHeavyRain":   "🌩",
#     "ThunderyShowers":     "⛈",
#     "ThunderySnowShowers": "⛈",
#     "VeryCloudy": "☁️",
# }
# MOON_PHASES = (
#     "🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"
# )

#https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

def wttrin():
    #wttrinAPI = 'http://wttr.in/?format="%t+%c:+%S+%s+%m"' #semicolon was there to add a space, suddenly in Jan 16 it doesnt work anymore
    #wttrinAPI = 'http://wttr.in/?format="%t+%c+%S+%s+%m"'
    wttrinAPI = 'http://wttr.in/?format="%t+%S+%s+%m+%c"'
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

    wttrin = wttrinAPI.text
    wttrin = wttrin[1:-1] # strip "" of string
    print("Data:",wttrin)

    wttrinAPI.close()
    gc.collect()

    chunks = wttrin.split(' ')
    print("Chunks:",chunks)

    temp = chunks[0]
    #print("temp:",temp)
    #temp = "-8dcc"
    if temp[0] == "+":
        temp = temp[1:]
    chunks[0] = int(temp[:-2])
    print("temp:",chunks[0])

    print("sunrise:",chunks[1])
    print("sunset :",chunks[2])
    print("moonphase:",chunks[3])
    #chunks[4] = chunks[4][:1]
    print("condition:", chunks[4])
    
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
    
    request.close()
    gc.collect()

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


tries = 1
exit = 0

brightness = rgb.getbrightness()
rgb.background((0,0,0))
rgb.clear()
maxcolor = 180


while not wifi.status():
    rgb.setfont(rgb.FONT_6x3)
    trietext = "Try: {}".format(tries)
    print(trietext)
    #rgb.text(trietext, (50, 50, 50), (0, 0))
    #time.sleep(1)
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
        # rgb.scrolltext(msg, (50, 50, 50), (0, 0))
        # time.sleep(5)
        rgb.clear()
        rgb.framerate(20)
        data, frames = icon_no_wifi
        rgb.image(data, (12, 0), (8,8))
        time.sleep(3)
        rgb.clear()
    time.sleep(1)
    tries = tries + 1

######################################################################3
setTime()
#######################################################################


rgb.setfont(rgb.FONT_7x5)
#rgb.setfont(rgb.FONT_6x3)

rgb.clear()
rgb.framerate(1)
print("Mem free after setup:",gc.mem_free())
gc.collect()
print("Mem free after clear:",gc.mem_free())

while not exit == 1:
    #showcolon = not showcolon
    #th = time.strftime("%H",rtc.now())
    #tm = time.strftime("%M")

    weather = wttrin()

    sunrise = sum(int(x) * 60 ** i for i, x in enumerate(reversed(weather[1].split(':'))))
    timeNow= sum(int(x) * 60 ** i for i, x in enumerate(reversed(time.strftime("%H:%M:%S",rtc.now()).split(':'))))
    sunset= sum(int(x) * 60 ** i for i, x in enumerate(reversed(weather[2].split(':'))))

    print("sunrise:",sunrise)
    print("timenow:",timeNow)
    print("sunset:",sunset)
    
    #https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another/1969274
    #######################################################################
    value= weather[0]
    minTemp= 0
    maxTemp= 35
    
    minHSVColor= 0
    maxHSVColor= 240

    if value >= maxTemp:
        print("red hot")
        color = (255,0,0)
    elif value > minTemp and value < maxTemp:
        # Figure out how 'wide' each range is
        tempSpan = maxTemp - minTemp
        HSVColorSpan = maxHSVColor - minHSVColor

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - minTemp) / float(tempSpan)

        # Convert the 0-1 range into a value in the right range.
        hsv= maxHSVColor - (valueScaled * HSVColorSpan)
        print("HSV color:",hsv)
        color = hsv_to_rgb(hsv/360.,1,1)
    else:
        print("white cold")
        color = (255,255,255) 
    ##################################################################
    
    if sunrise < timeNow and timeNow < sunset:
        output = "{}".format(weather[0])+"C"
    else:
        output = "{}".format(weather[0])+"C"
    
    rgb.clear()
    rgb.text(output, color, (1, 0))
   
    print("Mem free for gif:    ",gc.mem_free())
    gc.collect()
    print("Mem free after clear:",gc.mem_free())
    
    #rgb.gif(data, pos=(22, -1), size=(8, 8), frames=4)
    rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffffff, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffffff, 0xffffff00, 0xffffff00], (22, -1),( 9, 8), 8)
    print("Mem free after gif:  ",gc.mem_free())
    #rgb.gif(data, (22, -1), size, frames)


    time.sleep(60)
    
system.reboot()

#gc.collect()
#gc.mem_free()
