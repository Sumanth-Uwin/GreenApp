from django.urls import path
from . import views
from .views import EventListView, EventDetailView, create_event_view
from .views import TeamListView, TeamMemberDeleteView

app_name = 'ecoapp'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('upload/', views.upload_view, name='upload'),
    path('actions/', views.ActionListView.as_view(), name='action_list'),
    path('actions/<int:pk>/', views.ActionDetailView.as_view(), name='action_detail'),

    path('contact/', views.contact_view, name='contact'),
    path('user_history/', views.user_history_view, name='user_history'),
    path('my_uploads/', views.user_uploads_view, name='user_uploads'),

    path('search/', views.search_view, name='search'),
    path('feedback/', views.feedback_view, name='feedback'),

    # Use only one team list view: either function-based or class-based.
    # Here, I assume you want to use the class-based view TeamListView:
    path('team/', TeamListView.as_view(), name='team_list'),

    # Admin/staff URLs for team members
    path('team/add/', views.team_member_create, name='team_member_add'),
    path('team/<int:pk>/edit/', views.team_member_edit, name='team_member_edit'),
    path('team/delete/<int:pk>/', TeamMemberDeleteView.as_view(), name='team_delete'),

    # Admin/staff URL for site settings edit
    path('admin/site-settings/', views.site_settings_edit, name='site_settings_edit'),
    #path('admin/settings/', views.edit_site_settings, name='site_settings'),
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/create/', create_event_view, name='create_event'),

    # Custom password reset flow
    path('password-request/', views.CustomPasswordRequestView.as_view(), name='custom_password_request'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='custom_password_reset'),
]
