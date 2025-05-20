from kivy.uix.accordion import StringProperty
from kivy.uix.accordion import ObjectProperty
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.properties import ListProperty, BooleanProperty, NumericProperty  
from kivy.utils import get_color_from_hex as chex
from kivy.clock import Clock
from kivy.metrics import dp
class PinButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = self.width * 0.4  # ✅ Initial font size
        self.bind(size=self.update_font_size)  # ✅ Only recalculate on resize

    def update_font_size(self, *args):
        """ Update font size only when button size changes """
        self.font_size = self.width * 0.4  # ✅ Update only when resized
        
        
class ClickableLabel(Label):
    label_event: callable = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.bind(size=self.update_font_safely) # To much iterations remove soon
        # Clock.schedule_once(self.update_font_safely, 0)
    
    # def on_parent(self, *args):
    #     self.update_font_safely()

    # def update_font_safely(self, *args):
    #     """Update font and height with debounce"""
    #     # self.font_size = self.width * 0.08
    #     Clock.schedule_once(self.set_height_from_texture, 0)

    # def set_height_from_texture(self, *args):
    #     new_height = self.texture_size[1] + dp(20)
    #     if self.height != new_height:
    #         self.height = new_height

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.label_event:
                self.label_event()
            return True
        return super().on_touch_down(touch)
    
    
     
class PinWidget(Widget):
    default_color = ListProperty([0.254, 0.788, 0.886, 1])  # ✅ "41C9E2" converted to RGBA
    active_color = ListProperty([0.005, 0.26, 0.40, 1])  # ✅ Default color (#014367)
    is_active = BooleanProperty(False)  # ✅ Toggle variable

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.color_instruction = Color(*self.default_color)  # ✅ Set initial color
            self.circle = Ellipse(size=self.size, pos=self.pos)  # ✅ Create circle

        self.bind(size=self.update_canvas, pos=self.update_canvas, is_active=self.update_color)

    def update_canvas(self, *args):
        """Keep the circle always perfectly round and centered"""
        min_size = min(self.width, self.height)  # ✅ Keep it a perfect circle
        self.circle.size = (min_size, min_size)
        self.circle.pos = (self.center_x - min_size / 2, self.center_y - min_size / 2)  # ✅ Center it

    def update_color(self, *args):
        """Toggle the color when `is_active` is changed"""
        self.color_instruction.rgba = self.active_color if self.is_active else self.default_color  # ✅ Toggle color

    def toggle(self):
        """Toggle between active and default state"""
        self.is_active = not self.is_active  # ✅ Change state


class LoginBackButton(Button):
    pass

class LoginLabelTitle(Label):
    pass

class LoginTextInput(TextInput):
    text_tab_px = NumericProperty(8)
    adjusted_vpad = NumericProperty(15)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_padding()
        self.bind(size=self.update_padding)  # ✅ Update padding when size changes

    def on_parent(self, *args):
        self.update_padding()
    
    def update_padding(self, *args):
        """ Dynamically center text vertically """ 
        width, height = self.size
        # Protect padding from going negative
        vpad = min(max(0, (height - self.line_height) / 2), self.adjusted_vpad) 
        self.padding = [self.text_tab_px, vpad, self.text_tab_px, vpad] 
        self._refresh_text(self.text)


class LoginButton(Button):
    pass


class ProcessingModal(ModalView):
    proccess_text = StringProperty(". . . PROCESSING . . .")  # ✅ Default text
    dot_count = 0  # ✅ Counter to control animation

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.animate_text, 0.5)  # ✅ Update text every 0.5s

    def animate_text(self, dt):
        """Animates the text by adding/removing dots on both sides"""
        self.dot_count = (self.dot_count + 1) % 4  # ✅ Cycle from 0 to 3
        dots = "." * self.dot_count  # ✅ Dynamic dots
        self.proccess_text = f"{dots} PROCESSING {dots}"  # ✅ Update text

class ControllableModal(ModalView):
    my_text = StringProperty("You Have Successfully\nRegister Your New Pin ")  # ✅ Default text 
