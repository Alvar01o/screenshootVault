from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views 
urlpatterns = [
        path('', views.index, name='index'),
        path('about/', views.about, name='about'),
        path('portfolio/', views.portfolio, name='portfolio'),
        path('contact/', views.contact, name='contact'),
        path('admin/', admin.site.urls),
    ]

# Si estás en modo DEBUG, sirve los archivos estáticos directamente desde el servidor de desarrollo de Django
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
