from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect # Added for the redirect

# Function to handle the root URL
def root_redirect(request):
    return redirect('admin:index')

urlpatterns = [
    # Redirect root (/) to Admin/Jazzmin Login
    path('', root_redirect),

    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/v1/', include('core.urls')),
    path('api/v1/programs/', include('programs.urls')),
    path('api/v1/donations/', include('donations.urls')),
    path('api/v1/news/', include('news.urls')),
    path('api/v1/contact/', include('contact.urls')),
    path('api/v1/users/', include('users.urls')),
    
    # Editor
    path("ckeditor5/", include('django_ckeditor_5.urls')), 
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization (Jazzmin will use these as defaults)
admin.site.site_header = "KEEFA Admin"
admin.site.site_title = "KEEFA Admin Portal"
admin.site.index_title = "Welcome to KEEFA Administration"