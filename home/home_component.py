
from kivy.uix.scrollview import ScrollView 
from kivy.effects.dampedscroll import DampedScrollEffect
from time import time 

from kivy.properties import ObjectProperty, NumericProperty, StringProperty

class CallControl:
    def __init__(self, interval=1):
        self.interval = interval
        self.last_call = 0

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            now = time()
            if now - self.last_call > self.interval:
                self.last_call = now
                func(*args, **kwargs)
        return wrapper


class CustomScrollEffect(DampedScrollEffect):
    
    parent_event : callable = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlled_callback = self.do_refresh_controlled

    def on_overscroll(self, *args):
        super().on_overscroll(*args)
        if self.overscroll < -50:  # Pulling down
            self.controlled_callback()

    @CallControl(interval=1)
    def do_refresh_controlled(self):
        print("🔄 Pull-to-refresh triggered!")
        if self.parent_event:
            self.parent_event()


class CustomScrollView(ScrollView):
    
    refresh_callback : object = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        kwargs['effect_cls'] = CustomScrollEffect
        super().__init__(**kwargs)
    
    def setup_effect_callback(self, refresh_callback : object):
        self.effect_cls.parent_event = refresh_callback
        