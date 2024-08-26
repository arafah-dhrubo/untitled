from django.urls import path
from goal.views import *

urlpatterns = [
    path('', GoalListApiView.as_view(), name='base-list'),
    path('<int:pk>/', GoalDetailApiView.as_view(), name='base-detail'),

]
