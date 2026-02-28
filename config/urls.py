from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, register, login_view, logout_view, dashboard, textbook_upload, textbook_reader, textbook_delete, speak

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('register/', register),
    path('login/', login_view),
    path('logout/', logout_view),
    path('dashboard/', dashboard, name='dashboard'),
    path('textbooks/upload/', textbook_upload, name='textbook_upload'),
    path('textbooks/<int:pk>/read/', textbook_reader, name='textbook_reader'),
    path('textbooks/<int:pk>/delete/', textbook_delete, name='textbook_delete'),
    path('api/speak/', speak, name='speak'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)