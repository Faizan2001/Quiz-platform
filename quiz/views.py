from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import random

from .models import Category, Question, QuizAttempt, Answer, Option


def login_view(request):
    """User login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'quiz/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')


@login_required
def dashboard(request):
    """User dashboard showing available categories and recent attempts"""
    categories = Category.objects.all()
    recent_attempts = QuizAttempt.objects.filter(
        user=request.user,
        completed_at__isnull=False
    ).order_by('-completed_at')[:5]
    
    context = {
        'categories': categories,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'quiz/dashboard.html', context)


@login_required
def start_quiz(request, category_id):
    """Start a new quiz for the selected category"""
    category = get_object_or_404(Category, id=category_id)
    
    # Get random questions from this category (not deleted)
    all_questions = list(Question.objects.filter(
        category=category,
        is_deleted=False
    ))
    
    if len(all_questions) == 0:
        messages.error(request, f'No questions available for {category.name}')
        return redirect('dashboard')
    
    # Randomly select up to 10 questions
    num_questions = min(10, len(all_questions))
    selected_questions = random.sample(all_questions, num_questions)
    
    # Create quiz attempt
    attempt = QuizAttempt.objects.create(
        user=request.user,
        category=category,
        total_questions=num_questions
    )
    
    # Create Answer objects for each question
    for question in selected_questions:
        Answer.objects.create(
            attempt=attempt,
            question=question
        )
    
    return redirect('take_quiz', attempt_id=attempt.id)


@login_required
def take_quiz(request, attempt_id):
    """Quiz taking interface"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    # If quiz is already completed, redirect to results
    if attempt.completed_at:
        return redirect('quiz_results', attempt_id=attempt.id)
    
    # Get all answers for this attempt with their questions
    answers = (
        attempt.answers.all()
        .select_related('question')
        .prefetch_related('selected_options', 'question__options')
        .order_by('id')
    )
    
    # Get current question (first unanswered or first one)
    current_answer = answers.first()
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'current_answer': current_answer,
        'total_questions': answers.count(),
    }
    return render(request, 'quiz/take_quiz.html', context)


@login_required
def question_view(request, attempt_id, answer_id):
    """Display a specific question (HTMX target)"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    answer = get_object_or_404(Answer, id=answer_id, attempt=attempt)
    
    # Build next/previous navigation
    ordered_ids = list(
        Answer.objects.filter(attempt=attempt).order_by('id').values_list('id', flat=True)
    )
    idx = ordered_ids.index(answer.id)
    prev_id = ordered_ids[idx - 1] if idx > 0 else None
    next_id = ordered_ids[idx + 1] if idx < len(ordered_ids) - 1 else None
    
    if request.method == 'POST':
        # Save answer
        selected_option_ids = request.POST.getlist('options')
        answer.selected_options.clear()
        for option_id in selected_option_ids:
            option = Option.objects.get(id=option_id)
            answer.selected_options.add(option)
        answer.save()

    has_selection = answer.selected_options.exists()

    context = {
        'attempt': attempt,
        'answer': answer,
        'question': answer.question,
        'prev_id': prev_id,
        'next_id': next_id,
        'is_first': idx == 0,
        'is_last': idx == len(ordered_ids) - 1,
        'has_selection': has_selection,
    }
    return render(request, 'quiz/question_view.html', context)


@login_required
def toggle_flag(request, answer_id):
    """Toggle flag status for a question (HTMX)"""
    answer = get_object_or_404(Answer, id=answer_id)
    answer.is_flagged = not answer.is_flagged
    answer.save()
    
    return JsonResponse({'flagged': answer.is_flagged})


@login_required
def review_panel(request, attempt_id):
    """Review panel showing all questions status (HTMX target)"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    answers = attempt.answers.all().select_related('question').prefetch_related('selected_options')
    
    context = {
        'attempt': attempt,
        'answers': answers,
    }
    return render(request, 'quiz/review_panel.html', context)


@login_required
def submit_quiz(request, attempt_id):
    """Submit the quiz and show results"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    if request.method == 'POST':
        attempt.submit_quiz()
        messages.success(request, 'Quiz submitted successfully!')
        return redirect('quiz_results', attempt_id=attempt.id)
    
    return redirect('take_quiz', attempt_id=attempt.id)


@login_required
def quiz_results(request, attempt_id):
    """Display quiz results with correct/incorrect answers"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    # Get all answers with details
    answers = attempt.answers.all().select_related('question').prefetch_related(
        'selected_options',
        'question__options'
    )
    
    # Build results list with correct/incorrect info
    results = []
    for answer in answers:
        correct_options = answer.question.options.filter(is_correct=True)
        selected_options = answer.selected_options.all()
        
        results.append({
            'question': answer.question,
            'selected_options': selected_options,
            'correct_options': correct_options,
            'is_correct': answer.is_correct(),
        })
    
    context = {
        'attempt': attempt,
        'results': results,
    }
    return render(request, 'quiz/results.html', context)
