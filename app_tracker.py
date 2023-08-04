import time
import pygetwindow as gw

def get_active_app_title():
    try:
        active_app = gw.getActiveWindow()
        return active_app.title if active_app else None
    except gw.PyGetWindowException:
        return None

def main():
    print("Tracking active application... (Press Ctrl+C to stop)")
    try:
        while True:
            active_app_title = get_active_app_title()
            if active_app_title:
                print(f"Active Application: {active_app_title}")
            else:
                print("No active application.")
            time.sleep(5)  # Adjust the interval (in seconds) as needed
    except KeyboardInterrupt:
        print("Tracking stopped.")

if __name__ == "__main__":
    main()
