"""
URL configuration for onefin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from task import views, account_view, count_middleware_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # views url
    path('movies/', views.Movies.as_view()),
    path('collection/', views.CollectionView.as_view()),
    path('collection/<collection_uuid>/', views.CollectionEditView.as_view()),

    # count count_middleware_view urls
    path('request-count/', count_middleware_view.RequestCountView.as_view(), name='request-count'),
    path('request-count/reset/', count_middleware_view.ResetRequestCountView.as_view(), name='reset-request-count'),


    # accounts urls
    path('register/', account_view.RegistrationView.as_view(), name='login'),
    path('login/', account_view.LoginView.as_view(), name='login'),
]
