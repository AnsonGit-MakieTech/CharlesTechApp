[app]

# (str) Title of your application
title = TechApp

# (str) Package name
package.name = techapp
python_version = 3.10
# (str) Package domain (needed for android/ios packaging)
package.domain = org.billingko
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf,txt,otf
version = 0.1
requirements = cython==0.29.36,python3==3.10,kivy==2.3.1,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,https://github.com/HyTurtle/plyer/archive/master.zip,requests,pillow,kivy_garden.mapview,androidstorage4kivy,filetype,openssl,asynckivy,asyncgui

orientation = portrait
icon.filename = assets/app_logo.png
presplash.filename = assets/splash_app.png
android.presplash_color = #ABCFE3

android.api = 34
android.minapi = 29
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# Permissions you might need based on your dependencies (Mapview, Storage, Webview, etc.) 
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO

# Garden requirements explicitly included
garden_requirements = mapview
android.gradle_dependencies = com.google.android.gms:play-services-location:21.0.1

# P4A settings
p4a.branch = master

log_level = 2
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 0