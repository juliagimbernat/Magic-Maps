import evdev
from evdev import ecodes

X, Y = 0, 0

device = evdev.InputDevice('/dev/input/event4')
print(device)

for event in device.read_loop():
    if event.code == ecodes.ABS_MT_POSITION_X:
        X = event.value
        print('X = ', X)
    if event.code == ecodes.ABS_MT_POSITION_Y:
        Y = event.value
        print('Y= ', Y)
