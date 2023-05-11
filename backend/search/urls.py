from django.urls import path
from .views import SearchListOldView, SearchListNewView

urlpatterns = [
    path('v1/', SearchListOldView.as_view(), name='search'),
    path('v2/', SearchListNewView.as_view(), name='search'),
]
