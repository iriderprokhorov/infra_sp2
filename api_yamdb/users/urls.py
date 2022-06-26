from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpView, TokenView, UserViewSet

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(),
         ),
    path('v1/auth/token/', TokenView.as_view(),
         ),
    path('v1/', include(router_v1.urls),
         ),
]
