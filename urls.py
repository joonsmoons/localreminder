from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("events/", views.EventListView.as_view(), name="events"),
    path("event/<int:pk>", views.EventDetailView.as_view(), name="event-detail"),
    path("entities/", views.EntityListView.as_view(), name="entities"),
    path("entity/<int:pk>", views.EntityDetailView.as_view(), name="entity-detail"),
]
