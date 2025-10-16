"""
URL configuration for KEEFA project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.urls')),
    path('api/v1/programs/', include('programs.urls')),
    path('api/v1/donations/', include('donations.urls')),
    path('api/v1/news/', include('news.urls')),
    path('api/v1/contact/', include('contact.urls')),
    path('api/v1/users/', include('users.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"), 
    
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "KEEFA Admin"
admin.site.site_title = "KEEFA Admin Portal"
admin.site.index_title = "Welcome to KEEFA Administration"