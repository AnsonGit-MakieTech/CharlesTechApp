from kivy.app import App
from kivy_garden.mapview import MapView
from kivy_garden.mapview.mbtsource import MBTilesMapSource

import os

class OfflineMapApp(App):
    def build(self):
        # Load an offline MBTiles file
        file_path = os.path.join(os.path.dirname(__file__), "maps", "philippines.mbtiles")
        offline_source = MBTilesMapSource(file_path)


        # Create MapView with the offline source
        map_view = MapView(
            lat=12.8797, lon=121.7740,  # 📌 Center on the Philippines
            zoom=6,
            map_source=offline_source  # 🔥 Set to offline source
        )

        return map_view

if __name__ == "__main__":
    OfflineMapApp().run()
