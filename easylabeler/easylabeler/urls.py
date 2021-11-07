"""easylabeler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from . import functions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.startPage),           # Now, urls.py --> views.py --> startPage(request) --> showing index.html
    path('runMLService', functions.runMLService, name="runMLService"),    # this url is named as "pythonScript"
    path('returnResults', functions.returnResults, name="returnResults"),
    path('handleFormData', functions.handleFormData),
    path('generateLabeledFiles', functions.generateLabeledFiles, name="generateLabeledFiles"),
    path('checkLabeledData', functions.checkLabeledData, name="checkLabeledData"),
    path('handleChangedData', functions.handleChangedData)
]
