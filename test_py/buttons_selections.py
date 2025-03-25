
from kivy.utils import hex_colormap

from materialyoucolor.utils.platform_utils import SCHEMES
from kivymd.uix.menu import MDDropdownMenu

KV = """
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDBoxLayout:
        id: root_box
        orientation: "vertical"
        spacing: "12dp"
        padding: "12dp"

        MDIconButton:
            on_release: app.open_menu(self)
            icon: "menu"
    
        ScrollView:
    
            MDBoxLayout:
                orientation: "vertical"
                padding: "32dp", 0, "32dp", "32dp"
                spacing: "24dp"
                adaptive_height: True
        
                MDLabel:
                    adaptive_height: True
                    text: "Standard widget"
        
                MDBoxLayout:
                    id: widget_box
                    adaptive_height: True
                    spacing: "24dp"
        
                Widget:
                    size_hint_y: None
                    height: "12dp"
        
                MDLabel:
                    adaptive_height: True
                    text: "Custom widget"

                MDBoxLayout:
                    id: custom_widget_box
                    adaptive_height: True
                    spacing: "24dp"
"""


class CommonApp:
    menu: MDDropdownMenu = None

    def open_menu(self, menu_button):
        menu_items = []
        for item, method in {
            "Set palette": lambda: self.set_palette(),
            "Switch theme style": lambda: self.switch_theme(),
            "Switch scheme type": lambda: self.set_scheme_type(),
            "Disabled widgets": lambda: self.disabled_widgets(),
        }.items():
            menu_items.append(
                {
                    "text": item,
                    "on_release": method,
                }
            )
        self.menu = MDDropdownMenu(
            caller=menu_button,
            items=menu_items,
        )
        self.menu.open()

    def switch_palette(self, selected_palette):
        self.theme_cls.primary_palette = selected_palette
    
    def switch_theme(self):
        self.theme_cls.switch_theme()

    def set_palette(self):
        instance_from_menu = self.get_instance_from_menu("Set palette")
        available_palettes = [
            name_color.capitalize() for name_color in hex_colormap.keys()
        ]

        menu_items = []
        for name_palette in available_palettes:
            menu_items.append(
                {
                    "text": name_palette,
                    "on_release": lambda x=name_palette: self.switch_palette(x),
                }
            )
        MDDropdownMenu(
            caller=instance_from_menu,
            items=menu_items,
        ).open()

    def set_scheme_type(self):
        instance_from_menu = self.get_instance_from_menu("Switch scheme type")

        menu_items = []
        for scheme_name in SCHEMES.keys():
            menu_items.append(
                {
                    "text": scheme_name,
                    "on_release": lambda x=scheme_name: self.update_scheme_name(x),
                }
            )
        MDDropdownMenu(
            caller=instance_from_menu,
            items=menu_items,
        ).open()
    
    def update_scheme_name(self, scheme_name):
        self.theme_cls.dynamic_scheme_name = scheme_name

    def get_instance_from_menu(self, name_item):
        index = 0
        rv = self.menu.ids.md_menu
        opts = rv.layout_manager.view_opts
        datas = rv.data[0]

        for data in rv.data:
            if data["text"] == name_item:
                index = rv.data.index(data)
                break

        instance = rv.view_adapter.get_view(
            index, datas, opts[index]["viewclass"]
        )
        return instance

    def disabled_widgets(self):
        for widget in self.root.ids.widget_box.children:
            widget.disabled = not widget.disabled

        for widget in self.root.ids.custom_widget_box.children:
            widget.disabled = not widget.disabled













from kivy.clock import Clock
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.button import (
    MDIconButton,
    MDButton,
    MDFabButton,
    MDButtonText,
    MDButtonIcon,
    MDExtendedFabButton,
    MDExtendedFabButtonIcon,
    MDExtendedFabButtonText,
)

# https://github.com/kivymd/KivyMD/blob/master/examples/common_app.py 

