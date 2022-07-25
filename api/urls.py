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
    path('checkUserOnline/<str:username>', checkUserOnline),
    path('checkVetOnline/<str:username>', checkVetOnline),
    path('addMessage/', addMessage),
    path('getAllMessages/<str:sender>/<str:receiver>', getAllMessages),
    path('logout/', logout),
    path('resendEmail/<str:username>', resendEmail),
    path('checkVerified/<str:username>', checkVerified),
    path('loginVet/<str:username>/<str:password>', loginVet),
    path('loginUser/<str:username>/<str:password>', loginUser),
    path('listAnimals/<str:username>', listAnimals),
    path('insertAnimal/', insertAnimal),
    path('insertLocation/', insertLocation),
    path('insertUser/', insertuser),
    path('insertVet/', insertVet),
    path('listlocation/', listlocation),
    path('locationDetails/<int:id>/', locationDetails),
    path('listusers/', listusers),
    path('listvets/', listVets),
    path('finduser/<str:username>/', finduser),
    path('findvet/<str:username>/', findvet),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
