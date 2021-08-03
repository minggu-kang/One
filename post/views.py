from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Post
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse


class PostMyList(ListView):
    model = Post
    template_name = 'post/post_mylist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:       #로그인확인
            messages.warning(request, '로그인이 필요한기능입니다.')
            return HttpResponseRedirect('/')
        return super(PostMyList, self).dispatch(request, *args, **kwargs)



class PostLikeList(ListView):
    model = Post
    template_name = 'post/post_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:       #로그인확인
            messages.warning(request, '로그인이 필요한기능입니다.')
            return HttpResponseRedirect('/')
        return super(PostLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 좋아요한글 보여주기
        user = self.request.user
        queryset = user.like_post.all()
        return queryset


class PostFavoriteList(ListView):
    model = Post
    template_name = 'post/post_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:       #로그인확인
            messages.warning(request, '로그인이 필요한기능입니다.')
            return HttpResponseRedirect('/')
        return super(PostFavoriteList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 저장한글 보여주기
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset


class PostLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:       # 로그인확인
            return HttpResponseForbidden()
        else:
            if 'post_id' in kwargs:
                post_id = kwargs['post_id']
                post = Post.objects.get(pk=post_id)
                user = request.user
                if user in post.like.all():
                    post.like.remove(user)
                else:
                    post.like.add(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


class PostFavorite(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:       # 로그인확인
            return HttpResponseForbidden()
        else:
            if 'post_id' in kwargs:
                post_id = kwargs['post_id']
                post = Post.objects.get(pk=post_id)
                user = request.user
                if user in post.favorite.all():
                    post.favorite.remove(user)
                else:
                    post.favorite.add(user)
            return HttpResponseRedirect('/')


class PostList(ListView):
    model = Post
    template_name_suffix = '_list'


class PostCreate(CreateView):
    model = Post
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            # 정상작동 한다면
            # form : 모델폼
            form.instance.save()
            return redirect('/')
        else:
            # 정상작동 X
            return self.render_to_response({'form': form})


class PostUpdate(UpdateView):
    model = Post
    fields = ['text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)


class PostDelete(DeleteView):
    model = Post
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정 권한이 없습니다.')
            return HttpResponseRedirect('/')
            # 삭제 페이지에서 권한이 없다 출력
            # detail페이지로 되돌아가서 삭제실패 출력
        else:
            return super(PostDelete, self).dispatch(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name_suffix = '_detail'

