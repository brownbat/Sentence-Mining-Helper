# Sentence Mining Helper
 Sentence mining functions inspired by Giovanni Smith's Sentence Mining Scripts

See here for more info: 
https://github.com/GiovanniSmith/SentenceMiningFormAndScripts

See this video to set up ShareX and understand usage:
https://www.youtube.com/watch?v=P_nV8RPj_wE

You will also need to enable clipboard history in Windows settings for this version,
but you will not need to install AutoHotKey or Ditto.

Big picture, the goal is to perform the following functions:
1. record audio and take a screenshot
a. record audio using a prebuilt and hotkeyed sharex command
b. take screenshot using sharex cropped screenshot region
2. paste audio and screenshot from windows clipboard
3. paste most recent n clipboard items (for sharex commands that add a series of
subtitles to the clipboard in a row)

Differences from GS's scripts:
- simple checks to ensure correct window selected
- cannot choose between spacebar and left click to start video
- currently only works with VLC
- doesn't require ditto or autohotkey
- does require some pip installed python dependencies
- can't time screenshot before/after audio
- sharex wait time after a system wait command so your value can be smaller

TODO:
- support streaming services, at least netflix, youtube, iqiyi
- support other local media players
- support Pact style timestamp selection for clips
- improve ocr
- save files locally instead of using the clipboard to reduce volatility
-- this might be impractical because of lower speed
- automatically tab to anki window to paste after captures
- adjust pysimplegui visual appearance, try to give it focus


- detect and adjust system and sharex wait times dynamically
the following code might work, but it produced unexpectedly huge times when tested
you have to first take a screenshot of the start/stop/abort buttons sharex adds
while recording, then save that as sharex_status.bmp in the script directory
even then the results it produces are so badly tuned as to be unworkable)

``` python
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
```
