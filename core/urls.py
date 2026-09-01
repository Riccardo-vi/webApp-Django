from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # pubblica
    path('tickets/', views.TicketListView.as_view(), name='ticket_list'),  # ristretto
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),  # dettaglio
    path('my-tickets/', views.MyTicketsView.as_view(), name='my_tickets'),  # ristretto
    path('tickets/create/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/<int:pk>/edit/', views.TicketUpdateView.as_view(), name='ticket_edit'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('devices/', views.DeviceListView.as_view(), name='device_list'),
    path('devices/<int:pk>/', views.DeviceDetailView.as_view(), name='device_detail'),
    path('devices/create/', views.DeviceCreateView.as_view(), name='device_create'),
    path('devices/<int:pk>/edit/', views.DeviceUpdateView.as_view(), name='device_edit'),
    path('devices/<int:pk>/delete/', views.DeviceDeleteView.as_view(), name='device_delete'),

]
