from django.urls import path
from .views import trigger_etl
from . import views
from .views import user_demographics

urlpatterns = [
     path('trigger-etl/', trigger_etl, name='trigger_etl'),
     path('charts/', views.index, name='charts'),  # Main chart view
     path('unified_charts/', views.unified_charts, name='unified_charts'),
     path('donation_analysis/', views.donation_analysis, name='donation_analysis'),
     path('user-demographics/', user_demographics, name='user_demographics'),
     path('service-charges-overview/', views.service_charges_overview, name='service_charges_overview'),
     
]


