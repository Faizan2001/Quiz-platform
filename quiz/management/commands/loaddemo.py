"""
Django management command to load demo data for the quiz platform.
Run with: python manage.py loaddemo
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz.models import Category, Question, Option


class Command(BaseCommand):
    help = 'Load demo data into the quiz platform database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Loading demo data...'))
        
        # Create categories
        categories_data = [
            {
                'name': 'Python Programming',
                'description': 'Test your Python programming knowledge'
            },
            {
                'name': 'Web Development',
                'description': 'Questions about HTML, CSS, and JavaScript'
            },
            {
                'name': 'General Knowledge',
                'description': 'Fun general knowledge questions'
            }
]

        self.stdout.write('\nCreating categories...')
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created: {category.name}'))
            else:
                self.stdout.write(f'  - Already exists: {category.name}')

        # Python Programming Questions
        python_cat = Category.objects.get(name='Python Programming')

        python_questions = [
            {
                'text': 'What is the output of print(2 ** 3)?',
                'type': 'single',
                'options': [
                    ('6', False),
                    ('8', True),
                    ('9', False),
                    ('5', False)
                ]
            },
            {
                'text': 'Which of the following is NOT a valid Python data type?',
                'type': 'single',
                'options': [
                    ('int', False),
                    ('float', False),
                    ('char', True),
                    ('str', False)
                ]
            },
            {
                'text': 'What keyword is used to create a function in Python?',
                'type': 'single',
                'options': [
                    ('function', False),
                    ('def', True),
                    ('func', False),
                    ('define', False)
                ]
            },
            {
                'text': 'Which of the following are mutable data types in Python? (Select all that apply)',
                'type': 'multiple',
                'options': [
                    ('List', True),
                    ('Tuple', False),
                    ('Dictionary', True),
                    ('String', False)
                ]
            },
            {
                'text': 'What is the correct way to create a list in Python?',
                'type': 'single',
                'options': [
                    ('list = (1, 2, 3)', False),
                    ('list = [1, 2, 3]', True),
                    ('list = {1, 2, 3}', False),
                    ('list = <1, 2, 3>', False)
                ]
            },
        ]

        self.stdout.write('\nCreating Python questions...')
        for q_data in python_questions:
            question, created = Question.objects.get_or_create(
                text=q_data['text'],
                category=python_cat,
                defaults={'question_type': q_data['type']}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created question: {question.text[:50]}...'))
                for option_text, is_correct in q_data['options']:
                    Option.objects.create(
                        question=question,
                        text=option_text,
                        is_correct=is_correct
                    )
            else:
                self.stdout.write(f'  - Already exists: {question.text[:50]}...')

        # Web Development Questions
        web_cat = Category.objects.get(name='Web Development')

        web_questions = [
            {
                'text': 'What does HTML stand for?',
                'type': 'single',
                'options': [
                    ('Hyper Text Markup Language', True),
                    ('High Tech Modern Language', False),
                    ('Home Tool Markup Language', False),
                    ('Hyperlinks and Text Markup Language', False)
                ]
            },
            {
                'text': 'Which CSS property is used to change text color?',
                'type': 'single',
                'options': [
                    ('text-color', False),
                    ('font-color', False),
                    ('color', True),
                    ('text-style', False)
                ]
            },
            {
                'text': 'What is the correct HTML tag for inserting a line break?',
                'type': 'single',
                'options': [
                    ('<break>', False),
                    ('<br>', True),
                    ('<lb>', False),
                    ('<newline>', False)
                ]
            },
            {
                'text': 'Which of these are JavaScript frameworks? (Select all that apply)',
                'type': 'multiple',
                'options': [
                    ('React', True),
                    ('Django', False),
                    ('Vue.js', True),
                    ('Flask', False)
                ]
            },
        ]

        self.stdout.write('\nCreating Web Development questions...')
        for q_data in web_questions:
            question, created = Question.objects.get_or_create(
                text=q_data['text'],
                category=web_cat,
                defaults={'question_type': q_data['type']}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created question: {question.text[:50]}...'))
                for option_text, is_correct in q_data['options']:
                    Option.objects.create(
                        question=question,
                        text=option_text,
                        is_correct=is_correct
                    )
            else:
                self.stdout.write(f'  - Already exists: {question.text[:50]}...')

        # General Knowledge Questions
        gk_cat = Category.objects.get(name='General Knowledge')

        gk_questions = [
            {
                'text': 'What is the capital of France?',
                'type': 'single',
                'options': [
                    ('London', False),
                    ('Berlin', False),
                    ('Paris', True),
                    ('Madrid', False)
                ]
            },
            {
                'text': 'How many continents are there?',
                'type': 'single',
                'options': [
                    ('5', False),
                    ('6', False),
                    ('7', True),
                    ('8', False)
                ]
            },
            {
                'text': 'What is the largest planet in our solar system?',
                'type': 'single',
                'options': [
                    ('Earth', False),
                    ('Mars', False),
                    ('Jupiter', True),
                    ('Saturn', False)
                ]
            },
        ]

        self.stdout.write('\nCreating General Knowledge questions...')
        for q_data in gk_questions:
            question, created = Question.objects.get_or_create(
                text=q_data['text'],
                category=gk_cat,
                defaults={'question_type': q_data['type']}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created question: {question.text[:50]}...'))
                for option_text, is_correct in q_data['options']:
                    Option.objects.create(
                        question=question,
                        text=option_text,
                        is_correct=is_correct
                    )
            else:
                self.stdout.write(f'  - Already exists: {question.text[:50]}...')

        # Create a demo user
        self.stdout.write('\nCreating demo user...')
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@quiz.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('  Created demo user (username: demo, password: demo123)'))
        else:
            self.stdout.write('  - Demo user already exists')

        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Demo data loaded successfully!'))
        self.stdout.write('='*50)
        self.stdout.write('\nYou can now login with:')
        self.stdout.write('  Admin: Check your superuser credentials')
        self.stdout.write("  Demo:  username='demo', password='demo123'")
