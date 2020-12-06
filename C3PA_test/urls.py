from django.contrib import admin
from django.urls import path

from .views import PersonView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PersonView.as_view()),
]
