from django.urls import path
from .views import PostList, PostDelete, PostDetail, PostUpdate, PostCreate, PostLike, PostFavorite
from django.conf.urls.static import static
from django.conf import settings


app_name = "post"
urlpatterns = [
    path("create/", PostCreate.as_view(), name='create'),
    path("like/<int:post_id>/", PostLike.as_view(), name='like'),
    path('favorite/<int:post_id>/', PostFavorite.as_view(), name='favorite'),
    path("delete/<int:pk>", PostDelete.as_view(), name='delete'),
    path("update/<int:pk>", PostUpdate.as_view(), name='update'),
    path("detail/<int:pk>", PostDetail.as_view(), name='detail'),
    path("", PostList.as_view(), name='index'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)