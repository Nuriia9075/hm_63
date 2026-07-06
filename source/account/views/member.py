from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from account.forms import MyUserCreationForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()
# Create your views here.

def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('account:profile', pk=request.user.pk)

    if request.method == 'POST':
        login_input = request.POST.get('username')
        password = request.POST.get('password')
        target_username = login_input
        if '@' in login_input:
            user_by_email = User.objects.filter(email=login_input).first()
            if user_by_email:
                target_username = user_by_email.username
        user = authenticate(request, username=target_username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('account:profile', pk=user.pk)
        else:
            context['has_error'] = True
    return render(request, "account/login.html", context=context)

class RegisterView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'account/register.html'
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if not next_url:
            next_url = reverse_lazy('account:login')
        return next_url

class ProfileDetailView(DetailView):
    template_name = "account/profile.html"
    model = User
    context_object_name = 'profile'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "account/update_profile.html"
    model = User
    form_class = MyUserCreationForm
    success_url = reverse_lazy('account:profile')

class ToggleSubscribeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        target_profile = get_object_or_404(User, pk=pk)
        current_user = request.user
        if target_profile == current_user:
            return redirect('account:profile', pk=pk)
        if current_user.subscriptions.filter(pk=target_profile.pk).exists():
            current_user.subscriptions.remove(target_profile)

            if current_user.following_count > 0:
                current_user.following_count -= 1
            if target_profile.followers_count > 0:
                target_profile.followers_count -= 1
        else:
            current_user.subscriptions.add(target_profile)

            current_user.following_count += 1
            target_profile.followers_count += 1
        current_user.save()
        target_profile.save()
        return redirect('account:profile', pk=pk)

