#! /usr/bin/python

import time
import Adafruit_CharLCD as LCD
from datetime import datetime
from spark import send_message_to_email
import signal
from config import dad_email

lcd = LCD.Adafruit_CharLCDPlate()

lcd.set_color(1,0,0)
lcd.clear()
# lcd.message("Hello")

time_format = "%I:%M %p"

menu_options = [
    "Hello", 
    "I am playing Minecraft", 
    "Call me soon please!", 
    "Have a good day.", 
    "I love you Daddy!", 
    "I'm watching a movie.", 
    "I'm watching a movie on my phone", 
    "I miss you very so much", 
    "I miss you very very so much", 
    "I miss you very very very so much"
    ]

buttons = ( (LCD.SELECT, 'Select' ),
            (LCD.LEFT,   'Left'   ),
            (LCD.UP,     'Up'     ),
            (LCD.DOWN,   'Down'   ),
            (LCD.RIGHT,  'Right'  )  

          )

def get_time():
    now = datetime.now()
    return now.strftime(time_format)
    
def change_menu_position(position, action):
    option_count = len(menu_options)
    if action == "Up":
        position = position + 1
    elif action == "Down":
        position = position -1
    else:
        position = 0
        
    if position > option_count - 1:
        position = 0
    elif position < 0: 
        position = option_count -1 
    
    return position

def sigterm_handler(_signo, _stack_frame):
    "When sysvinit sends the TERM signal, cleanup before exiting."
    print("[" + get_time() + "] received signal {}, exiting...".format(_signo))
#     cleanup_pins()
    sys.exit(0)
signal.signal(signal.SIGTERM, sigterm_handler)

menu_position = 0
new_menu = False

# Startup Messages
print(get_time() + ": Clock Started Up.")
send_message_to_email(dad_email, "Clock Started up.")

while True:
    t_msg = get_time()

    # check if button pressed 
    for button in buttons:
        if lcd.is_pressed(button[0]):
            # if Select is pressed, send message 
            if button[0] in [LCD.SELECT]:
                print(get_time() + ": Sending Message")
                lcd.clear()
                lcd.message("Sending message!")
                send_message_to_email(dad_email, menu_options[menu_position])
            # if up or down, change the menu_position value 
            if button[0] in [LCD.UP, LCD.DOWN]:
                menu_position = change_menu_position(menu_position, button[1])
                new_menu = True
            lcd.clear()

    m_msg = "Say '%s'" % (menu_options[menu_position])
    m_msg_len = len(m_msg)

    message = t_msg + "\n" + m_msg

    lcd.message(message)
    if m_msg_len >= 16 and new_menu: 
        shifts = m_msg_len - 15
        i = 0
        while i < shifts:
            lcd.move_left()
            i = i + 1
            time.sleep(0.5)
        new_menu = False
        time.sleep(0.5)
    lcd.home()

#     time.sleep(3.0)


