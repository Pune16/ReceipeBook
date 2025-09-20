"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from veges.views import delete_receipe, login_page, logout_page, receipes, update_receipe, register

urlpatterns = [
    path('receipes/', receipes, name="receipes"),
    path('admin/', admin.site.urls),
    path('delete-receipe/<id>/', delete_receipe, name="delete_receipe"),
    path('update-receipe/<id>/', update_receipe, name="update_receipe"),
    path('login/', login_page, name="login"),
    path('register/', register, name="register"), 
    path('logout/',logout_page, name = "logout_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()