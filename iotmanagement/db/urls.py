from django.urls import path
from . import views


# base views
urlpatterns = [
    path('', views.home, name='home'),
    # path('create/', views.parameter_create, name='parameter_create')
]

# main app logic mapping
urlpatterns += [
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('invitations/accept/<int:notification_id>/', views.accept_invitation, name='accept_invitation'),
    path('invitations/decline/<int:notification_id>/', views.decline_invitation, name='decline_invitation'),
    path('systems/', views.systems_list, name='systems_list'),
    path('systems/<int:pk>/detail', views.system_detail, name='system_detail'),
    path('systems/<int:pk>/edit', views.system_edit, name='system_edit'),
    path('system/<int:system_id>/remove-user/<int:user_id>/', views.remove_user, name='remove_user'),
    path('system/<int:system_id>/remove-device/<int:device_id>/', views.remove_device, name='remove_device'),
    path('systems/<int:pk>/delete', views.system_delete, name='system_delete'),
    path('systems/create', views.system_create, name='system_create'),
    path('systems/<int:pk>/devices', views.devices_list, name='devices_list'),
    path('devices/', views.devices_list, name='devices_list'),
    path('devices/<int:pk>/', views.devices_detail, name='devices_detail'),
    path('devices/<int:pk>/edit', views.devices_edit, name='devices_edit'),
    path('devices/<int:pk>/delete', views.devices_delete, name='devices_delete'),
    path('devices/create/', views.devices_create, name='devices_create'),
    path('system/<int:system_id>/add-device', views.add_device_to_system, name='add_device_to_system'),
    path('parameter/create', views.parameter_create, name='parameter_create'),
    path('parameter/delete', views.parameter_delete, name='parameter_delete'),
    path('devices/save_selected_parameters/', views.save_selected_parameters, name='save_selected_parameters'),
    path('devices/<int:device_pk>/parameters/<int:parameter_pk>/modify/', views.update_parameter, name='update_parameter'),
    path('devices/<int:device_id>/parameters/<int:parameter_id>/delete/', views.delete_parameter_from_device, name='delete_parameter'),
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