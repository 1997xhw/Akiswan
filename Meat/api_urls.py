from django.urls import path

from Meat.api_views import CreateMeatView, MeatView, MeatStatusView, MeatPoolView

urlpatterns = [
    path('create', CreateMeatView.as_view()),
    path('pool', MeatPoolView.as_view()),
    path('', MeatView.as_view()),
    path('status', MeatStatusView.as_view())
]
