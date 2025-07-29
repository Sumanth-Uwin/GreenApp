from django.contrib import admin
from .models import (
    UserProfile, UserHistory, EcoAction, Category, Upload, Feedback,
    VisitTracker, ContactMessage, SiteSettings, TeamMember, SearchLog
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'visit_date', 'visit_count')

@admin.register(EcoAction)
class EcoActionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'uploaded_at')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at')

@admin.register(VisitTracker)
class VisitTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'visit_time')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('footer_text', 'theme_color')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'searched_at')
