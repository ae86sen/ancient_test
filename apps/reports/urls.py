from rest_framework.routers import SimpleRouter, DefaultRouter
from reports import views
router = SimpleRouter()
router.register('reports', views.ReportsViewSet)
urlpatterns = [
]
urlpatterns += router.urls