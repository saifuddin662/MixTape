from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('login_user/', views.LoginFormView.as_view(), name='login_user'),
    path('logout_user/', views.LogOutView.as_view(), name='logout_user'),
    path('<user>/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('create_album/', views.AlbumCreate.as_view(), name='create_album'),
    path('<int:pk>/update_album/', views.AlbumUpdate.as_view(), name='update_album'),
    path('<int:pk>/delete_album/', views.AlbumDelete.as_view(), name='delete_album'),
    path('song/<str:filter_by>', views.SongView.as_view(), name='songs'),
    path('<user>/<int:pk>/create_song/', views.SongCreate.as_view(), name='create_song'),
    path('<int:pk>/delete_song/<int:song_pk>/', views.SongDelete.as_view(), name='delete_song'),
]
