# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

# Herz08: changes for RGB_LED


import time
import subprocess
import psutil
try:
    import RPi.GPIO as GPIO
    from board import SCL, SDA
    import busio
    from PIL import Image, ImageDraw, ImageFont
    import adafruit_ssd1306
except ImportError as e:
    print(f"DEBUG: Fehler beim Importieren von Bibliotheken: {e}")
    exit(1)

# --- Konstanten ---
class Config:
    # GPIO Pins
    INFO_BTN = 20
    LED_R = 22
    LED_G = 23
    LED_B = 24

    # Timer Einstellungen
    DISP_TIMEOUT = 15
    REBOOT_TIMEOUT = 5
    SHUTDOWN_TIMEOUT = 10

    # Display Einstellungen
    TOP = -2

# --- Hardware Initialisierung ---
def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Config.LED_R, GPIO.OUT)
    GPIO.setup(Config.LED_G, GPIO.OUT)
    GPIO.setup(Config.LED_B, GPIO.OUT)
    GPIO.setup(Config.INFO_BTN, GPIO.IN)

def init_display():
    try:
        i2c = busio.I2C(SCL, SDA)
        disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    except Exception as e:
        print(f"DEBUG: Fehler beim Initialisieren des Displays: {e}")
        exit(1)    
    disp.rotation = 2
    disp.fill(0)
    disp.show()
    
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    return disp, draw, image, font, width, height

# --- LED Steuerung ---
def set_leds(r, g, b):
    GPIO.output(Config.LED_R, r)
    GPIO.output(Config.LED_G, g) 
    GPIO.output(Config.LED_B, b)

# --- System Informationen ---
def get_system_info():
    hostname = subprocess.check_output("hostname", shell=True).decode('UTF-8').strip()
    ip = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True).decode('UTF-8').strip()
    cpu = "{:3.0f}".format(psutil.cpu_percent())
    mem = "{:2.0f}".format(psutil.virtual_memory().percent)
    return hostname, ip, cpu, mem

# --- Display Funktionen ---
def show_startup_info(draw, disp, image, font, width, height):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    Config.TOP
    draw.text((40, Config.TOP),    "--------------------", font=font, fill=255)
    draw.text((20, Config.TOP+12), " Infoscreen Started ", font=font, fill=255) 
    draw.text((40, Config.TOP+24), "--------------------", font=font, fill=255)
    disp.image(image)
    disp.show()
    time.sleep(5)  # Show startup message for 5 seconds
    disp.fill(0)   # Clear the display
    disp.show()

def draw_info(draw, font, width, height, timer):
    hostname, ip, cpu, mem = get_system_info()
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, Config.TOP), f"NAME: {hostname}", font=font, fill=255)
    draw.text((0, Config.TOP+12), f"IP  : {ip}", font=font, fill=255)
    draw.text((0, Config.TOP+24), f"CPU : {cpu}% | MEM: {mem}%", font=font, fill=255)
    draw.text((110, Config.TOP), f"{timer}", font=font, fill=255)

def draw_reboot(draw, font, width, height, timer, confirmed=False):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    if confirmed:
        draw.text((0, Config.TOP+12), "Performing Reboot...", font=font, fill=255)
    else:
        draw.text((0, Config.TOP), ".......Reboot.......", font=font, fill=255)
        draw.text((0, Config.TOP+12), "   Release Button   ", font=font, fill=255)
        draw.text((0, Config.TOP+24), "      To Reboot     ", font=font, fill=255)
        draw.text((110, Config.TOP), f"{timer}", font=font, fill=255)

def draw_shutdown(draw, font, width, height, timer, confirmed=False):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    if confirmed:
        draw.text((0, Config.TOP+12), "Shutting down.......", font=font, fill=255)
    else:
        draw.text((0, Config.TOP), "......Shutdown......", font=font, fill=255)
        draw.text((0, Config.TOP+12), "   Release Button   ", font=font, fill=255)
        draw.text((0, Config.TOP+24), "    To Shutdown     ", font=font, fill=255)
        draw.text((110, Config.TOP), f"{timer}", font=font, fill=255)

def system_cmd(do_reboot: int, do_shutdown: int ):
        if do_reboot == 1:
            cmd = "sudo reboot now"
            subprocess.Popen(cmd, shell = True)
        if do_shutdown == 1:
            cmd = "sudo shutdown now"
            subprocess.Popen(cmd, shell = True)


# --- Hauptprogramm ---
def main():
    init_gpio()
    disp, draw, image, font, width, height = init_display()

    # Show startup message
    show_startup_info(draw, disp, image, font, width, height)

    disp_timer = 0
    menu_state = 0
    menu_timer = 0

    try:
        while True:
            print(f"DEBUG: Menu Timer: {menu_timer}, Menu State: {menu_state}, Disp Timer: {disp_timer}")
 
            btn = GPIO.input(Config.INFO_BTN)
            if btn == 0:  # Button pressed
                if menu_timer >= Config.REBOOT_TIMEOUT:
                    menu_state = 1
                    
                if menu_timer >= Config.SHUTDOWN_TIMEOUT:
                    menu_state = 2
                    
                disp_timer = Config.DISP_TIMEOUT
                menu_timer += 1
            else:
                if disp_timer == 0:
                    menu_timer = 0
                    set_leds(0, 0, 0)

            if disp_timer > 0:
                if menu_state == 2:
                    draw_shutdown(draw, font, width, height,menu_timer, btn == 1)
                    set_leds(0, 0, 1)
                    if btn == 1:
                        system_cmd(0,1)
                elif menu_state == 1:
                    draw_reboot(draw, font, width, height, menu_timer, btn == 1)
                    set_leds(1, 1, 0)
                    if btn == 1:
                        system_cmd(1,0)
                else:
                    draw_info(draw, font, width, height, disp_timer)
                    set_leds(0, 1, 0)
                    if btn == 1: # Button released
                        menu_timer = 0                    
                
                disp.image(image)
                disp.show()
                disp_timer -= 1

            else:
                disp.fill(0)   # Clear the display
                disp.show()
            
            time.sleep(1)

    except KeyboardInterrupt:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        disp.image(image)
        disp.show()
        set_leds(0, 0, 0)
        GPIO.cleanup()

if __name__ == "__main__":
    main()
