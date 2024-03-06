from django.urls import path

from core.accounts.views.user.views import *

app_name = 'accounts'

urlpatterns = [
    path('', UserTemplateView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('my/profile/', UserProfileView.as_view(), name='user_profile'),
    path('update/password/', UserChangePassswordView.as_view(), name='user_update_password'),
    path('change/group/<int:pk>/', UserChangeGroupView.as_view(), name='user_change_group'),
]
