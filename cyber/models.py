from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

SKILL_LEVELS = {
    "Beginner": "Beginner",
    "Intermediate": "Intermediate",
    "Advance": "Advance"
}

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    
class Content(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    
    def __str__(self):
        return f"{self.title}"
    
class Course(models.Model):
    title = models.CharField(max_length=50)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="course")
    assigned_to = models.ManyToManyField(User, blank=False, related_name="courses")
    skill_level = models.CharField(max_length=12, choices=SKILL_LEVELS)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to="courses/")
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    completed_by = models.ManyToManyField(User, blank=True, related_name="courses_completed")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return {
            "completed_by": None 
        }
    
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    assigned_to = models.ManyToManyField(User, blank=True, related_name="quizzes")
    completed_by = models.ManyToManyField(User, blank=True, related_name="quizzes_completed")
    passed_by = models.ManyToManyField(User, blank=True, related_name="quizzes_passed")
    course = models.ForeignKey(Course, blank=True, on_delete=models.CASCADE, related_name="quiz", null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural = "quizzes"

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

class QuizChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
class QuizAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(QuizChoice, on_delete=models.CASCADE)
    
class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Email(models.Model):
    sender = models.ForeignKey(User, related_name='sent_emails', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(User, blank=True, related_name='received_emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_phishing = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    clicked_by = models.ManyToManyField(User, blank=True, related_name="links_clicked")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "recipients": [user.username for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "is_phishing": self.is_phishing,
            "clicked_by": None
        }

    def __str__(self):
        return self.subject
