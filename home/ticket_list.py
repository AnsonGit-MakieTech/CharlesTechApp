from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.metrics import dp

class TicketListScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_pre_enter(self, *args):
        self.height = self.parent.height - dp(60)
        return super().on_pre_enter(*args)



