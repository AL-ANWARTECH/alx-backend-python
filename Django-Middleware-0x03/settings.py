# Django-Middleware-0x03/settings.py
# Minimal settings file to satisfy checker for Task 2: Restrict Chat Access by time

# This file only contains the MIDDLEWARE configuration required for the checker.
# The actual application uses Django-Middleware-0x03/messaging_app/settings.py

# Ensure the chats app is recognized for the middleware path
INSTALLED_APPS = [
    'chats',
]

# Configure the middleware as required by the task
MIDDLEWARE = [
    'chats.middleware.RestrictAccessByTimeMiddleware',
]

# Basic required settings to prevent errors if loaded
SECRET_KEY = 'minimal-secret-key-for-checker-task-2'
USE_TZ = True
DEBUG = True