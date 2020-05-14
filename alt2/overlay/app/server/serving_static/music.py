import gpiod
import sys
import time
import mpd
import json

client = mpd.MPDClient()
chip = gpiod.Chip("gpiochip0")

def light():
    with gpiod.Chip('gpiochip0') as chip:
        lines = chip.get_lines([ 24, 25, 26, 27])
        lines.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_OUT)
        vals = lines.set_values([1 ,1, 1, 1])

def dark():
    with gpiod.Chip('gpiochip0') as chip:
        lines = chip.get_lines([ 24, 25, 26, 27])
        lines.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_OUT)
        vals = lines.set_values([0, 0, 0, 0])

if __name__ == "__main__":
    
    playing = False
    client.connect("localhost", 6600)
    buttons2 = [12,13,14,15]
    buttons = chip.get_lines(buttons2)
    buttons.request(consumer='mychip', type=gpiod.LINE_REQ_EV_FALLING_EDGE)
    while(True):
        lines = buttons.event_wait(sec=2)
        client.update()
        if(lines):
            for line in lines:
                event = line.event_read()
                button = event.source.offset()
                if(button == 12):
                    if(not playing):
                        client.clear()
                        print("Current Queue")
                        with open('/app/server/serving_static/queue.json') as f:
                            data = json.load(f)
                        for song in data:
                            print(song)
                            client.add(song)
                        print("PLAYING")
                        client.play()
                        print("Now playing: " + str(client.currentsong()))
                        light()
                        playing = True
                    else:
                        client.stop()
                        dark()
                        playing = False
                if(button == 13):
                    client.next()
                    print("Now playing: " + str(client.currentsong()))
                    client.play()
                if(button == 14):
                    client.setvol(max(0, int(client.status()['volume']) - 10)) 
                    print("The volume has been changed to " + client.status()['volume'])
                if(button == 15):
                    client.setvol(min(100, int(client.status()['volume']) + 10)) 
                    print("The volume has been changed to " + client.status()['volume'])