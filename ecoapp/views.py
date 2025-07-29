from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View, DeleteView
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    LoginActivity, TeamMember, SiteSettings, EcoAction, Upload,
    Feedback, ContactMessage, SearchLog, UserHistory, VisitTracker, Event
)
from .forms import (
    RegisterForm, UploadForm, EcoActionForm, FeedbackForm,
    ContactForm, TeamMemberForm, SiteSettingsForm, SearchForm,
    CustomPasswordRequestForm, CustomPasswordResetForm, EventForm
)

User = get_user_model()

# Home View
class HomeView(TemplateView):
    template_name = 'ecoapp/home.html'

# Register View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ecoapp:home')
    else:
        form = RegisterForm()
    return render(request, 'ecoapp/register.html', {'form': form})

# Login & Logout
class CustomLoginView(DjangoLoginView):
    template_name = 'ecoapp/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'ecoapp:login'

# Password Reset Steps
class CustomPasswordRequestView(View):
    def get(self, request):
        form = CustomPasswordRequestForm()
        return render(request, 'ecoapp/custom_password_request.html', {'form': form})

    def post(self, request):
        form = CustomPasswordRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(username=username, email=email)
                request.session['reset_user_id'] = user.id
                return redirect('ecoapp:custom_password_reset')
            except User.DoesNotExist:
                messages.error(request, "Username and email do not match. Try again or create a new account.")
        return render(request, 'ecoapp/custom_password_request.html', {'form': form})

class CustomPasswordResetView(View):
    def get(self, request):
        if not request.session.get('reset_user_id'):
            return redirect('ecoapp:custom_password_request')
        form = CustomPasswordResetForm()
        return render(request, 'ecoapp/custom_password_reset.html', {'form': form})

    def post(self, request):
        if not request.session.get('reset_user_id'):
            return redirect('ecoapp:custom_password_request')
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user_id = request.session['reset_user_id']
            user = get_object_or_404(User, id=user_id)
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            del request.session['reset_user_id']
            messages.success(request, "Password reset successful. Please login.")
            return redirect('ecoapp:login')
        return render(request, 'ecoapp/custom_password_reset.html', {'form': form})

# Upload View
@login_required
def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.uploaded_at = timezone.now()
            upload.save()
            return redirect('ecoapp:user_uploads')
    else:
        form = UploadForm()
    return render(request, 'ecoapp/upload.html', {'form': form})

# EcoAction Views
class ActionListView(ListView):
    model = EcoAction
    template_name = 'ecoapp/action_list.html'
    context_object_name = 'actions'

class ActionDetailView(DetailView):
    model = EcoAction
    template_name = 'ecoapp/action_detail.html'
    context_object_name = 'action'

# Contact View
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save message in DB
            messages.success(request, "Thank you for your message! We will get back to you soon.")
            return redirect('ecoapp:contact')
    else:
        form = ContactForm()
    return render(request, 'ecoapp/contact.html', {'form': form})

# User History View
@login_required
def user_history_view(request):
    login_activities = LoginActivity.objects.filter(user=request.user).order_by('-login_date')
    total_logins = login_activities.count()

    visit_count = int(request.COOKIES.get('visit_count', 0)) + 1
    last_visit = request.COOKIES.get('last_visit', 'First Visit')
    current_time = timezone.now()
    first_visit = (visit_count == 1)

    response = render(request, 'ecoapp/user_history.html', {
        'total_logins': total_logins,
        'login_dates': [activity.login_date for activity in login_activities],
        'visit_count': visit_count,
        'last_visit': last_visit,
        'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'first_visit': first_visit,
    })

    response.set_cookie('visit_count', visit_count, max_age=60*60*24*30)
    response.set_cookie('last_visit', current_time.strftime('%Y-%m-%d %H:%M:%S'), max_age=60*60*24*30)
    return response

# Visit Tracker Middleware
def track_visit(get_response):
    def middleware(request):
        ip = get_client_ip(request)
        if request.user.is_authenticated:
            VisitTracker.objects.create(
                user=request.user,
                ip_address=ip,
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        return get_response(request)
    return middleware

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

# Team Views
class TeamListView(ListView):
    model = TeamMember
    template_name = 'ecoapp/team_list.html'
    context_object_name = 'team_members'

@staff_member_required
def team_member_create(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Team member added successfully.")
            return redirect('ecoapp:team_list')
    else:
        form = TeamMemberForm()
    return render(request, 'ecoapp/team_member_form.html', {'form': form, 'title': 'Add Team Member'})

@staff_member_required
def team_member_edit(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Team member updated successfully.")
            return redirect('ecoapp:team_list')
    else:
        form = TeamMemberForm(instance=member)
    return render(request, 'ecoapp/team_member_form.html', {'form': form, 'title': 'Edit Team Member'})

class TeamMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = TeamMember
    template_name = 'ecoapp/team_member_confirm_delete.html'
    success_url = reverse_lazy('ecoapp:team_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You don't have permission to delete team members.")
            return redirect('ecoapp:team_list')
        return super().dispatch(request, *args, **kwargs)

# Site Settings
@staff_member_required
def site_settings_edit(request):
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings()

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings updated.")
            return redirect('ecoapp:site_settings_edit')
    else:
        form = SiteSettingsForm(instance=settings)
    return render(request, 'ecoapp/site_settings_form.html', {'form': form})

# Search View
def search_view(request):
    form = SearchForm(request.GET or None)
    eco_actions = []
    uploads = []
    query = ''

    if form.is_valid():
        query = form.cleaned_data['query']
        eco_actions = EcoAction.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        uploads = Upload.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

        if query.strip():
            SearchLog.objects.create(user=request.user if request.user.is_authenticated else None, query=query)

    return render(request, 'ecoapp/search.html', {
        'form': form,
        'actions': eco_actions,
        'uploads': uploads,
        'query': query,
    })

# Feedback View
@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.user = request.user
            fb.save()
            return redirect('ecoapp:home')
    else:
        form = FeedbackForm()
    return render(request, 'ecoapp/feedback.html', {'form': form})

# User Uploads View
@login_required
def user_uploads_view(request):
    user_uploads = Upload.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'ecoapp/user_uploads.html', {'uploads': user_uploads})

# ----------- Event Views --------------

class EventListView(ListView):
    model = Event
    template_name = 'ecoapp/event_list.html'
    context_object_name = 'events'
    ordering = ['-date']

class EventDetailView(DetailView):
    model = Event
    template_name = 'ecoapp/event_detail.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj

@login_required
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('ecoapp:event_list')
    else:
        form = EventForm()
    return render(request, 'ecoapp/create_event.html', {'form': form})
