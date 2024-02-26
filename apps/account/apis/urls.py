from django.urls import path
from apps.account.apis.views import UsersListView, UserRegisterView, LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='user-registration'),
    path('user-list/', UsersListView.as_view(), name='user-list'),
    path('logout/', LogoutView.as_view(), name='logout')
]

