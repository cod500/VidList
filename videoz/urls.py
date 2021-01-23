"""videoz URL Configuration

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
from django.contrib import admin, auth
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from vids import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    # Auth
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', auth.views.LoginView.as_view(), name='login'),
    path('logout', auth.views.LogoutView.as_view(), name='logout'),
    # favories
    path('vids/list', views.full_list, name='list_faves'),
    path('vids/create', views.CreateFaves.as_view(), name='create_faves'),
    path('vids/<int:pk>', views.DetailFaves.as_view(), name='detail_faves'),
    path('vids/<int:pk>/update', views.UpdateFaves.as_view(), name='update_faves'),
    path('vids/<int:pk>/delete', views.DeleteFaves.as_view(), name='delete_faves'),
    # Videos
    path('video/<int:pk>/deletevideo',
         views.DeleteVideo.as_view(), name='delete_video'),
    path('vids/<int:pk>/addvideo', views.add_video, name='add_video'),
    path('vids/search', views.video_search, name='video_search'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
