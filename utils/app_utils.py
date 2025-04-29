 
from kivy.core.window import Window 
from kivy.utils import platform 
import socket
import base64

if platform == 'android':
    from jnius import autoclass, cast
 
def get_android_id():
    SettingsSecure = autoclass("android.provider.Settings$Secure")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    context = PythonActivity.mActivity

    android_id = SettingsSecure.getString(
        context.getContentResolver(),
        SettingsSecure.ANDROID_ID
    )
    return android_id
def get_android_keyboard_height():
    """ Get keyboard height on Android using pyjnius """
    if platform == 'android':
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Activity = cast('android.app.Activity', PythonActivity.mActivity)
        Rect = autoclass('android.graphics.Rect')
        root_window = Activity.getWindow()
        view = root_window.getDecorView()
        r = Rect()
        view.getWindowVisibleDisplayFrame(r)
        return Window.height - (r.bottom - r.top)
    return 0  # Default for non-Android platforms


def is_valid_latlon(text):
    try:
        lat_str, lon_str = text.split(",")
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except (ValueError, AttributeError):
        return False
 

def has_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def image_path_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None 