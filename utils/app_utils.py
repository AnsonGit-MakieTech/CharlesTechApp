 
from kivy.core.window import Window 
from kivy.utils import platform 

if platform == 'android':
    from jnius import autoclass, cast

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
 