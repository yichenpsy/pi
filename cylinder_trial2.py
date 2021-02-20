# WS2812 LED Matrix Cylinder
# by M Oehler
# https://hackaday.io/project/162035-led-matrix-cylinder
# Released under a "Simplified BSD" license

import time, random, sys
import argparse
from font5x3 import font5x3
from itertools import chain
import numpy

# False for simulation mode, True for using a Raspberry PI
PI=True

if PI:
    from neopixel import *
else:
    import pygame
    from pygame.locals import *


#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 255,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 255)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (255, 255,   0)
LIGHTYELLOW = (175, 175,  20)
CYAN        = (  0, 255, 255)
MAGENTA     = (255,   0, 255)
ORANGE      = (255, 100,   0)

#BORDERCOLOR = BLUE
#BGCOLOR = BLACK
#TEXTCOLOR = WHITE
#TEXTSHADOWCOLOR = GRAY
#COLORS      = (BLUE,GREEN,RED,YELLOW,CYAN,MAGENTA,ORANGE)
#LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

# LED strip configuration:
LED_COUNT      = 150     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 2     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

if PI:
    # Create NeoPixel object 
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Init lib
    strip.begin()
else:
    strip=[]


# Main program logic follows:
def main():
    global FPSCLOCK, DSPLAYSURF, BASICFONT, BIGFONT
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            user_input = input("Enter mode (You have three modes: RandomColors, ColorWipe, Read, Date): \n")
            
            if user_input.lower() == 'read':
                mode = input('Enter the mode you want to display (1=>2=>3 =>warmer): ')
                while True:
                    try:
                        if int(mode) == 1:
                            brightness = input('Enter the brightness (0 to 255): \n')
                            strip_modified = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, int(brightness), LED_CHANNEL)
                            strip_modified.begin()
                            for i in range(strip_modified.numPixels()):
                                strip_modified.setPixelColor(i, Color(255,255,255))
                            strip_modified.show()
                        elif int(mode) == 2:
                            brightness = input('Enter the brightness (0 to 255): \n')
                            strip_modified = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, int(brightness), LED_CHANNEL)
                            strip_modified.begin()
                            for i in range(strip.numPixels()):
                                strip_modified.setPixelColor(i, Color(150,255,40))
                            strip_modified.show()
                        elif int(mode) == 3:
                            brightness = input('Enter the brightness (0 to 255): \n')
                            strip_modified = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, int(brightness), LED_CHANNEL)
                            strip_modified.begin()
                            for i in range(strip.numPixels()):
                                strip_modified.setPixelColor(i, Color(100,255,0))
                            strip_modified.show()
                            
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break
                        
            elif user_input.lower() == "randomcolors":
                while True:
                    try:
                        colorRandom_new(strip, 5000)
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break
                    
            elif user_input.lower() == "date":
                color1 = 0x96FFCF
                color2 = 0x00FF00
                
                brightness = 5

                ls = [i for i in range(LED_COUNT)]
                ls_subs = [ls[i:i+10] for i in range(0, LED_COUNT, 10)]
                
                colorWipe_new(strip, color1)
                
                def picky(ls):
                    pick = []
                    n=2
                    for i in ls:
                        for j in range(n):
                            pick.append(random.choice(i))
                    return pick
                
                def lovespark(strip, ls, color1, color2, brightness):
                    for i in ls:
                        strip.setPixelColor(i, color2)
                    strip.show()
                    rebirth(brightness)
                    time.sleep(0.5)
                    for i in ls:
                        strip.setPixelColor(i, color1)
                    strip.show()

                while True:
                    try:
                        spark_spot = picky(ls_subs)
                        lovespark(strip, spark_spot, color1, color2, brightness)
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break
            
            elif user_input.lower() == "dim":
                brightness = 10
                while True:
                    try:
                        for i in range(LED_COUNT):
                            strip.setPixelColor(i, Color(0,255,0))
                        strip.show()
                        rebirth(brightness)
                    except KeyboardInterrupt: 
                        colorWipe_new(strip, Color(0,0,0))
                        break

            elif user_input.lower() == "colorwipe":
                while True:
                    try:
                        colorWipe_new(strip, Color(255,255,255))  # Blue wipe
                        colorWipe_new(strip, Color(255, 255, 0))  # Green wipe
                       # colorWipe_new(strip, Color(242, 185, 15))  # Blue wipe
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break
            
            elif user_input.lower() == "nightstar":
                ls = [i for i in range(LED_COUNT)]
                ls_sub = [ls[i:i+10] for i in range(0, LED_COUNT, 10)]
                brightness = 100
                
                def picky(ls, n):
                    pick = []
                    for i in ls:
                        for j in range(n):
                            pick.append(random.choice(i))
                    return pick
                
                def nightstar(n):
                    spark_spot = picky(ls_sub, n)
                    for i in spark_spot:
                        strip.setPixelColor(i, Color(248,252,3))
                    strip.show()
                    rebirth(brightness)
                    rebirth(brightness)
                    for i in spark_spot:
                        strip.setPixelColor(i, Color(0,0,0))
                    strip.show()

                def nightstar_reversed(n):
                    spark_spot = picky(ls_sub, n)
                    strip.setBrightness(10)
                    strip.show()
                    for i in spark_spot:
                        strip.setPixelColor(i, Color(248,252,3))
                    strip.show()
                    rebirth_reversed(brightness)
                    rebirth_reversed(brightness)
                    for i in spark_spot:
                       strip.setPixelColor(i, Color(0,0,0))
                    strip.show()

                while True:
                    try:
                        nightstar(5)
                        '''
                        #nightstar_reversed(5)
                        spot = picky(ls_sub, 5)
                        for count in range(2):
                            b = 10
                            strip.setBrightness(b)
                            strip.show()
                            for i in spot:
                                strip.setPixelColor(i, Color(248,252,3))
                            strip.show()
                            
                            while b < 100:
                                b += 10
                                strip.setBrightness(b)
                                strip.show()
                                time.sleep(0.12)

                            while b > 0:
                                b -= 10
                                strip.setBrightness(b)
                                strip.show()
                                time.sleep(0.12)
                        for i in spot:
                            strip.setPixelColor(i, Color(0,0,0))
                        strip.show()
                        '''
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break
            else:
                print('You have entered the mode wrong!')
    except KeyboardInterrupt:
        if args.clear:
            colorWipe_new(strip, Color(0,0,0))

