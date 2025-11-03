# channellearn/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('api/notifications/', include('notifications.urls')),
]


# ---- DEVELOPMENT ONLY ------------------------------------------------
if settings.DEBUG:
    # Serve files from STATICFILES_DIRS
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    # Serve media files (uploaded by users)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
