
from inspect import signature
from pynput import keyboard
import pyperclip
import threading
import time

# TODO: add setup.py with sudo apt-get install xclip
# The key combination to check
HOTKEY = {keyboard.Key.shift, keyboard.Key.space}

class Keyboard:
    def __init__(self, method:lambda x: x):
        self.hotkey = HOTKEY
        self.controller = keyboard.Controller()
        self._typing = False

        if len(signature(method).parameters) != 1:
            raise ValueError('Method must have exactly 1 parameter!') 
        if method('') == None:
            raise ValueError('Method returns None')

        self.method = lambda x: str(method(x))
    
    def trigger(self):        
        self._typing = True
        pre_clipboard = pyperclip.paste()
        
        for key in self.hotkey: self.controller.release(key)

        # press ctrl-a and ctrl-c to get the current text field
        self.controller.press(keyboard.Key.ctrl)
        self.controller.press('a')
        self.controller.release('a')
        self.controller.press('c')
        self.controller.release('c')
        self.controller.release(keyboard.Key.ctrl)
        time.sleep(0.02)

        # deselect the selected text
        self.controller.press(keyboard.Key.left)
        self.controller.release(keyboard.Key.left)
        
        # get the copied text and process it
        # could take time, so hold up on ctrl-a
        text = self.method(pyperclip.paste()) 
        
        # select all and replace it with the output
        self.controller.press(keyboard.Key.ctrl)
        self.controller.press('a')
        self.controller.release('a')
        self.controller.release(keyboard.Key.ctrl)
        time.sleep(0.02)
        self.controller.type(text)

        # reset the clipboard to its previous state
        pyperclip.copy(pre_clipboard)

    def start(self, threaded:bool = False):
        held = set()

        def on_press(key):
            if self._stop_listener: listener.stop()
            elif key in HOTKEY:
                held.add(key)
                if all(k in held for k in self.hotkey):
                    if not self._typing: self.trigger()
            elif self._typing: self._typing = False

        def on_release(key):
            try: held.remove(key)
            except KeyError: pass
        
        self._stop_listener = False

        if threaded:
            threading.Thread(target=lambda: self.start(threaded=False), daemon=True).start()
        else:
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                try: listener.join()
                except (KeyboardInterrupt, OSError, SystemError): self.stop()
            
    
    def stop(self):
        self._stop_listener = True

    @staticmethod
    def leetspeak(string):
        #l33t substitutions
        subs = {'to':'2','be':'B','cks':'x','e':'3','I':'1','a':'@'}
        for k,v in subs.items():
            string = string.replace(k, v)

        # remove spaces from words
        output = ""
        for word in string: 
            if len(word) >= 5: output += ' '
            output += word
        
        return output.strip()

if __name__ == '__main__':
    kbrd = Keyboard(Keyboard.leetspeak)
    kbrd.start_listener()