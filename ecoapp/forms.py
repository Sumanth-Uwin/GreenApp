from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Upload, EcoAction, Feedback, ContactMessage, TeamMember, Event
from .models import SiteSettings, TeamMember


# ✅ Person 1: Register, Login, Custom Password Reset
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)


class CustomPasswordRequestForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")

class CustomPasswordResetForm(forms.Form):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("new_password")
        pw2 = cleaned_data.get("confirm_password")
        if pw1 and pw2 and pw1 != pw2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data


# ✅ Person 2: Upload and EcoAction forms
class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['title', 'description', 'category', 'file']


class EcoActionForm(forms.ModelForm):
    class Meta:
        model = EcoAction
        fields = ['title', 'description', 'category']


# ✅ Person 3: Contact Form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']


# ✅ Person 4: SiteSettings and TeamMember Forms
# forms.py


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['footer_text', 'theme_color']

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'bio', 'photo']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'date', 'time', 'location', 'city', 'image']



# ✅ Person 5: Feedback and Search
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title or description'
        })
    )
