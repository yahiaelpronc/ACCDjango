from django.urls import path
from . import views
from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('users-list/', views.usersList),
    # path('users-list/<str:username>', views.getUser),
    # path('users-delete/<str:username>', views.deleteUser),
    path('insertUser/',insertuser),
    path('insertVet/',insertVet),
    path('listlocation/',listlocation),
    path('locationDetails/<int:id>/',locationDetails),
    path('listusers/',listusers),
    path('listvets/',listVets),
    path('finduser/<str:username>/',finduser),
    path('findvet/<str:username>/',findvet),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
