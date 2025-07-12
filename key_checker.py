import keyboard
import sys
import time

print("Press keys to see their names. Press 'q' to quit.")

quit_flag = False

def on_key_event(event):
    global quit_flag
    if event.event_type == keyboard.KEY_DOWN:
        print(f"Key: '{event.name}'")
        if event.name == 'q':
            print("Quitting...")
            quit_flag = True

keyboard.hook(on_key_event)

try: 
    while not quit_flag:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nInterrupted by user")

keyboard.unhook_all()