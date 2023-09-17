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
    # TODO: test if this exit actually works
    exit()


def start_stop_recording():
    vlc_window.activate()
    system_wait()

    global is_recording

    if not is_recording:
        keyboard.send("space")  # start/stop player
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
        print(f"Anki's Add card window is not active. Current active window: " +
              f"{active_window_title}")
        print(f"Please select Anki's Add card window to continue...")
        # wait for Add to be active
        while "Add" not in active_window_title:
            active_window_title = pyautogui.getActiveWindow().title
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

    layout = [[sg.Text("How many images have you captured?")],
              [sg.InputText(key='-IN-', focus=True)], [sg.OK()]]
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
