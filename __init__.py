try:
    import time, rgb, wifi, urequests, machine,virtualtimers,gc
    from default_icons import animation_connecting_wifi, icon_no_wifi
    #https://github.com/badgeteam/ESP32-platform-firmware/blob/cdc6e4bd0759a58f8fe2310efd41775060a456c5/firmware/python_modules/campzone2019/default_icons.py

    #https://stackoverflow.com/questions/3018313/algorithm-to-convert-rgb-to-hsv-and-hsv-to-rgb-in-range-0-255-for-both

    #https://github.com/chubin/wttr.in/blob/master/lib/constants.py

    def moonphase(moon,x,y):
        x = 24
        y = 0

        if moon == "🌑":
            # newmoon🌑.gif
            rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00], (x, y),( 9, 8), 1)

        elif moon == "🌒":
            # waxingcrescent🌒.gif
            rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00], (x, y),( 9, 8), 1)

        elif moon == "🌓":
            # firstquarter🌓.gif
            rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00], (x, y),( 9, 8), 1)

        elif moon == "🌔":
            # waxinggibbous🌔.gif
            rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00], (x, y),( 9, 8), 1)

        elif moon == "🌕":
            # fullmoon🌕.gif
            rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00], (x, y),( 9, 8), 1)

        elif moon == "🌖":
            # waninggibbous🌖.gif
            rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00], (x, y),( 9, 8), 1)

        elif moon == "🌗":
            # lastquarter🌗.gif
            rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00], (x, y),( 9, 8), 1)

        elif moon == "🌘":
            # waningcrescent🌘.gif
            rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xe4a204ff, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xe4a204ff, 0x093752ff, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0x093752ff, 0x093752ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00], (x, y),( 9, 8), 1)
        else:
            # errorstate✨.gif
            rgb.gif([0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00, 0xffffff00, 0xb03248ff, 0xffffff00, 0xffffff00], (x, y),( 9, 8), 2)

    def condition(emoji,x,y):

        if emoji == "☀️":
            print("sunny☀️.gif")
            from .sunny import data

        if emoji == "☁️":
            print("cloudy☁️.gif")
            from .cloudy import data
            
        elif emoji == "⛅️":
            print("partlycloudy⛅️.gif")
            from .partlycloudy import data
        
        elif emoji == "❄️":
            print("snow❄️.gif")
            from .snow import data
        
        elif emoji =="⛈":
            print("thunderstorm⛈.gif")
            from .thunderstorm import data
        
        elif emoji =="🌧":
            print("rain🌧.gif")
            from .rain import data

        else:
            print("errorstate✨.gif")
            from .errorstate import data
        
        img, pos, size, frames = data
        rgb.gif(img,(x,y), size, frames)
        del data
            
    def mapToHSV(value):   
        #https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another/1969274
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
            hsv= int(maxHSVColor - (valueScaled * HSVColorSpan))
            print("HSV color:",hsv)
            color = hsv_to_rgb(hsv/360.,1,1)
        else:
            print("white cold")
            color = (255,255,255) 
            
        return color
        ##################################################################

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
                continue

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
                continue
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

    setTime()

    rgb.setfont(rgb.FONT_7x5)
    #rgb.setfont(rgb.FONT_6x3)

    rgb.clear()
    rgb.framerate(1)
    print("Mem free after setup:",gc.mem_free())
    gc.collect()
    print("Mem free after clear:",gc.mem_free())

    def refresh():
        
        print("Mem free for gif:    ",gc.mem_free())
        gc.collect()
        print("Mem free after clear:",gc.mem_free())

        weather = wttrin()

        sunrise = sum(int(x) * 60 ** i for i, x in enumerate(reversed(weather[1].split(':'))))
        timeNow= sum(int(x) * 60 ** i for i, x in enumerate(reversed(time.strftime("%H:%M:%S",time.localtime()).split(':'))))
        sunset= sum(int(x) * 60 ** i for i, x in enumerate(reversed(weather[2].split(':'))))

        print("sunrise:",sunrise)
        print("timenow:",timeNow)
        print("sunset:",sunset)
        rgb.clear()

        if sunrise < timeNow and timeNow < sunset: #It is daytime
            condition(weather[4],24,0)
        else:
            moonphase(weather[3],24,0)

        output = "{}".format(weather[0])+"C"    
        
        color= mapToHSV(weather[0])
        rgb.text(output, color, (0, 1))

        print("Mem free after gif:  ",gc.mem_free())
        
        run_again_in = 60000  # time until this function should run again, in ms
        return run_again_in
        
    # Initialise the virtualtimers task, and register our function
    virtualtimers.begin(100)
    virtualtimers.new(0, refresh)  # run now, with 0 delay

except:
    print("################################################################################################################################################################")
    print("################################################################################################################################################################")
    print("Something bad happened (blame lack of RAM), exception, we need a reboot")
    print("################################################################################################################################################################")
    print("################################################################################################################################################################")
    #system.reboot()
    machine.reset()