from kivy.uix.accordion import ObjectProperty, BooleanProperty

from kivy.uix.scrollview import ScrollView 
from kivy.effects.dampedscroll import DampedScrollEffect
from time import time 
from kivy.uix.modalview import ModalView

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock

import os

from kivy.properties import ObjectProperty, NumericProperty, StringProperty

from kivy.graphics import PushMatrix, PopMatrix, Rotate, Translate


class CallControl:
    def __init__(self, interval=3):
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

    @CallControl(interval=3)
    def do_refresh_controlled(self):
        print("🔄 Pull-to-refresh triggered!")
        if self.parent_event:
            self.parent_event()


class CustomScrollView(ScrollView):
    
    refresh_callback : object = ObjectProperty(None)
    
    # def __init__(self, **kwargs):
    #     kwargs['effect_cls'] = CustomScrollEffect
    #     super().__init__(**kwargs)
    
    def setup_effect_callback(self, refresh_callback: object): 
        self.effect_cls = CustomScrollEffect
        self.effect_cls.parent_event = refresh_callback
        print("Setup : ", refresh_callback)
        
 

class CustomSpinner(Image):
    # process_image: str = StringProperty('')
    angle: float = NumericProperty(0)  # ✅ Required for animation
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.anim = None

        # parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        # self.process_image = os.path.join(parent_dir, 'assets', 'loading_image.png')

        # Use canvas instructions to apply rotation
        self.bind(pos=self.update_canvas, size=self.update_canvas, angle=self.update_canvas)

    def start_spinner(self, *args):
        # self.source = self.process_image
        self.size_hint_x = 0.5
        self.size_hint_y = 0.5
        self.anim = Animation(angle=360, duration=1)
        self.anim += Animation(angle=0, duration=0)
        self.anim.repeat = True
        self.anim.start(self)
        

    def stop_success_spinner(self, *args):
        if self.anim:
            self.anim.cancel(self)

            # Animate shrink first
            anim = Animation(size_hint_x=0.0, size_hint_y=0.0, duration=0.5)
            anim.bind(on_complete=self.display_done)
            anim.start(self)
            

    def display_done(self, *args):
        # Update the image to success icon
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.source = os.path.join(parent_dir, 'assets', 'checked_success.png')
        self.angle = 0 
        # Animate grow and fade out sequentially
        anim = (
            Animation(size_hint_x=0.5, size_hint_y=0.5, duration=0.5, t='out_back') 
        )
        anim.start(self)
    
    def stop_error_spinner(self, *args):
        if self.anim:
            self.anim.cancel(self)
            # Animate shrink first
            anim = Animation(size_hint_x=0.0, size_hint_y=0.0, duration=0.5)
            anim.bind(on_complete=self.display_error)
            anim.start(self)
            
    def display_error(self, *args):
        # Update the image to error icon
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.source = os.path.join(parent_dir, 'assets', 'warning_error.png')
        self.angle = 0
        # Animate grow and fade out sequentially
        anim = (
            Animation(size_hint_x=0.5, size_hint_y=0.5, duration=0.5  ) 
        )
        anim.start(self)

    def update_canvas(self, *args):
        
        self.canvas.before.clear()
        with self.canvas.before:
            PushMatrix()
            Translate(self.center_x, self.center_y)
            Rotate(angle=self.angle, origin=(0, 0))
            Translate(-self.center_x, -self.center_y)
        self.canvas.after.clear()
        with self.canvas.after:
            PopMatrix()


class ProcessingLayout(ModalView):
    
    spinner : CustomSpinner = ObjectProperty(None)
    proccess_text : str = StringProperty('')
    is_open : bool = BooleanProperty(False)
    
    def on_pre_open(self):
        self.auto_dismiss = False
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.spinner.source = os.path.join(parent_dir, 'assets', 'loading_image.png')
        return super().on_pre_open()
    def on_open(self):
        self.auto_dismiss = False
        self.spinner.start_spinner()
        self.proccess_text = "Please wait while we complete the process. Do not close the application until it is finished."
        self.is_open = True
        
        # Clock.schedule_once(self.display_success , 2)
        
        return super().on_open()

    def display_success(self, message = None):
        self.spinner.stop_success_spinner()
        self.proccess_text = "Process completed successfully!" if not message else message
        Clock.schedule_once(self.dismiss, 2) 
        self.is_open = False
    
    def display_error(self, message = None):
        self.spinner.stop_error_spinner()
        self.proccess_text = "An error occurred while processing the data." if not message else message
        self.auto_dismiss = True
        self.is_open = False
    

        
        