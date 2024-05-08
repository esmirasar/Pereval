from django.urls import path
from .views import SubmitDataView, SubmitDataDetailView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', SubmitDataView.as_view(), name='api_view'),
    path('<int:pk>/', SubmitDataDetailView. as_view(), name='api_detail'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

