import concurrent.futures
import random
import keyboard
import pydirectinput
import pyautogui
import connect
import re
import math
from keys import *

blacklist = ['fuck', 'damn', 'dammit', 'ass', 'bitch', 'crap', 'cunt', 'dick', 'fag', 'nigg', 'piss', 'pussy', 'shit', 'slut', 'tits', 'boob', 'boner', 'balls', 'report', 'black', 'white', 'hallmonitor']
# ^^^ the blacklisted words for the chat command

##################### GAME VARIABLES #####################

# Replace this with your Twitch username. Must be all lowercase.
TWITCH_CHANNEL = 'fwtap' 

# If streaming on Youtube, set this to False
STREAMING_ON_TWITCH = True

# If you're streaming on Youtube, replace this with your Youtube's Channel ID
# Find this by clicking your Youtube profile pic -> Settings -> Advanced Settings
YOUTUBE_CHANNEL_ID = "CHANNEL_ID" 

# If you're using an Unlisted stream to test on Youtube, replace "None" below with your stream's URL in quotes.
# Otherwise you can leave this as "None"
YOUTUBE_STREAM_URL = None

##################### MESSAGE QUEUE VARIABLES #####################

# MESSAGE_RATE controls how fast we process incoming Twitch Chat messages. It's the number of seconds it will take to handle all messages in the queue.
# This is used because Twitch delivers messages in "batches", rather than one at a time. So we process the messages over MESSAGE_RATE duration, rather than processing the entire batch at once.
# A smaller number means we go through the message queue faster, but we will run out of messages faster and activity might "stagnate" while waiting for a new batch. 
# A higher number means we go through the queue slower, and messages are more evenly spread out, but delay from the viewers' perspective is higher.
# You can set this to 0 to disable the queue and handle all messages immediately. However, then the wait before another "batch" of messages is more noticeable.
MESSAGE_RATE = 0.5
# MAX_QUEUE_LENGTH limits the number of commands that will be processed in a given "batch" of messages. 
# e.g. if you get a batch of 50 messages, you can choose to only process the first 10 of them and ignore the others.
# This is helpful for games where too many inputs at once can actually hinder the gameplay.
# Setting to ~50 is good for total chaos, ~5-10 is good for 2D platformers
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100 # Maximum number of threads you can process at a time 

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
pyautogui.FAILSAFE = False

##########################################################

# Count down before starting, so you have time to load up the game
countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
    time.sleep(1)

if STREAMING_ON_TWITCH:
    t = connect.Twitch()
    t.twitch_connect(TWITCH_CHANNEL)
else:
    t = connect.YouTube()
    t.youtube_connect(YOUTUBE_CHANNEL_ID, YOUTUBE_STREAM_URL)

lastPot = time.time()

