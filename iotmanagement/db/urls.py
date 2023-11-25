from django.urls import path
from . import views


# base views
urlpatterns = [
    path('', views.home, name='home'),
    # path('create/', views.parameter_create, name='parameter_create')
]

# main app logic mapping
urlpatterns += [
    path('systems/', views.systems_list, name='systems_list'),
    path('systems/<int:pk>/detail', views.system_detail, name='system_detail'),
    path('systems/<int:pk>/edit', views.system_edit, name='system_edit'),
    path('systems/<int:pk>/delete', views.system_delete, name='system_delete'),
    path('systems/<int:pk>/invite', views.system_invite, name='system_invite'),
    path('systems/<int:system_id>/remove/<int:user_id>', views.system_remove_user, name='system_remove_user'),
    path('systems/create', views.system_create, name='system_create'),
    path('systems/<int:pk>/devices', views.devices_list, name='devices_list'),
    path('devices/', views.devices_list, name='devices_list'),
    path('devices/<int:pk>/', views.devices_detail, name='devices_detail'),
    path('devices/<int:pk>/edit', views.devices_edit, name='devices_edit'),
    path('devices/<int:pk>/delete', views.devices_delete, name='devices_delete'),
    path('devices/create/', views.devices_create, name='devices_create'),
    path('parameter/create', views.parameter_create, name='parameter_create'),
    path('parameter/delete', views.parameter_delete, name='parameter_delete'),
    path('devices/save_selected_parameters/', views.save_selected_parameters, name='save_selected_parameters'),
]
# user access logic
urlpatterns += [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/delete', views.profile_delete, name='profile_delete'),
    path('profile/changepassword', views.change_password, name='change_password'),
]

# admin logic
urlpatterns += [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/<int:pk>', views.user_detail, name='user_detail'),
    path('admin/users/<int:pk>/edit', views.user_edit, name='user_edit'),
    path('admin/users/<int:pk>/delete/', views.user_delete, name='user_delete'),
]
