from Leetboard import Keyboard
import time

kbrd = Keyboard(Keyboard.leetspeak)

print('Leetboard Starting, press Shift+Space to trigger...')
kbrd.start(threaded=True)
print('Keyboard will run for 30 seconds')
time.sleep(30)
print('Stopped')