KV = """
MDScreen:
    md_bg_color: app.theme_cls.backgroundColor

    MDIconButton:
        on_release: app.open_menu(self)
        pos_hint: {"top": .98}
        x: "12dp"
        icon: "menu"

    ScrollView:
        size_hint_y: None
        height: root.height - dp(68)

        MDBoxLayout:
            orientation: "vertical"
            padding: "24dp", 0, "24dp", 0
            adaptive_height: True

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "24dp"
                padding: "24dp"

                MDLabel:
                    text: "MDIconButton"
                    bold: True
                    adaptive_height: True

                MDBoxLayout:
                    id: icon_button_box
                    adaptive_height: True
                    spacing: "12dp"

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "24dp"
                padding: "24dp"
                md_bg_color: app.theme_cls.secondaryContainerColor
                radius: "12dp"

                MDLabel:
                    text: "MDIconButton (custom color)"
                    bold: True
                    adaptive_height: True

                MDBoxLayout:
                    id: custom_icon_button_box
                    adaptive_height: True
                    spacing: "12dp"

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "24dp"
                padding: "24dp"

                MDLabel:
                    text: "MDFabButton"
                    bold: True
                    adaptive_height: True

                MDBoxLayout:
                    id: fab_button_box
                    adaptive_height: True
                    spacing: "12dp"

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "24dp"
                padding: "24dp"
                md_bg_color: app.theme_cls.secondaryContainerColor
                radius: "12dp"

                MDLabel:
                    text: "MDFabButton (custom color)"
                    bold: True
                    adaptive_height: True

                MDBoxLayout:
                    id: custom_fab_button_box
                    adaptive_height: True
                    spacing: "12dp"

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "24dp"
                padding: "24dp"

                MDLabel:
                    text: "MDButton"
                    adaptive_height: True
                    bold: True

                MDBoxLayout:
                    id: md_button_box
                    adaptive_height: True
                    spacing: "12dp"

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "24dp"
                padding: "24dp", 0, "24dp", "24dp"

                MDLabel:
                    text: "MDButton (with icon)"
                    adaptive_height: True
                    bold: True

                MDBoxLayout:
                    id: md_button_icon_box
                    adaptive_height: True
                    spacing: "12dp"

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "24dp"
                padding: "24dp"
                md_bg_color: app.theme_cls.secondaryContainerColor
                radius: "12dp"

                MDLabel:
                    text: "MDButton (custom color)"
                    bold: True
                    adaptive_height: True

                MDBoxLayout:
                    id: custom_md_button_box
                    adaptive_height: True
                    spacing: "12dp"

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "24dp"
                padding: "24dp"
                radius: "12dp"

                MDLabel:
                    text: "MDExtendedFabButton"
                    bold: True
                    adaptive_height: True

                MDBoxLayout:
                    id: extended_fab_button_box
                    adaptive_height: True
                    spacing: "12dp"

                    Widget:
"""


