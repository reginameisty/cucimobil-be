from django.urls import include, path, re_path
from rest_framework import routers, serializers, viewsets, permissions
from .views import CustomerViewSet, ServiceViewSet, OrderViewSet, PaymentViewSet, FeedbackViewSet, LoginViewSet, LapakViewSet, ProfileViewSet, LoginView
from . import views
from .views import profile
from .views import process_payment
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'login', LoginViewSet, basename='login')
router.register(r'service', ServiceViewSet)
router.register(r'order', OrderViewSet)
router.register(r'payment', PaymentViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'lapak', LapakViewSet, basename='lapak')
router.register(r'profile', ProfileViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'messages', views.MessageViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', views.register, name='register'),
    path('order_service/', views.order_service, name='order_service'),
    path('order_history/', views.order_history, name='order_history'),
    path('profile/', profile, name='profile'),
    path('process-payment/', process_payment, name='process_payment'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('daftar_lapak/', views.daftar_lapak, name='daftar_lapak'),
    path('api/customer/', views.CustomerListView.as_view(), name='customer-list'),
    path('api/customer/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('customer/register/', views.customer_registration, name='customer-registration'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)