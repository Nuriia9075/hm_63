from django.urls import reverse
from django.views.generic import CreateView
from account.forms import PostForm
from account.models import Post


class PostAddView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "partials/post_add.html"

    def form_valid(self, form):
        post= form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("account:profile", kwargs={"pk": self.request.user.pk})