class Example(MDApp, CommonApp):
    def build(self):
        self.theme_cls.dynamic_color = True
        return Builder.load_string(KV)

    def disabled_widgets(self):
        for button in (
            self.root.ids.fab_button_box.children
            + self.root.ids.custom_fab_button_box.children
            + self.root.ids.custom_icon_button_box.children
            + self.root.ids.md_button_box.children
            + self.root.ids.icon_button_box.children
            + self.root.ids.md_button_icon_box.children
            + self.root.ids.custom_md_button_box.children
            + self.root.ids.extended_fab_button_box.children
        ):
            button.disabled = not button.disabled

    def on_start(self):
        styles = ["standard", "filled", "outlined", "tonal"]
        color_disabled = [
            0.4627450980392157,
            0.47058823529411764,
            0.07450980392156863,
            0.38,
        ]

        for style in styles:
            self.root.ids.icon_button_box.add_widget(
                MDIconButton(style=style, icon="heart")
            )
            if style in ["filled", "tonal"]:
                self.root.ids.custom_icon_button_box.add_widget(
                    MDIconButton(
                        style=style,
                        icon="heart",
                        theme_bg_color="Custom",
                        theme_icon_color="Custom",
                        md_bg_color={"filled": "brown", "tonal": "green"}[
                            style
                        ],
                        icon_color={"filled": "green", "tonal": "brown"}[style],
                        icon_color_disabled="black",
                        md_bg_color_disabled=color_disabled,
                    )
                )
            elif style == "outlined":
                self.root.ids.custom_icon_button_box.add_widget(
                    MDIconButton(
                        style=style,
                        icon="heart",
                        theme_icon_color="Custom",
                        theme_line_color="Custom",
                        line_color="brown",
                        icon_color="green",
                        icon_color_disabled="black",
                        md_bg_color_disabled=color_disabled,
                    )
                )
            elif style == "standard":
                self.root.ids.custom_icon_button_box.add_widget(
                    MDIconButton(
                        style=style,
                        icon="heart",
                        theme_icon_color="Custom",
                        icon_color="green",
                        icon_color_disabled="black",
                        md_bg_color_disabled=color_disabled,
                    )
                )

        styles = ["filled", "outlined", "tonal", "elevated", "text"]
        for style in styles:
            text = style.capitalize()
            self.root.ids.md_button_box.add_widget(
                MDButton(
                    MDButtonText(
                        text=text,
                    ),
                    style=style,
                )
            )
            self.root.ids.md_button_icon_box.add_widget(
                MDButton(
                    MDButtonIcon(
                        icon="heart",
                    ),
                    MDButtonText(
                        text=text,
                    ),
                    style=style,
                )
            )
            self.root.ids.custom_md_button_box.add_widget(
                MDButton(
                    MDButtonIcon(
                        icon="heart",
                        theme_icon_color="Custom",
                        icon_color="yellow",
                        icon_color_disabled="black",
                    ),
                    MDButtonText(
                        text=text,
                        theme_text_color="Custom",
                        text_color={
                            "filled": "white",
                            "tonal": "white",
                            "outlined": "green",
                            "text": "green",
                            "elevated": "white",
                        }[style],
                    ),
                    style=style,
                    theme_bg_color="Custom",
                    theme_line_color="Custom"
                    if style == "outlined"
                    else "Primary",
                    md_bg_color={
                        "filled": "brown",
                        "tonal": "brown",
                        "outlined": self.theme_cls.transparentColor,
                        "text": self.theme_cls.transparentColor,
                        "elevated": "red",
                    }[style],
                    line_color="green",
                    md_bg_color_disabled=color_disabled,
                )
            )

        styles = {
            "standard": "surface",
            "small": "secondary",
            "large": "tertiary",
        }
        for style in styles.keys():
            self.root.ids.fab_button_box.add_widget(
                MDFabButton(
                    style=style, icon="pencil-outline", color_map=styles[style]
                )
            )
            self.root.ids.custom_fab_button_box.add_widget(
                MDFabButton(
                    style=style,
                    icon="heart",
                    theme_bg_color="Custom",
                    md_bg_color="brown",
                    theme_icon_color="Custom",
                    icon_color="yellow",
                    icon_color_disabled="lightgrey",
                    md_bg_color_disabled=color_disabled,
                )
            )
        button = MDExtendedFabButton(
            MDExtendedFabButtonIcon(
                icon="pencil-outline",
            ),
            MDExtendedFabButtonText(
                text="Compose",
            ),
            fab_state="expand",
        )
        button.bind(on_release=self.fab_button_expand)
        self.root.ids.extended_fab_button_box.add_widget(
            MDExtendedFabButton(
                MDExtendedFabButtonText(
                    text="Compose",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                fab_state="expand",
            )
        )
        self.root.ids.extended_fab_button_box.add_widget(button)

    def fab_button_expand(self, instance):
        def fab_button_expand(*args):
            instance.fab_state = (
                "expand" if instance.fab_state == "collapse" else "collapse"
            )

        Clock.schedule_once(fab_button_expand, 0.3)


Example().run()
