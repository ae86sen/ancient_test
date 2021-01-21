from rest_framework.routers import SimpleRouter, DefaultRouter
from configures import views
router = SimpleRouter()
router.register('configures', views.ConfiguresViewSet)
urlpatterns = [
]
urlpatterns += router.urls