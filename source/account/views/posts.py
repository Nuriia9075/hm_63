from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView
from account.forms import PostForm, CommentForm
from account.models import Post
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class PostAddView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_add.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.user.posts_count+=1
        post.save()
        post.user.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("account:profile", kwargs={"pk": self.request.user.pk})

class IndexView(ListView):
    model = Post
    template_name = "posts/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = self.request.user
        subscribed_user_ids = user.subscriptions.values_list('pk', flat=True)
        return Post.objects.filter(user_id__in=subscribed_user_ids).order_by('-created_at')

class UserSearchView(ListView):
    model = User
    template_name = "posts/search_form.html"
    context_object_name = "found_users"

    def get_queryset(self):
        query = self.request.GET.get('search')

        if query:
            return User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query)
            )
        return User.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_value'] = self.request.GET.get('search', '')
        return context

class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post_obj = get_object_or_404(Post, pk=pk)
        user = request.user
        if post_obj.likes.filter(pk=user.pk).exists():
            post_obj.likes.remove(user)
            if post_obj.likes_count > 0:
                post_obj.likes_count -= 1
        else:
            post_obj.likes.add(user)
            post_obj.likes_count += 1
        post_obj.save()
        return redirect(request.META.get('HTTP_REFERER', 'account:index'))


class CommentADDView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post_obj = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post_obj
            comment.save()
            post_obj.comment_count += 1
            post_obj.save()
        return redirect(request.META.get('HTTP_REFERER', 'account:index'))


