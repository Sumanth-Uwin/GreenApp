from django.test import TestCase
from django.contrib.auth.models import User
from .models import EcoAction, Category, Upload, Feedback

class EcoActionModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        category = Category.objects.create(name='Recycling')
        EcoAction.objects.create(title='Recycle paper', description='Recycle old papers', category=category, user=user)

    def test_ecoaction_str(self):
        action = EcoAction.objects.first()
        self.assertEqual(str(action), 'Recycle paper')

class UploadModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='uploaduser', password='testpass')
        category = Category.objects.create(name='Energy')
        Upload.objects.create(title='Solar Panel Manual', description='Manual for solar panel', category=category, user=user)

    def test_upload_str(self):
        upload = Upload.objects.first()
        self.assertEqual(str(upload), 'Solar Panel Manual')

class FeedbackModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='feedbackuser', password='testpass')
        Feedback.objects.create(user=user, comment='Great app!')

    def test_feedback_str(self):
        feedback = Feedback.objects.first()
        self.assertTrue('Great app' in str(feedback))
