from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from .models import LoginActivity

@receiver(user_logged_in)
def log_login_activity(sender, user, request, **kwargs):
    today = now().date()
    LoginActivity.objects.get_or_create(user=user, login_date=today)
