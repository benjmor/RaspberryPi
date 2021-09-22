import RPi.GPIO as GPIO
import time

# Configure the Pi to use the BCM (Broadcom) pin names, rather than the pin position
GPIO.setmode(GPIO.BCM)
red_pin = 18
green_pin = 23
blue_pin = 24
yellow_switch_pin = 8
purple_switch_pin = 7
buzzer_pin = 21

# define musical notes
B0=31
C1=33
CS1=35
D1=37
DS1=39
E1=41
F1=44
FS1=46
G1=49
GS1=52
A1=55
AS1=58
B1=62
C2=65
CS2=69
D2=73
DS2=78
E2=82
F2=87
FS2=93
G2=98
GS2=104
A2=110
AS2=117
B2=123
C3=131
CS3=139
D3=147
DS3=156
E3=165
F3=175
FS3=185
G3=196
GS3=208
A3=220
AS3=233
B3=247
C4=262
CS4=277
D4=294
DS4=311
E4=330
F4=349
FS4=370
G4=392
GS4=415
A4=440
AS4=466
B4=494
C5=523
CS5=554
D5=587
DS5=622
E5=659
F5=698
FS5=740
G5=784
GS5=831
A5=880
AS5=932
B5=988
C6=1047
CS6=1109
D6=1175
DS6=1245
E6=1319
F6=1397
FS6=1480
G6=1568
GS6=1661
A6=1760
AS6=1865
B6=1976
C7=2093
CS7=2217
D7=2349
DS7=2489
E7=2637
F7=2794
FS7=2960
G7=3136
GS7=3322
A7=3520
AS7=3729
B7=3951
C8=4186
CS8=4435
D8=4699
DS8=4978

GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(yellow_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(purple_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Utility function to turn the gree LED on and the red off
def green():
    GPIO.output(green_pin, True)
    GPIO.output(red_pin, False)
    GPIO.output(blue_pin, False)

# Utility function to turn the red LED on and the green off
def red():
    GPIO.output(green_pin, False)
    GPIO.output(red_pin, True)
    GPIO.output(blue_pin, False)

# Turn all off
def off():
    GPIO.output(green_pin, False)
    GPIO.output(red_pin, False)
    GPIO.output(blue_pin, False)

def yellow():
    GPIO.output(green_pin, True)
    GPIO.output(red_pin, True)
    GPIO.output(blue_pin, False)

def purple():
    GPIO.output(green_pin, False)
    GPIO.output(red_pin, True)
    GPIO.output(blue_pin, True)
    
def white():
    GPIO.output(green_pin, True)
    GPIO.output(red_pin, True)
    GPIO.output(blue_pin, True)
    
# find which buttons pressed -1 means neither, 0=both, 1=red, 2=green
def key_pressed():
    # if button is pressed GPIO.input will report false for that input
    if GPIO.input(yellow_switch_pin) and GPIO.input(purple_switch_pin):
        return 0
    if not GPIO.input(yellow_switch_pin) and not GPIO.input(purple_switch_pin):
        return -1
    if not GPIO.input(yellow_switch_pin) and GPIO.input(purple_switch_pin):
        return 1
    if GPIO.input(yellow_switch_pin) and not GPIO.input(purple_switch_pin):
        return 2

def buzz(buzzer_pin, freq=440):
    Buzz = GPIO.PWM(buzzer_pin, freq)
    Buzz.start(50)
    Buzz.ChangeFrequency(freq)
    time.sleep(0.7)
    Buzz.stop()

# Tell the computer if the user's response was correct. Give a point if correct.
# No penalty if incorrect
def validate_response():
    correct = raw_input("Correct response? Y/N\n")
    if (correct == "Y" or correct == "y"):
        green()
        buzz(buzzer_pin, A5)
        return 1
    else:
        red()
        buzz(buzzer_pin, A3)
        return 0

yellow_score = 0
purple_score = 0
#number of seconds participants have to respond
seconds = 5

print("Starting up...")
off()
while True:
    go = raw_input("Hit enter when you've completed reading the question. Enter c to exit\n")
    if (go == "c" or go == "C"):
        break
    white()
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            print("Time up!")
            buzz(buzzer_pin, E3)
            buzz(buzzer_pin, A2)
            break
        else:
            time.sleep(0.05)
            if not key_pressed():
                pass
            elif (key_pressed() == 1):
                print("yellow")
                yellow()
                buzz(buzzer_pin, A4)
                yellow_score += validate_response()
                break
            elif (key_pressed() == 2):
                print("purple")
                purple()
                buzz(buzzer_pin, D4)
                purple_score += validate_response()
                break
    print("Current scores: Yellow has {} points. Purple has {} points.\n".format(yellow_score, purple_score))
    off()

print("Final scores: Yellow has {} points. Purple has {} points.\n".format(yellow_score, purple_score))
print("Cleaning up")
GPIO.cleanup()