def handle_message(message):
    try:
        msg = message['message'].lower()
        username = message['username'].lower()

        # MODIFY THE BELOW CODE TO FIT YOUR MONITOR!!!!
        # -> Make sure your IN GAME UI SIZE IS "SMALL" ⚠️
        # -> Make sure your game is FULL SCREEN or BORDERLESS ⚠️
        # -> Make sure your game is the same resolution as your monitor ⚠️
        # -> Make sure the game is on your MAIN monitor (whatever "Monitor 1" is) ⚠️

        monitorWidth, monitorHeight = pyautogui.size()

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        monitor = 1
        if (monitorWidth != 1920):
            monitor = (monitorWidth/1920)
        if (monitorWidth != 1080):
            monitor = (monitorHeight/1080)
        

        print("[" + username + "]: " + msg)

        # Now that you have a chat message, this is where you add your game logic.
        # Use the "HoldKey(KEYCODE)" function to permanently press and hold down a key.
        # Use the "ReleaseKey(KEYCODE)" function to release a specific keyboard key.
        # Use the "HoldAndReleaseKey(KEYCODE, SECONDS)" function press down a key for X seconds, then release it.
        # Use the pydirectinput library to press or move the mouse

        if msg.startswith("chat"):
            words = msg.split(' ', 1)[1] # get all words after "chat"
            for word in blacklist:
                if re.search(word, words):
                    blacklisted_word = next(word for word in blacklist if word in words)
                    return print(username + '\'s message was blocked because it included the word "'+ blacklisted_word + '", - '+ msg)
            else:
                pydirectinput.press('enter')
                pyautogui.typewrite(username + ': ' + words)
                return pydirectinput.press('enter')

        if msg == 'screenshot' or msg == 'ss':
            pydirectinput.press('z')
            pydirectinput.press('z')

        if msg == 'stop':
            pydirectinput.keyUp('up')
            pydirectinput.keyUp('down')

        if msg == "walk":
            pyautogui.keyDown('w')
            pyautogui.keyUp('s')
            time.sleep(10)
            pyautogui.keyUp('w')
        
        if msg == "step forward":
            pyautogui.keyDown('w')
            time.sleep(0.1)
            pyautogui.keyUp('w')
            
        if msg == "step back":
            pyautogui.keyDown('s')
            time.sleep(0.1)
            pyautogui.keyUp('s')
            
        if msg == "back":
            pyautogui.keyDown('s')
            pyautogui.keyUp('w')
            time.sleep(10)
            pyautogui.keyUp('s')
            
        if msg == 'jump' or msg == 'next':
            pydirectinput.press("space")
        if msg == 'dialogue' or msg == 'npc':
            for i in range(10):
                pydirectinput.press("space")
        if msg == 'left':
            pydirectinput.keyDown('left')
            time.sleep(0.5)
            pydirectinput.keyUp('left')
        if msg == 'right':
            pydirectinput.keyDown('right')
            time.sleep(0.5)
            pydirectinput.keyUp('right')
        if msg == 'short left' or msg == 'shortleft' or msg == 'sleft':
            pydirectinput.keyDown('left')
            time.sleep(0.25)
            pydirectinput.keyUp('left')
        if msg == 'short right' or msg == 'shortright' or msg == 'sright':
            pydirectinput.keyDown('right')
            time.sleep(0.25)
            pydirectinput.keyUp('right')
        if msg == 'backpack':
            pydirectinput.press("b")
        if msg == 'quest':
            pydirectinput.press('q')
        if msg == 'deck':
            pydirectinput.press('p')
        if msg == 'friend':
            pydirectinput.press('f')
        if msg == 'map':
            pydirectinput.press('m')
        if msg == 'interact' or msg == 'x':
            pydirectinput.press('x')
        if msg == 'navigate':
            pydirectinput.press('n')
        if msg == 'pet':
            pydirectinput.press('i')
        if msg == 'character':
            pydirectinput.press('c')
        if msg == 'esc':
            pydirectinput.press('esc')

#        if msg == 'commons':
#           pyautogui.press('end')
#        if msg == 'home':
#            pyautogui.press('home')

