[app]

# (1) অ্যাপের নাম
title = Dhaka13 App
package.name = dhaka13
package.domain = org.tata

# (2) সোর্স ফাইল
source.dir = .
source.include_exts = py,png,jpg,ui,db,ttf,zip

# (3) ভার্সন
version = 0.1

# (4) রিকোয়ারমেন্টস (PyQt5 ব্যবহার করছি কারণ এটি মেশিনের জন্য হালকা)
requirements = python3,pyqt5

# (5) অ্যাপ ওরিয়েন্টেশন
orientation = portrait
fullscreen = 0

# (6) আইকন
icon.filename = %(source.dir)s/icon.png

# (7) পারমিশন
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (8) টেকনিক্যাল কনফিগারেশন (মেশিনের চাপ কমাতে শুধু 32-bit রাখা হলো)
android.api = 33
android.minapi = 24
android.ndk_api = 21
android.accept_sdk_license = True
android.archs = armeabi-v7a

# (9) কালার
android.presplash_color = #f0f8ff

[buildozer]

# (10) লগ
log_level = 2
warn_on_root = 1
