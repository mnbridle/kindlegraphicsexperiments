# -*- coding: utf-8 -*-

import time
import datetime
import kindle_graphics

import astral
import suncalc

def main():
    kindle_screen = kindle_graphics.FB_GFXInterface()
    # Double buffering - clear the screen and write to display quicker
    double_buffer = kindle_graphics.FB_GFXInterface()

    kindle_screen.init_screen()
    draw_window(kindle_screen)
    # Calculate astronomical data, make location
    latitude = -43.5321
    longitude = 172.6362

    astro_data = suncalc.getTimes(datetime.datetime.now(), latitude, longitude)
    moon_data = suncalc.getMoonTimes(datetime.datetime.now(), latitude, longitude)

    sunrise = astro_data["sunrise"].strftime("%I:%M %p")
    sunset =  astro_data["sunset"].strftime("%I:%M %p")

    moonrise = moon_data['rise'].strftime("%I:%M %p")
    moonset  = moon_data['set'].strftime("%I:%M %p")

    # Get data from kindle
    base_device_path = "/sys/devices/system/luigi_battery/luigi_battery0/"

    values_to_obtain = ["battery_voltage", "battery_current", "battery_temperature", "battery_mAH"]
    battery_data = {}

    for value in values_to_obtain:
        with open(base_device_path+value, 'r') as dev_file:
            data = dev_file.read()
            battery_data[value] = int(data.strip('\r\n'))

    display_information(kindle_screen=kindle_screen, battery_voltage=battery_data['battery_voltage'], battery_current=battery_data['battery_current'], battery_mAH=battery_data['battery_mAH'],
                        temperature=int((battery_data['battery_temperature'] - 32)*(5/9.0)), sunrise=sunrise, sunset=sunset, moonrise=moonrise, moonset=moonset)

    double_buffer.write_screen()
    # Clear artifacts by making the screen black, then making it white
    double_buffer.bg_shade = 0x9
    double_buffer.init_screen()
    double_buffer.write_screen()
    double_buffer.bg_shade = 0x0
    double_buffer.init_screen()
    double_buffer.write_screen()

    kindle_screen.write_screen()


def draw_window(kindle_screen):
    # Draw screen frame
    kindle_screen.horizontal_line(y=0, fg_shade=15)
    kindle_screen.horizontal_line(y=266, fg_shade=15)
    kindle_screen.horizontal_line(y=533, fg_shade=15)
    kindle_screen.horizontal_line(y=667, fg_shade=15)
    kindle_screen.horizontal_line(y=799, fg_shade=15)

    kindle_screen.vertical_line(x=0, fg_shade=15)
    kindle_screen.vertical_line(x=599, fg_shade=15)

    kindle_screen.line(x1=300, y1=533, x2=300, y2=799, fg_shade=15)
    kindle_screen.line(x1=300, y1=0, x2=300, y2=266, fg_shade=15)

    kindle_screen.line(x1=300, x2=599, y1=66, y2=66, fg_shade=15)
    kindle_screen.line(x1=300, x2=599, y1=133, y2=133, fg_shade=15)
    kindle_screen.line(x1=300, x2=599, y1=200, y2=200, fg_shade=15)

    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/LiberationSerif-Regular.ttf', text="Sunrise", angle=0, start_x=305, start_y=60, font_size=6)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/LiberationSerif-Regular.ttf', text="Sunset", angle=0, start_x=305, start_y=127, font_size=6)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/LiberationSerif-Regular.ttf', text="Moonrise", angle=0, start_x=305, start_y=194, font_size=6)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/LiberationSerif-Regular.ttf', text="Moonset", angle=0, start_x=305, start_y=260, font_size=6)


def display_information(kindle_screen, temperature=25, sunrise="00:00", sunset="00:00", moonrise="00:00", moonset="00:00", battery_voltage=4200, battery_current=0, battery_mAH=0):
    battery_voltage = battery_voltage * 0.001

    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text="{}\xb0C".format(temperature), angle=0, start_x=30, start_y=180, font_size=48)

    # Display moonrise/set and sunrise/set data
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text=sunrise, angle=0, start_x=400, start_y=60, font_size=18)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text=sunset, angle=0, start_x=400, start_y=127, font_size=18)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text=moonrise, angle=0, start_x=400, start_y=194, font_size=18)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text=moonset, angle=0, start_x=400, start_y=260, font_size=18)

    # Display battery parameters
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text="{:.3f} V".format(battery_voltage), angle=0, start_x=70, start_y=623, font_size=18)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text="{} mA".format(battery_current), angle=0, start_x=70, start_y=766, font_size=18)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text="{} mAH".format(battery_mAH), angle=0, start_x=340, start_y=623, font_size=18)

    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text="{}".format(datetime.datetime.now().strftime("%I:%M %p")), angle=0, start_x=70, start_y=500, font_size=48)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.ttf', text="{}".format(datetime.datetime.now().strftime("%A %d %B, %Y")), angle=0, start_x=30, start_y=350, font_size=18)


iter = 0
while iter < 60*12:
    main()
    iter+=1
    time.sleep(60)
