from django.urls import path
from .views import SubmitDataView, SubmitDataDetailView

urlpatterns = [
    path('', SubmitDataView.as_view()),
    path('<int:pk>/', SubmitDataDetailView. as_view()),
]

