from django.urls import path,include
from home.views import index, person, login, PersonAPI, PersonViewset, Register, Login
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'persons', PersonViewset,basename='persons')
urlpatterns = router.urls

urlpatterns = [
    #path('', index),
    path('register/', Register.as_view()),
    path('person/', person),
    path('login/', Login.as_view()),
    path('person_class/', PersonAPI.as_view()),
    path('', include(router.urls))
]