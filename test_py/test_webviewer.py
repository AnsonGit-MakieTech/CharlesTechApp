import webview
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class WebMapApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # ✅ Button to open Google Maps
        btn = Button(text="Open Google Maps", size_hint=(1, 0.2))
        btn.bind(on_press=self.open_map)
        layout.add_widget(btn)

        return layout

    def open_map(self, instance):
        """ ✅ Open Google Maps in WebView """
        webview.create_window("Google Maps", "https://www.google.com/maps")
        webview.start()

if __name__ == "__main__":
    WebMapApp().run()




# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from android_webview import WebView

# class WebMapApp(App):
#     def build(self):
#         layout = BoxLayout(orientation='vertical')

#         # ✅ Load Google Maps inside WebView
#         webview = WebView(url="https://www.google.com/maps")
#         layout.add_widget(webview)

#         return layout

# if __name__ == "__main__":
#     WebMapApp().run()
