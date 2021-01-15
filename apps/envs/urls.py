from rest_framework.routers import SimpleRouter, DefaultRouter
from envs import views
router = SimpleRouter()
router.register('envs', views.EnvsViewSet)
urlpatterns = [
]
urlpatterns += router.urls