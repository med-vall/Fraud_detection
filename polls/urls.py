from django.contrib.auth.decorators import login_required
from django.urls import path,include

from polls.views import fraude,upload,upload_file
from . import views

urlpatterns = [

    path(r'', upload_file),
    path(r'a', fraude,name='uploa'),
    ]