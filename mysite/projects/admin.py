from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ['username','first_name','last_name']
    search_fields = ['first_name', 'last_name', 'username', 'email', 'phone']

    
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name', 'description']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'methodology',
                    'current_deadline', 'current_budget')
    list_filter = ['current_deadline']
    search_fields = ['name']


class RiskEvaluationAdmin(admin.ModelAdmin):
    list_display = ('project', 'success_chance', 'date')
    list_filter = ['project', 'success_chance', 'date']
    search_fields = ['project']


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name', 'description']


class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'project', 'work_hours')
    list_filter = ['role', 'project']
    search_fields = ['role', 'project']


class TimeWorkedAdmin(admin.ModelAdmin):
    list_display = ('member', 'task', 'time')
    list_filter = ['member', 'task', 'time']
    search_fields = ['member', 'task']


class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('project', 'name')
    list_filter = ['project', 'name']
    search_fields = ['project', 'name', 'description']


class RoleRequirementAdmin(admin.ModelAdmin):
    list_display = ('role',)
    list_filter = ['role', 'skillset']
    search_fields = ['role', 'skillset']


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('project', 'date', 'duration', 'attendence')
    list_filter = ['project', 'date']
    search_fields = ['project', 'date']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('project', 'confidence', 'emotion', 'date')
    list_filter = ['project', 'date']
    search_fields = ['project', 'confidence', 'emotion', 'date']


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'completion_status', 'duration')
    list_filter = ['name', 'project', 'completion_status']
    search_fields = ['name', 'project', 'description', 'completion_status']


admin.site.register(Project, ProjectAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(TimeWorked, TimeWorkedAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(RoleRequirement, RoleRequirementAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(RiskEvaluation, RiskEvaluationAdmin)
