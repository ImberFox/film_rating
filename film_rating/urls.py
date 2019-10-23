"""film_rating URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from app import views


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^get_token', views.get_new_token),
    re_path(r'^delete_film_rating', views.delete_film_rating),
    re_path(r'^status', views.root),
    re_path(r'^delete_rating', views.delete_rating),
    re_path(r'^get_linked_objects/(?P<id>[-\w]+)$', views.get_linked_objects),
    re_path(r'^get_rating/(?P<id>[-\w]+)', views.get_rating),
    re_path(r'^set_rating', views.set_rating),
    re_path(r'^$', views.root),
]

#or new style
#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('delete_film_rating', views.delete_film_rating),
#    path('status/', views.root),
#    path('get_linked_objects/<slug:id>/', views.get_linked_objects),
    #path(r'^get_films_by_user/slug:id', views.get_films_by_user),
    #path(r'^get_users_by_film/(?P<f_id>[-\w]+)', views.get_films_by_user),
#    path('get_rating/<slug:id>/', views.get_rating),
#    path('set_rating/', views.set_rating),
#    path('', views.root),
#]
