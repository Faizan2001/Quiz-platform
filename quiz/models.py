from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """Category or subject for quiz questions (e.g., Math, Science, Python)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Question(models.Model):
    """Individual quiz question with multiple choice options"""
    QUESTION_TYPES = [
        ('single', 'Single Answer'),
        ('multiple', 'Multiple Answers'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="The question text")
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='single')
    
    # Soft delete fields
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.category.name}: {self.text[:50]}..."
    
    def delete(self, *args, **kwargs):
        """Soft delete - mark as deleted instead of removing from database"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class Option(models.Model):
    """Answer options for each question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"


class QuizAttempt(models.Model):
    """Tracks each quiz attempt by a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # Quiz configuration
    total_questions = models.IntegerField(default=10)
    passing_score = models.IntegerField(default=70, help_text="Passing score percentage")
    time_limit = models.IntegerField(default=30, help_text="Time limit in minutes")
    
    # Results
    score = models.IntegerField(null=True, blank=True)
    passed = models.BooleanField(default=False)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.started_at.strftime('%Y-%m-%d')})"
    
    def calculate_score(self):
        """Calculate the percentage score for this attempt"""
        total_answers = self.answers.count()
        if total_answers == 0:
            return 0
        
        correct_answers = sum(1 for answer in self.answers.all() if answer.is_correct())
        percentage = (correct_answers / total_answers) * 100
        return round(percentage, 2)
    
    def submit_quiz(self):
        """Mark quiz as completed and calculate final score"""
        self.completed_at = timezone.now()
        self.score = self.calculate_score()
        self.passed = self.score >= self.passing_score
        self.save()


class Answer(models.Model):
    """User's answer for a specific question in a quiz attempt"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(Option, related_name='answers')
    is_flagged = models.BooleanField(default=False, help_text="User flagged for review")
    
    answered_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.user.username} - Q{self.question.id}"
    
    def is_correct(self):
        """Check if the answer is correct"""
        # Get all correct options for the question
        correct_options = set(self.question.options.filter(is_correct=True))
        # Get selected options
        selected = set(self.selected_options.all())
        
        # For answer to be correct, selected options must match correct options exactly
        return correct_options == selected