def colorWipe(strip, r,g,b, wait_ms=50):
    for i in range(LED_COUNT):
        draw_pixel(int(i%20),int(i/20),r,g,b)
        time.sleep(wait_ms/1000.0)
        
def colorWipe_new(strip, color1, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color1)
        strip.show()
        time.sleep(wait_ms/1000.0)

def colorRandom(strip, cycles):
    for i in range(0,cycles):
        a= random.randrange(0,200,1)
        c=random.randrange(0,0xFFFFFF,1)
        drawPixel(int(a%20),int(a/20),c)
        time.sleep(1/1000.0)
        
def colorRandom_new(strip,cycles):
    for i in range(cycles):
        a = random.randrange(0, 200, 1)
        c=random.randrange(0,0xFFFFFF,1)
        drawPixel_new(a, c)
        time.sleep(1/1000.0)
        
def drawPixel_new(x, color):
    if color == None:
        return
    if PI:
        if (x>0 and color>=0):
            strip.setPixelColor(x, color)
            strip.show()
        
def drawPixel(x,y,color):
    if color == None:
        return
    if PI:
        if (x>=0 and y>=0 and color >=0):
            strip.setPixelColor(y*20+x,color)
            strip.show()
    else:
        pygame.draw.rect(DISPLAYSURF, (color>>16,(color>>8)&0xFF,color&0xFF), (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()



def draw_pixel(x,y,r,g,b):
    if PI:
        strip.setPixelColor(matrix[y*20+x],Color(g, r, b))
        strip.show()
    else:
        pygame.draw.rect(DISPLAYSURF, (r,g,b), (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()

def rebirth(brightness):
    n = brightness
    while brightness > 0:
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(0.12)
        brightness -= 10
    while brightness < n:
        brightness += 10
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(0.12)

def rebirth_reversed(brightness):
    n = brightness
    while brightness < n:
        brightness += 10
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(0.12)

    while brightness > 0:
        brightness -= 10
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(0.12)

if __name__ == '__main__':
    main()