# remove the hashtag in front of these if you want these enabled ^ 

        if msg == 'return':
            pyautogui.press('pageup')
        if msg == 'mark':
            pyautogui.press('pagedown')

        global lastPot
        pot_delay = 60 #You can replace pot_delay with the amount of seconds you want your chat to be able to use potions. (60 means potion can only be used once a minute.)
        if msg == 'pot' or msg == 'potion':
            if time.time() - lastPot >= pot_delay: 
                with pyautogui.hold('CTRL'):
                    pyautogui.press('O')
                lastPot = time.time()
            else: 
                print('-> [⚠️  ANTI-ABUSE] '+ username +f' used "pot" before {pot_delay} seconds... wait {60 - math.ceil(time.time() - lastPot)} more seconds.')

        if msg == 'gg':
            pydirectinput.press('enter')
            pyautogui.typewrite('GG')
            pydirectinput.press('enter')

        def resetMouse():
            pydirectinput.moveTo(90*int(monitor), 1000*int(monitor))

        if msg == 'spell1' or msg == 'spell 1':
            pydirectinput.moveTo(760*int(monitor), 530*int(monitor))
            pydirectinput.click()
            resetMouse()
        if msg == 'spell2' or msg == 'spell 2':
            pydirectinput.moveTo(840*int(monitor), 530*int(monitor))
            pydirectinput.click()
            resetMouse()
        if msg == 'spell3' or msg == 'spell 3':
            pydirectinput.moveTo(920*int(monitor), 530*int(monitor))
            pydirectinput.click()
            resetMouse()
        if msg == 'spell4' or msg == 'spell 4':
            pydirectinput.moveTo(1000*int(monitor), 530*int(monitor))
            pydirectinput.click()
            resetMouse()
        if msg == 'spell5' or msg == 'spell 5':
            pydirectinput.moveTo(1080*int(monitor), 530*int(monitor))
            pydirectinput.click()
            resetMouse()
        if msg == 'spell6' or msg == 'spell 6':
            pydirectinput.moveTo(1160*int(monitor), 530*int(monitor))
            pydirectinput.click()
            resetMouse()
        if msg == 'spell7' or msg == 'spell 7':
            pydirectinput.moveTo(1240*int(monitor), 530*int(monitor))
            pydirectinput.click()
            resetMouse()
        
        if msg == 'ds1' or msg == 'discard 1':
            pydirectinput.moveTo(760*int(monitor), 530*int(monitor))
            pydirectinput.rightClick()
            resetMouse()
        if msg == 'ds2' or msg == 'discard 2':
            pydirectinput.moveTo(840*int(monitor), 530*int(monitor))
            pydirectinput.rightClick()
            resetMouse()
        if msg == 'ds3' or msg == 'discard 3':
            pydirectinput.moveTo(920*int(monitor), 530*int(monitor))
            pydirectinput.rightClick()
            resetMouse()
        if msg == 'ds4' or msg == 'discard 4':
            pydirectinput.moveTo(1000*int(monitor), 530*int(monitor))
            pydirectinput.rightClick()
            resetMouse()
        if msg == 'ds5' or msg == 'discard 5':
            pydirectinput.moveTo(1080*int(monitor), 530*int(monitor))
            pydirectinput.rightClick()
            resetMouse()
        if msg == 'ds6' or msg == 'discard 6':
            pydirectinput.moveTo(1160*int(monitor), 530*int(monitor))
            pydirectinput.rightClick()
            resetMouse()
        if msg == 'ds7' or msg == 'discard 7':
            pydirectinput.moveTo(1240*int(monitor), 530*int(monitor))
            pydirectinput.rightClick()
            resetMouse()

        if msg == 'p1' or msg == 'player 1':
            pydirectinput.moveTo(1578*int(monitor), 1011*int(monitor))
            pydirectinput.click()
        if msg == 'p2' or msg == 'player 2':
            pydirectinput.moveTo(1147*int(monitor), 1011*int(monitor))
            pydirectinput.click()
        if msg == 'p3' or msg == 'player 3':
            pydirectinput.moveTo(726*int(monitor), 1011*int(monitor))
            pydirectinput.click()
        if msg == 'p4' or msg == 'player 4':
            pydirectinput.moveTo(380*int(monitor), 1011*int(monitor))
            pydirectinput.click()
        if msg == 'mob1' or msg == 'mob 1':
            pydirectinput.moveTo(190*int(monitor), 40*int(monitor))
            pydirectinput.click()
        if msg == 'mob2' or msg == 'mob 2':
            pydirectinput.moveTo(630*int(monitor), 40*int(monitor))
            pydirectinput.click()
        if msg == 'mob3' or msg == 'mob 3':
            pydirectinput.moveTo(1064*int(monitor), 40*int(monitor))
            pydirectinput.click()
        if msg == 'mob4' or msg == 'mob 4':
            pydirectinput.moveTo(1493*int(monitor), 40*int(monitor))
            pydirectinput.click()

        if msg == 'pass':
            pydirectinput.moveTo(728*int(monitor), 642*int(monitor))
            pydirectinput.click()
        if msg == 'draw':
            pydirectinput.moveTo(950*int(monitor), 636*int(monitor))
            pydirectinput.click()
        
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))

ms = 0
while True:
    ms += 1
    # print(ms)
    if ms >= 10000:
        print("-> [ANTI-AFK] Running anti-afk to avoid disconnection.")
        ms = 0
        pyautogui.keyDown("A")
        time.sleep(0.1)
        pyautogui.keyUp("A")
        time.sleep(0.1)
        pyautogui.keyDown("D")
        time.sleep(0.1)
        pyautogui.keyUp("D")

    active_tasks = [t for t in active_tasks if not t.done()]

    #Check for new messages
    new_messages = t.twitch_receive_messages();
    if new_messages:
        message_queue += new_messages; # New messages are added to the back of the queue
        message_queue = message_queue[-MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

    messages_to_handle = []
    if not message_queue:
        # No messages in the queue
        last_time = time.time()
    else:
        # Determine how many messages we should handle now
        r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            # Pop the messages we want off the front of the queue
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time();

    # If user presses Shift+Backspace, automatically end the program
    if keyboard.is_pressed('shift+backspace'):
        exit()

    if not messages_to_handle:
        continue
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(thread_pool.submit(handle_message, message))
            else:
                print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')
 
