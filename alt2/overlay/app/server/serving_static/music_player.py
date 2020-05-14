import mpd
import gpiod
import os
import signal
import sys
from time import time_ns

mpc = mpd.MPDClient()

def start():
    mpc.clear()
    mpc.update()
    for song in os.listdir("/music/"):
        print(song + "  DEBUGGING")
        mpc.add(song)
    mpc.play()

def stop():
    mpc.stop()

def volume_up():
    value = min(int(mpc.status()['volume']) + 10, 100)
    mpc.setvol(value)

def volume_down():
    value = max(int(mpc.status()['volume']) - 10, 0)
    mpc.setvol(value)

def next_song():
    mpc.next()
    mpc.play()


def cleanup(signo, frame):
    mpc.close()
    mpc.disconnect()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup)

    mpc.connect("localhost",6600)

    chip = gpiod.Chip("gpiochip0")
    buttons2 = [12,13,14,15]
    buttons = chip.get_lines(buttons2)
    buttons.request(consumer='mychip', type=gpiod.LINE_REQ_EV_FALLING_EDGE)

    is_playing = False
    start_time = time_ns() // 1000000
    threshold = 250

    while(True):
        lines = buttons.event_wait(sec=1)

        if lines:
            for line in lines:
                event = line.event_read()
                button = event.source.offset()

                interval = time_ns() // 1000000  - start_time
                start_time = time_ns() // 1000000

                if interval < threshold:
                    continue

                if button == 12:
                    if is_playing:
                        stop()
                    else:
                        start()
                        print("Playing: " + mpc.currentsong()['file'])

                    is_playing = not is_playing
                elif button == 13:
                    if is_playing:
                        next_song()
                        print("Playing: " + mpc.currentsong()['file'])
                elif button == 14:
                    volume_down()
                    print("volume: " + mpc.status()['volume'])
                elif button == 15:
                    volume_up()
                    print("volume: " + mpc.status()['volume'])
                else:
                    pass
