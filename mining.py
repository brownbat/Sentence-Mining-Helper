'''
Sentence mining app inspired by Giovanni Smith's Sentence Mining Scripts

Perform the following functions:
1. record audio and take a screenshot
a. record audio using sharex key command
b. take screenshot using sharex cropped screenshot region
2. paste audio and screenshot from windows clipboard
3. paste most recent n clipboard items (for sharex commands that add a series of
subtitles to the clipboard in a row)

Difference from GS's scripts:
- simple checks to ensure correct window selected
- can't choose between spacebar and left click to start video
- currently only works with VLC
- doesn't require ditto or autohotkey
- does require some pip installed python dependencies
- can't time screenshot before/after audio
- sharex wait time after a system wait command so your value can be smaller

TODO:
- support streaming services, at least netflix and youtube
- support Pact style timestamp selection for clips
- improve ocr
- save files locally instead of using the clipboard to reduce volatility
-- this might be impractical because of speed
- detect and adjust system and sharex wait times
the following code might work, but it produced unexpectedly huge times when tested
you have to first take a screenshot of the start/stop/abort buttons sharex adds
while recording, then save that as sharex_status.bmp in the script directory
even then the results it produces are so badly tuned as to be unworkable)

    wait_for_recording():
        while True:
            global region
            location = pyautogui.locateOnScreen('sharex_status.bmp')
            if location is not None:
                print(location)
                if region is None:
                    region = (location.left-50, location.top-50, location.width+100, location.height+100)
                break  # the recording has started, break out of the loop
            time.sleep(0.1)  # wait a bit before trying again
            print('recording not started')

            
    def test_recording_delay():
        for _ in range(3):
            keyboard.send("ctrl+alt+r")  # start recording
            start_time = time.perf_counter()
            wait_for_recording()
            end_time = time.perf_counter()
            print(f'Recording started in {(end_time - start_time) * 1000:.2f} ms')

            time.sleep(0.500)  # Wait for a moment to ensure the recording has fully started

            keyboard.send("ctrl+alt+r")  # stop recording
            time.sleep(0.500)  # Wait for a moment to ensure the recording has fully stopped

    test_recording_delay()
'''

import keyboard
import time
import pyautogui
import PySimpleGUI as sg

is_recording = False
vlc_window = None

system_wait_time = 0.350
sharex_wait_time = 0.200

def system_wait():
    time.sleep(system_wait_time)
    
def sharex_wait():
    time.sleep(sharex_wait_time)


# find VLC window
for window in pyautogui.getAllWindows():
    if "VLC" in window.title:
        vlc_window = window
if vlc_window is None:
    print("Could not find VLC")
    #TODO: test if this exit actually works
    exit()


def start_stop_recording():
    vlc_window.activate()
    system_wait()
    
    global is_recording
 
    if not is_recording:
        keyboard.send("space") # start/stop player
        system_wait()
        keyboard.send("ctrl+alt+r")  # start recording
        is_recording = True
        system_wait()
        sharex_wait()
        keyboard.send("ctrl+alt+s")  # grab screenshot
        system_wait()
    else:
        keyboard.send("ctrl+alt+r")  # stop recording
        system_wait()
        keyboard.send("space")
        system_wait()
        is_recording = False


def wait_add_card_active():
    active_window_title = pyautogui.getActiveWindow().title
    # warn if "Add" is in the title
    if "Add" not in active_window_title:
        print(f"Anki's Add card window is not active. Current active window: {active_window_title}")
        print(f"Please select Anki's Add card window to continue...")
        # wait for Add to be active
        while "Add" not in active_window_title:
            active_window_title = pyautogui.getActiveWindow().title  # Update the window title
            time.sleep(0.500)


def paste_audio_screenshot():
    wait_add_card_active()
    system_wait()
    keyboard.send("ctrl+v")  # paste audio
    system_wait()
    keyboard.send("enter")  # enter return
    system_wait()
    keyboard.send("win+v")  # open clipboard history
    system_wait()
    keyboard.send("enter")  # select first item (screenshot) and paste
    system_wait()


def paste_clipboard_items():
    wait_add_card_active()
    system_wait()

    layout = [[sg.Text("How many images have you captured?")], [sg.InputText(key='-IN-', focus=True)], [sg.OK()]]
    window = sg.Window("Image Count", layout, finalize=True)
    window.bring_to_front()  # bring the window to the front
    system_wait()
    window.Element('-IN-').SetFocus()  # set focus on input box
    system_wait()
    event, values = window.read()
    window.close()
    system_wait()

    count = int(values['-IN-'])
    for i in range(count):
        keyboard.send("win+v")  # open clipboard history
        system_wait()
        for _ in range(count - i - 1):
            keyboard.send("down")  # navigate to the appropriate clipboard item
            system_wait()
        keyboard.send("enter")  # select item and paste
        system_wait()
        keyboard.send("enter")  # add a line return to separate values
        system_wait()


keyboard.add_hotkey("ctrl+shift+f1", start_stop_recording)
keyboard.add_hotkey("ctrl+shift+f2", paste_audio_screenshot)
keyboard.add_hotkey("ctrl+shift+f3", paste_clipboard_items)
keyboard.wait()

