from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from account.forms import MyUserCreationForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context