[app]

# Strip debug symbols from your .so files to make them less fingerprint-y:
android.strip = True

# (str) Title of your application
title = TechApp


# (str) Package name (must remain the same for updates)
package.name = techapp 
# (str) Package domain (also must remain the same)
package.domain = org.billingko
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf,txt,otf
# --- Versioning: ---
# (str) Human-readable version name (optional, shown to users)
#      Bump this whenever you make a new release, e.g. "0.1" → "0.2" → "1.0" → etc.
version = 0.1

# (int) Android version code
#      This is what Android actually checks to see if the APK is “newer.” 
#      Must increase by at least +1 from the last build (e.g. 1, 2, 3, …).
#      If your previous APK had version_code = 1, set this to 2 for the next release.
android.version_code = 1

requirements = hostpython3,python3,kivy==2.3.1,cython==0.29.36,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,https://github.com/HyTurtle/plyer/archive/master.zip,requests,pillow,kivy_garden.mapview,androidstorage4kivy,filetype,openssl,asynckivy,asyncgui

orientation = portrait
icon.filename = assets/app_logo.png
presplash.filename = assets/splash_app.png
android.presplash_color = #ABCFE3

android.api = 34
android.minapi = 26
android.ndk = 25b
android.accept_sdk_license = True

# Bundle both 32-bit and 64-bit ARM into one “universal” APK:
android.archs = arm64-v8a, armeabi-v7a
android.multi_apk = False


# Permissions you might need based on your dependencies (Mapview, Storage, Webview, etc.) 
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Garden requirements explicitly included
garden_requirements = mapview
android.gradle_dependencies = com.google.android.gms:play-services-location:21.0.1


# — Your release keystore for in-place updates — 
android.release_keystore = releasekey.jks
android.release_keyalias = techcharlesapp
android.release_keystore_password = Charles691Tech
android.release_keyalias_password = Charles691Tech



# P4A settings
p4a.branch = master
p4a.python_version = 3.10

log_level = 2
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 0