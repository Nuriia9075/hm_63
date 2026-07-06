from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView
from account.forms import PostForm
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
        post.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("account:profile", kwargs={"pk": self.request.user.pk})

class IndexView(ListView):
    model = Post
    template_name = "account/index.html"
    context_object_name = "posts"


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


