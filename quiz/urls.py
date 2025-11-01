from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start-quiz/<int:category_id>/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:attempt_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:attempt_id>/question/<int:answer_id>/', views.question_view, name='question_view'),
    path('quiz/<int:attempt_id>/review/', views.review_panel, name='review_panel'),
    path('quiz/<int:attempt_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/<int:attempt_id>/results/', views.quiz_results, name='quiz_results'),
    path('answer/<int:answer_id>/flag/', views.toggle_flag, name='toggle_flag'),
]
