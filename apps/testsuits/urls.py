from rest_framework.routers import SimpleRouter, DefaultRouter

from testsuits import views
router = SimpleRouter()
router.register('testsuits', views.TestSuitsViewSet)
urlpatterns = [
]
urlpatterns += router.urls