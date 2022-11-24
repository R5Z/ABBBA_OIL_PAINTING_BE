from django.urls import path
from painters import views

urlpatterns = [
        path('download/<int:pk>', views.Download_view, name="download"),
        path('', views.ImageView.as_view(), name='image_view'),
]