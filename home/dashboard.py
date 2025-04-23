from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapView, MapSource, MapMarker, MapLayer
from kivy.animation import Animation
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Line, Color
from kivy.uix.boxlayout import BoxLayout
from utils.app_utils import has_internet
from kivy.metrics import dp
import os
import random
from kivy import platform
from plyer import gps

from kivymd.app import MDApp


# Optional: Custom tile server or use default
# map_source = MapSource(url="http://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
#                        cache_key="osm",
#                        tile_size=256,
#                        image_ext="png")
map_source = MapSource(
    url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    cache_key="satellite",
    tile_size=256,
    image_ext="jpg",  # Esri tiles are usually JPG
    attribution="Tiles © Esri — Source: Esri, Earthstar Geographics"
)
 
from kivy_garden.mapview import MapLayer
from kivy.graphics import Line, Color

class RouteLineLayer(MapLayer):
    def __init__(self, route_coords, **kwargs):
        super().__init__(**kwargs)
        self.route_coords = route_coords

    def reposition(self, *args):
        self.canvas.clear()

        mapview = self.get_map_view()
        if not self.route_coords or not mapview:
            return

        with self.canvas:
            Color(0, 0.4, 1, 1)  # Optional: change line color
            points = []

            for lon, lat in self.route_coords:
                x, y = mapview.get_window_xy_from(lat, lon, mapview.zoom)
                points.extend((x, y))

            if points:
                Line(points=points, width=2)

    def get_map_view(self):
        parent = self.parent
        while parent:
            if isinstance(parent, MapView):
                return parent
            parent = parent.parent
        return None


class Dashboard(Screen):
    map_container : BoxLayout = ObjectProperty(None)
    mapview : MapView = ObjectProperty(None)
    main_parent : BoxLayout = ObjectProperty(None)
    truck_marker : MapMarker = ObjectProperty(None)
    truck_image_path : str = StringProperty('')
    location_image_path : str = StringProperty('')

    dashboard_server_data : dict = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.truck_image_path = os.path.join(parent_dir, 'assets', 'truck.png')
        self.location_image_path = os.path.join(parent_dir, 'assets', 'location.png')
        print(parent_dir)
    
    def on_leave(self, *args):
        Animation(opacity=0, duration=0.5).start(self)
        return super().on_leave(*args)
    
    def on_parent(self, *args):
        if self.parent:
            # self.main_parent.height = self.parent.height - dp(65)
            Clock.schedule_once(self.load_map, 1)

    def on_enter(self, *args):
        Animation(opacity=1, duration=0.5).start(self)  
        app = MDApp.get_running_app()  
        key = "GET_USER_TECH_INFO"
        print(f'keys : {app.communications.key_running}')
        if key not in app.communications.key_running:
            app.communications.get_user_tech_info()
            def communication_event(*args):
                data = app.communications.data.get(key, None)
                if data: 
                    if data.get("result", False):
                        self.dashboard_server_data = data.get("data", {})
                        print(self.dashboard_server_data)
                return False
            
            Clock.schedule_interval(communication_event, 1)


        Clock.schedule_once(self.load_map, 1) 
        return super().on_enter(*args)

    def load_map(self, *args):

        if not self.map_container.children:

            if not has_internet():
                return
            
            self.mapview = MapView(
                lat=12.375466976,
                lon=123.63299577,
                zoom=16,
                map_source=map_source,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.mapview.min_zoom = 1
            self.mapview.max_zoom = 17


            self.truck_marker = MapMarker(
                lat=12.376211,
                lon=123.63004,
                source=self.truck_image_path
            )

            self.truck_marker.size = (dp(30), dp(30))

            self.mapview.add_marker(self.truck_marker)
            # for i in range(10):
            #     location_marker = MapMarker(
            #         lat=12.375466976 + random.uniform(-0.01, 0.01),
            #         lon=123.63299577 + random.uniform(-0.01, 0.01),
            #         source=self.location_image_path
            #     )
            #     location_marker.size = (dp(30), dp(30))
            #     self.mapview.add_marker(location_marker)
            
            
            # Sample route from OSRM
            route_coords = [[123.63004, 12.376211], [123.630617, 12.375892], [123.630764, 12.37581], [123.631128, 12.37572], [123.631574, 12.375635], [123.632742, 12.37544], [123.633135, 12.375432], [123.633532, 12.375436]]

            # Create and add the route line layer
            self.route_layer = RouteLineLayer(route_coords)
            self.mapview.add_layer(self.route_layer)

            # Ensure line is redrawn when user pans or zooms
            self.mapview.bind(on_map_relocated=self.route_layer.reposition)
            self.mapview.bind(zoom=self.route_layer.reposition)


            
            self.map_container.add_widget(self.mapview)

            

            if platform == 'android':
                try:
                    gps.configure(on_location=self.update_location, on_status=self.on_gps_status)
                    gps.start(minTime=1000, minDistance=1)
                except NotImplementedError:
                    print("GPS is not implemented on this platform.")
                    

        if self.truck_marker:
            self.mapview.center_on(self.truck_marker.lat, self.truck_marker.lon)

    def update_location(self, **kwargs):
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        if lat and lon:
            self.truck_marker.lat = float(lat)
            self.truck_marker.lon = float(lon)
            # self.mapview.center_on(float(lat), float(lon))
            print(f"📍 GPS Location updated → Lat: {lat}, Lon: {lon}")

    def on_gps_status(self, stype, status):
        print(f"📡 GPS Status update: {stype} → {status}")