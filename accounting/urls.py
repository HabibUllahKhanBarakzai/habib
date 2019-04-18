


from django.contrib import admin
# from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from django.urls import path, include

from accounts import views

router = routers.DefaultRouter()
router.register("transactions", views.TransactionViewSet,base_name="transactions")

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),

]
