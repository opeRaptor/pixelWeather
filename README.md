# pixelWeather
Live weather/astro information for the[Pixel badge](https://pixel.curious.supplies/) written in microPython

Fully animated weather conditions~

No configuration needed! Location and timezone automatically set using IP geolocation

At sunset, moonphase replaces current condition.

Hatchery link: https://badge.team/projects/pixelWeather/

## Make app run on boot: ##
```python
import machine
machine.nvs_setstr("system", "default_app", "pixelWeather")
machine.reset()
```

## Install app without using the store: ##
```python
import wifi, woezel,machine
wifi.connect()
wifi.wait()
woezel.install("pixelWeather")
machine.reset()
```
![pixelWeather](https://github.com/opeRaptor/pixelWeather/blob/main/images/pixelWeather.jpg)
