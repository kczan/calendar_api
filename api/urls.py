from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register("event", views.EventAPIViewset, basename="events")
router.register("room", views.ConferenceRoomAPIViewset, basename="conference_rooms")
router.register("user", views.CalendarUserAPIViewset, basename="users")

urlpatterns = router.urls
