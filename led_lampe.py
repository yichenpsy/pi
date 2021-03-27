# WS2812 LED Lamp
# by Gruppe H

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
LED_COUNT      = 85     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
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
            user_input = input("Enter mode (You have eight modes: color light, party, Disco, Christmas, Rainbow, Read, Date, Sleep): ")
            #### read
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
                    
            ### color light
            elif user_input.lower() == 'color light':
                while True:
                    try:
                        color = input('Enter the color you want to display (green, red, blue )')
                        while True:
                            try:
                                if color == "green":
                                    color_display = Color(255,0,0)
                                elif color == "red":
                                    color_display = Color(0,255,0)
                                elif color == "blue":
                                    color_display = Color(0,0,225)
                                for i in range(strip.numPixels()):                               
                                    strip.setPixelColor(i, color_display)
                                strip.show()
                            except KeyboardInterrupt:
                                colorWipe_new(strip, Color(0,0,0))
                                break
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break                    

            ##### Family party         
            elif user_input.lower() == "party":
                while True:
                    try:
                        colorRandom_new(strip, 5000)
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break
                    
             ##### Disco         
            elif user_input.lower() == "disco":
                while True:
                    try:
                            strip_disco = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, 50, LED_CHANNEL)
                            strip_disco.begin()
                            while True:
                                color = random.randrange(0,0xFFFFFF,1)
                                for i in range(strip_disco.numPixels()):
                                    strip_disco.setPixelColor(i, color)
                                strip_disco.show()
                                time.sleep(0.1)
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break      
            #### Date       
            elif user_input.lower() == "date":
                color1 = Color(100,255,150)
                color2 = 0x00FF00
                
                ls = [i for i in range(LED_COUNT)]
                ls_subs = [ls[i:i+10] for i in range(0, LED_COUNT, 10)]
                
                colorWipe_new(strip, color1)
                    
                while True:
                    try:
                        spark_spot = picky(ls_subs,3)
                        lovespark(strip, spark_spot, color1, color2, random.uniform(2.0,3.0))
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break

            #### night       
            elif user_input.lower() == "night":
                color1 = Color(0,0,100)  # base color  blue
                color2 = Color(126,242,24)  # gelb
                
                ls = [i for i in range(LED_COUNT)]
                ls_subs = [ls[i:i+10] for i in range(0, LED_COUNT, 10)]
                
                colorWipe_new(strip, color1)
                    
                while True:
                    try:
                        spark_spot1 = picky(ls_subs,4)
                        lovespark(strip, spark_spot1, color1, color2, random.uniform(0.8,2.0))

   
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break
                    
            #### colorwipe        
            elif user_input.lower() == "colorwipe":
                while True:
                    try:
                        colorWipe_new(strip, Color(255,255,255))  # white
                        colorWipe_new(strip, Color(255, 255, 0))  # yellow
                        colorWipe_new(strip, Color(255, 0, 255))  # 
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break
     
                    
            #### rainbow       
            elif user_input.lower() == "rainbow":
                while True:
                    try:
                        rainbow(strip)
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break

            #### Christmas      
            elif user_input.lower() == "christmas":
                while True:
                    try:
                        colorWipe_new(strip, Color(0,255,0),20)  # red
                        colorWipe_new(strip, Color(255,0,0),70)  # green
                        theaterChase(strip, Color(255, 255, 0),100) # yellow
                        theaterChase(strip, Color(0, 255, 0),100)
                        theaterChase(strip, Color(255, 0, 0),100)
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break
            ### sleep        
            elif user_input.lower() == "sleep":
                ls = [i for i in range(LED_COUNT)]
                ls_sub = [ls[i:i+10] for i in range(0, LED_COUNT, 10)]
                brightness = 255
                
                while True:
                    try:
                        nightstar(ls_sub, 3, brightness)
                    except KeyboardInterrupt:
                        colorWipe_new(strip, Color(0,0,0))
                        break                    
                    
                    
            else:
                print('You have entered the mode wrong!')

    except KeyboardInterrupt:
        if args.clear:
            colorWipe_new(strip, Color(0,0,0))



##### Methods
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
        
        ## rainbow
def colorWipe_rb(strip, color1, wait_ms=10):
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

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
        
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def picky(ls,n=2):
    pick = []
    for i in ls:
        for j in range(n):
            pick.append(random.choice(i))
    return pick
                    
def lovespark(strip, ls, color1, color2, sleep=2):
    for i in ls:
        strip.setPixelColor(i, color2)
    strip.show()
    time.sleep(sleep)
    for i in ls:
        strip.setPixelColor(i, color1)
    strip.show()

def nightstar(ls_sub, n, brightness):
    spark_spot = picky(ls_sub, n)
    for i in spark_spot:
        strip.setPixelColor(i, Color(100,255,3))
    strip.show()
    rebirth(brightness)
    for i in spark_spot:
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

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


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
                    
if __name__ == '__main__':
    main()
