from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

kv_code = '''
<DelayedWidget@BoxLayout>:
    orientation: 'vertical'
    Label:
        text: "I'm loaded later!"
'''

class MyApp(App):
    def build(self):
        root = BoxLayout()
        Clock.schedule_once(lambda dt: self.load_ui(root), 2)  # Delay 2 seconds
        return root

    def load_ui(self, root):
        Builder.load_string(kv_code)
        from kivy.factory import Factory
        root.add_widget(Factory.DelayedWidget())

MyApp().run()
