from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('posts.urls')),
    path('account/', include('account.urls')),
    path('chat/', include('chat.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
