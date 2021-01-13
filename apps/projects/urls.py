from projects import views
from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework.documentation import include_docs_urls
# 1、创建路由对象
# router = SimpleRouter()
router = DefaultRouter()
# 2、注册路由
#   a、第一个参数为路径前缀
#   b、第二个参数为指定视图集，注意不用调用as_view()
router.register('projects', views.ProjectsViewSet)
urlpatterns = [
    # path('projects/', views.ProjectsViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('projects/names/', views.ProjectsViewSet.as_view({'get': 'names'})),
    # path('projects/<int:pk>/interfaces/', views.ProjectsViewSet.as_view({'get': 'interfaces'})),
    # path('projects/<int:pk>/', views.ProjectsViewSet.as_view({'get': 'retrieve',
    #                                                           'put': 'update', 'delete': 'destroy'}))
    # path('projects/', ProjectsCR.as_view())
]
# 3、将路由对象生成的url列表加到urlpatterns中
urlpatterns += router.urls