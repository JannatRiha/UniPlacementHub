from django.urls import path
from .views import analytics
urlpatterns = [path("placement/analytics/", analytics, name="placement_analytics")]
