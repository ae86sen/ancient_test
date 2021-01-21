from rest_framework.routers import SimpleRouter, DefaultRouter

from testcases import views
router = SimpleRouter()
router.register('testcases', views.TestSuitsViewSet)
urlpatterns = [
]
urlpatterns += router.urls