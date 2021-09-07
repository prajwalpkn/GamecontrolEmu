from pynput.mouse import Button, Controller
from pynput import keyboard


mouse = Controller()


class Keys:
    def __init__(self, name):
        self.name = name
        self.pressed = False
        self.prev = False


def mousetap(x, y):
    mouse.position = (x, y)
    mouse.click(Button.left, 1)


def mousehold(x, y):
    mouse.position = (x, y)
    mouse.press(Button.left)


class KeyboardManager:
    up = Keys('w')
    down = Keys('s')
    right = Keys('d')
    left = Keys('a')
    char1 = Keys('1')
    char2 = Keys('2')
    char3 = Keys('3')
    jump = Keys('space')
    sprint = Keys('shift')
    elemental = Keys('e')
    burst = Keys('q')
    pickup = Keys('f')
    attack = Keys('j')
    setting = Keys('esc')
    map = Keys('m')
    # ordered in terms of priority
    book = {'esc': setting, 'm': map, '1': char1, '2': char2, '3': char3,
            'q': burst, 'e': elemental, 'j': attack, 'f': pickup,
            'space': jump, 'shift': sprint,
            'w': up, 's': down, 'a': left, 'd': right}

    def currentstate(self, note):
        return self.book[note].pressed

    def prevstate(self, note):
        return self.book[note].prev

    def update(self, name, state):
        # key continued to be pressed C1
        # key released C2
        # key not pressed till this updateC3
        if self.currentstate(name) == state and self.currentstate(name):
            self.book[name].prev = True
            self.book[name].pressed = state
            #print(name+' continued to be pressed')
        elif self.currentstate(name) and (not state):
            self.book[name].prev = False
            self.book[name].pressed = state
            #print(name + ' released')
            self.responder()
        elif state and (not self.currentstate(name)):
            self.book[name].prev = False
            self.book[name].pressed = state
            #print(name + ' pressed')
            self.responder()
        else:
            print('bug')

    def playermovement(self):
        if self.currentstate('w') and self.currentstate('d'):
            mousehold(430, 577)
        elif self.currentstate('w') and self.currentstate('a'):
            mousehold(165, 577)
        elif self.currentstate('w') and (not self.currentstate('a')) and (not self.currentstate('d')) and (not self.currentstate('s')):
            mousehold(312, 577)
        elif self.currentstate('s') and self.currentstate('d'):
                mousehold(430, 850)
        elif self.currentstate('s') and self.currentstate('a'):
                mousehold(185, 800)
        elif self.currentstate('s') and (not self.currentstate('a')) and (not self.currentstate('d')) and (not self.currentstate('w')):
                mousehold(312, 850)
        elif self.currentstate('a') and (not self.currentstate('s')) and (not self.currentstate('d')) and (not self.currentstate('w')):
            mousehold(165, 750)
        elif self.currentstate('d') and (not self.currentstate('s')) and (not self.currentstate('a')) and (not self.currentstate('w')):
            mousehold(430, 750)
        else:
            mouse.release(Button.left)
    def responder(self):
        mouse.release(Button.left)
        for check in self.book:
            if self.currentstate(check):
                pre = self.prevstate(check)
                if check == 'esc':
                    mousetap(162, 40)
                    print("Opened Settings")
                    break
                elif check == 'm':
                    mousetap(250, 85)
                    print("Opened Map")
                    break
                elif check == '1':
                    mousetap(1255, 373)
                    print("Changed Character1")
                    break
                elif check == '2':
                    mousetap(1255, 442)
                    print("Changed Character2")
                    break
                elif check == '3':
                    mousetap(1255, 510)
                    print("Changed Character3")
                    break
                elif check == 'f':
                    mousehold(940, 450)
                    print("Pickup")
                    break
                elif check == 'q':
                    mousehold(893, 830)
                    print("Burst")
                    break
                elif check == 'j':
                    mousehold(1100, 735)
                    print("Normal Attack")
                    break
                elif check == 'e' :
                    mousehold(985, 800)
                    print("Elemental Attack")
                    break
                elif check == 'space':
                    mousehold(1235, 675)
                    print("Jump")
                    break
                elif check == 'shift':
                    mousetap(1255, 800)
                    print("Sprint")
                    break
                elif check == 'w' or check == 's' or check == 'a' or check == 'd':
                    self.playermovement()
                    break
                else:
                    break

            else:
                continue


class Listener:

    def __init__(self, manage):
        self.manager = manage
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        try:
            manager.update(key.char, True)
        except AttributeError:
            try:
                if key == keyboard.Key.space:
                    manager.update('space', True)
                elif key == keyboard.Key.shift:
                    manager.update('shift', True)
                elif key == keyboard.Key.esc:
                    manager.update('esc', True)
                else:
                    print("key not defined")
            except:
                print("Error")
        except :
            print("No such key")

    def on_release(self, key):
        try:
            manager.update(key.char, False)
        except AttributeError:
            try:
                if key == keyboard.Key.space:
                    manager.update('space', False)
                elif key == keyboard.Key.shift:
                    manager.update('shift', False)
                elif key == keyboard.Key.esc:
                    manager.update('esc', False)
                else:
                    print("key not defined")
            except:
                print("Error")
        except :
            print("No such key")
        if key == keyboard.Key.alt:
            # Stop listener
            return False


manager = KeyboardManager()
listen = Listener(manager)

