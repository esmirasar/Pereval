from django.urls import path
from .views import SubmitDataView

urlpatterns = [
    path('', SubmitDataView.as_view()),
]

