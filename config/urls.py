
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/', include('common.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

    # ✅ 루트 URL을 pybo 앱으로 연결
    path('', include('pybo.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
