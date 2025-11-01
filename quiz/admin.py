from django.contrib import admin
from .models import Category, Question, Option, QuizAttempt, Answer


class OptionInline(admin.TabularInline):
    """Inline form to add options directly when creating/editing questions"""
    model = Option
    extra = 4  # Show 4 empty option fields by default
    fields = ('text', 'is_correct')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for managing quiz categories"""
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for managing quiz questions"""
    list_display = ('text_preview', 'category', 'question_type', 'is_deleted', 'created_at')
    list_filter = ('category', 'question_type', 'is_deleted')
    search_fields = ('text',)
    ordering = ('-created_at',)
    inlines = [OptionInline]
    
    def text_preview(self, obj):
        """Show first 100 characters of question text"""
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Question'


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    """Admin interface for managing answer options"""
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__category')
    search_fields = ('text', 'question__text')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Admin interface for viewing quiz attempts and results"""
    list_display = ('user', 'category', 'score', 'passed', 'started_at', 'completed_at')
    list_filter = ('category', 'passed', 'started_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('score', 'passed', 'started_at', 'completed_at')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin interface for viewing user answers"""
    list_display = ('attempt', 'question', 'is_flagged', 'answered_at')
    list_filter = ('is_flagged', 'attempt__category')
    readonly_fields = ('answered_at',)
