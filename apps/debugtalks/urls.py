from rest_framework.routers import SimpleRouter, DefaultRouter
from debugtalks import views
router = SimpleRouter()
router.register('debugtalks', views.DebugTalksViewSet)
urlpatterns = [
]
urlpatterns += router.urls