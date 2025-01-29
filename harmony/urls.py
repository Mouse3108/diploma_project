from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from information.views import *
from events.views import *
from tests.views import *
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('information/', include('information.urls')),
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('tests/', include('tests.urls')),
    path('tinymce/', include('tinymce.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = custom_404_view
