from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapView, MapSource  # Make sure mapview is installed

# Optional: Custom tile server or use default
map_source = MapSource(url="http://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
                       cache_key="osm",
                       tile_size=256,
                       image_ext="png")

class Dashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        Clock.schedule_once(self.load_map, 0.3)

    def load_map(self, *args):
        if not self.ids.map_container.children:
            mapview = MapView(lat=14.5995, lon=120.9842, zoom=15,
                              map_source=map_source,
                              size_hint=(1, 1))
            self.ids.map_container.add_widget(mapview)

