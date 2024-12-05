from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:post_id>', views.post_detailed, name='post_detailed'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('create', views.create_post, name='create'),
    path('update/<int:post_id>', views.update_post, name='update'),
    path('delete/<int:post_id>', views.delete_post, name='delete'),
    path('reply/<int:post_id>/<int:comment_id>/', views.replied_comment, name='reply'),
    path('rate/<int:post_id>/<int:score>/', views.rate_post, name='rate_post'),
]