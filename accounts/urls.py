from django.urls import path
from .views import signup, profile, profile_edit


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('profile_edit/', profile_edit, name='profile_edit'),
]
