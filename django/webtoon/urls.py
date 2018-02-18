
# Webtoon list in localhost:8000
#
# Webtoon detail w/ pk=n in localhost:8000/n
from django.urls import path

from webtoon import views

urlpatterns = [
    path('', views.webtoon_list, name='webtoon-list'),
    path('<int:pk>/', views.webtoon_detail, name='webtoon-detail'),
    # path('<int:pk>/', views.episode_set, name='episode-set'),
]