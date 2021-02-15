# pixelWeather
Live weather/astro information for the [Pixel badge](https://pixel.curious.supplies/) written in microPython using the [wttr.in](https://wttr.in) API~

No configuration needed! Location and timezone automatically set using IP geolocation

⛅️Fully animated weather conditions⛈

🌘At sunset, moonphase replaces current condition.🌒

Hatchery link: https://badge.team/projects/pixelWeather/

## Make app run on boot: ##
This is useful for long term running of the app to recover from occasional crashes
```python
import machine
machine.nvs_setstr("system", "default_app", "pixelWeather")
machine.reset()
```

## Specify your location manually: ##
You can specify your location manually by saving the nearest city name in flash

To verify it with the API go to:http://wttr.in/CITYNAMEHERE
```python
import valuestore
valuestore.save('pixelWeather', 'settings', {"localisation":"CITYNAMEHERE"})
```
To go back to automatic IP based geolocalisation
```python
import valuestore
valuestore.save('pixelWeather', 'settings', {"localisation":""})
```
## Install app without using the store: ##
```python
import wifi, woezel,machine
wifi.connect()
wifi.wait()
woezel.install("pixelWeather")
machine.reset()
```

![pixelWeather](https://github.com/opeRaptor/pixelWeather/blob/main/images/animated.gif)
