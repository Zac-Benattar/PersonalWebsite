from django.urls import path, include
from rest_framework_nested import routers
from api.views import * 
from rest_framework_simplejwt.views import TokenRefreshView


router = routers.DefaultRouter()
router.register(r'projects', PostsViewSet, basename='posts')
router.register(r'users', UserViewSet)

# user routers , api call : /api/users/myaccount
userAccount_router = routers.NestedDefaultRouter( router, r'users', lookup = 'user')
userAccount_router.register( r'myaccount', MyAccountViewSet, basename='user-myAccount')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(userAccount_router.urls)),
    path('token/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]