from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window

kv_code = '''
#:import utils kivy.utils

<DelayedWidget@BoxLayout>:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    canvas.before:
        Color:
            rgba: utils.get_color_from_hex('#f0f0f0')
        Rectangle:
            pos: self.pos
            size: self.size
    
    Label:
        text: "I'm loaded later!"
        font_size: '24sp'
        color: utils.get_color_from_hex('#333333')
        bold: True
        size_hint_y: None
        height: '50dp'
    
    BoxLayout:
        orientation: 'horizontal'
        spacing: 10
        size_hint_y: None
        height: '40dp'
        
        Button:
            text: 'Click Me!'
            background_color: utils.get_color_from_hex('#4CAF50')
            color: 1, 1, 1, 1
            size_hint_x: 0.5
            font_size: '16sp'
            
        Button:
            text: 'Settings'
            background_color: utils.get_color_from_hex('#2196F3')
            color: 1, 1, 1, 1
            size_hint_x: 0.5
            font_size: '16sp'
'''

class MyApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background
        root = BoxLayout()
        Clock.schedule_once(lambda dt: self.load_ui(root), 2)  # Delay 2 seconds
        return root

    def load_ui(self, root):
        Builder.load_string(kv_code)
        from kivy.factory import Factory
        root.add_widget(Factory.DelayedWidget())

MyApp().run()
