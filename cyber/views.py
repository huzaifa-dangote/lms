from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Course, Quiz, QuizQuestion, QuizChoice, QuizAnswer, QuizScore, Email
from .forms import ContentForm, CourseForm

# Create your views here.

@login_required(login_url="/login")
def index(request):
    
    # Get all courses in reverse chronological order
    courses = request.user.courses.all()
    courses = courses.order_by("-timestamp").all()
    
    return render(request, "cyber/index.html", {
        "courses": courses
    })

@login_required(login_url="/login")
def course_search_result(request, user_id):
    # Get the user
    user = User.objects.get(id=user_id)
    
    # Get all courses in reverse chronological order
    courses = user.courses.all()
    courses = courses.order_by("-timestamp").all()
    
    # Search functionality
    course_title = request.GET.get('course_title')
    
    if course_title:
        courses = courses.filter(title__icontains=course_title)
        
    return render(request, "cyber/course_search_result.html", {
        "courses": courses
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid email and/or password.")
            return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "cyber/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return HttpResponseRedirect(reverse("register"))

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Email already taken.")
            return HttpResponseRedirect(reverse("register"))
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cyber/register.html")
    
@login_required(login_url="/login")
def create_content(request):
    
    if request.method == "POST":
        form = ContentForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Course content was created successfully")
            return HttpResponseRedirect(reverse("create-content"))
            
    return render(request, "cyber/create_content.html", {
        "form": ContentForm()    
    })

@login_required(login_url="/login")
def create_course(request):
    
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit=False) # Save ForeignKey fields
            instance.save()
            form.save_m2m() # Save ManyToMany fields
            messages.success(request, "Course was created successfully")
            return HttpResponseRedirect(reverse("create-course"))
        
    return render(request, "cyber/create_course.html", {
        "form": CourseForm()    
    })

@login_required(login_url="/login")
def course_content(request, course_id):
    course = Course.objects.get(id=course_id)
    
    return render(request, "cyber/course_content.html", {
        "course": course    
    })

@csrf_exempt
@login_required(login_url="/login")
def course_completion(request, course_id):
    
    # Query for requested course
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({"error": "course not found."}, status=404)
    
    # Record users who have completed assigned courses
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("completed_by") is not None:
            user_id = int(data["completed_by"])
            user = User.objects.get(id=user_id)
            if user not in course.completed_by.all():
                course.completed_by.add(user)
                user.points += 3 # Add 3 points in the employee cyber league table
                user.save()
            return HttpResponse(status=204)
        return JsonResponse({"error": "Invalid request"}, status=400)
    
    else:
        return JsonResponse({"error": "Only PUT request allowed"}, status=400)

@login_required(login_url="/login")
def create_quiz(request):
    
    if request.method == "POST":
        title = request.POST.get("title")
        course_id = request.POST.get("course_id")
        course = Course.objects.get(id=course_id)
        quiz = Quiz.objects.create(title=title, course=course)
        
        for i in range(10):
            question_text = request.POST.get(f"question_{i}")
            question = QuizQuestion.objects.create(quiz=quiz, text=question_text)
            
            for j in range(4):
                choice_text = request.POST.get(f"choice_{i}_{j}")
                is_correct = request.POST.get(f"is_correct_{i}_{j}") == 'on'
                QuizChoice.objects.create(question=question, text=choice_text, is_correct=is_correct)
                
        return HttpResponseRedirect(reverse("quiz-detail", args=(quiz.id,)))
    
    courses = Course.objects.all()
    return render(request, "cyber/create_quiz.html", {
        "courses": courses    
    })

@login_required(login_url="/login")
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    
    if request.method == "POST":
        
        for question in quiz.questions.all():
            choice_id = request.POST.get(f"question_{question.id}")
            QuizAnswer.objects.create(user=request.user, question=question, choice_id=choice_id)
            
        quiz.completed_by.add(request.user)
        return HttpResponseRedirect(reverse("quiz-result", args=(quiz.id,)))
    
    return render(request, "cyber/take_quiz.html", {
        "quiz": quiz
    })

@login_required(login_url="/login")
def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    
    return render(request, "cyber/quiz_detail.html", {
        "quiz": quiz,
        "questions": questions
    })

@login_required(login_url="/login")
def quiz_result(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    answers = QuizAnswer.objects.filter(user=request.user, question__quiz=quiz)
    
    score = 0
    for answer in answers:
        if answer.choice.is_correct:
            score += 1
    
    # Save the score in the database
    QuizScore.objects.create(user=request.user, quiz=quiz, score=score)
    
    # Users who score at least 7 out of 10 have passed
    if score >= 7 and request.user not in quiz.passed_by.all():
        quiz.passed_by.add(request.user)
        request.user.points += 10 # Add 10 points in the employee cyber league table
        request.user.save()

    return render(request, "cyber/quiz_result.html", {
        "quiz": quiz,
        "score": score,
        "total": questions.count()
    })

@login_required(login_url="/login")
def manage_quiz(request):
    return render(request, "cyber/manage_quiz.html")

@login_required(login_url="/login")
def assign_quiz(request):
    
    if request.method == "POST":
        quiz_id = request.POST.get(f"quiz_id")
        selected_users = request.POST.getlist("users")
        
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.assigned_to.set(selected_users)
        
        messages.success(request, "Quiz was assigned successfully")
        return HttpResponseRedirect(reverse("manage-quiz"))
    
    quizzes = Quiz.objects.all()
    users = User.objects.all()
    return render(request, "cyber/assign_quiz.html", {
        "quizzes": quizzes,
        "users": users
    })

@login_required(login_url="/login")
def quizzes(request, user_id):
    
    # Get the user
    user = User.objects.get(id=user_id)
    
    # Get all assigned quizzes in reverse chronological order
    quizzes = user.quizzes.all()
    quizzes = quizzes.order_by("-timestamp").all() 
    
    return render(request, "cyber/quizzes.html", {
        "quizzes": quizzes
    })

@login_required(login_url="/login")
def quiz_search_result(request, user_id):
    
    # Get the user
    user = User.objects.get(id=user_id)
    
    # Get all quizzes in reverse chronological order
    quizzes = user.quizzes.all()
    quizzes = quizzes.order_by("-timestamp").all()
    
    # Search functionality
    quiz_title = request.GET.get('quiz_title')
    
    if quiz_title:
        quizzes = quizzes.filter(title__icontains=quiz_title)
        
    return render(request, "cyber/quiz_search_result.html", {
        "quizzes": quizzes
    })

@login_required(login_url="/login")
def privileges(request):
    
    if request.method == "POST":
        selected_users = request.POST.getlist("users")
        user_ids = list(map(int, selected_users)) 
        users = User.objects.filter(id__in=user_ids)
        
        for user in users:
            if user.is_admin == False:
                user.is_admin = True
                user.save()
            
        messages.success(request, "Successful")
        return HttpResponseRedirect(reverse("privileges"))
    
    admin_users = User.objects.filter(is_admin=True)
    users = User.objects.exclude(is_admin=True)
    return render(request, "cyber/privileges.html", {
        "users": users,
        "admin_users": admin_users
    })

@login_required(login_url="/login")
def mail(request):
    emails = Email.objects.filter(recipients=request.user)
    
    # Get emails in reverse chronological order
    emails = emails.order_by("-timestamp").all()
    
    return render(request, "cyber/mail.html", {
        "emails": emails    
    })

@login_required(login_url="/login")
def compose(request):
    
    if request.method == 'POST':
        recipients_usernames = request.POST.getlist('recipients')
        recipients = User.objects.filter(username__in=recipients_usernames)
        subject = request.POST['subject']
        body = request.POST['body']
        is_phishing = 'is_phishing' in request.POST
        email = Email.objects.create(
            sender=request.user, 
            subject=subject, 
            body=body, 
            is_phishing=is_phishing
        )
        email.recipients.set(recipients)
        
        return HttpResponseRedirect(reverse("mail"))
    
    users = User.objects.all()
    return render(request, "cyber/compose.html", {
        "users": users    
    })

@csrf_exempt
@login_required(login_url="/login")
def email(request, email_id):

    # Query for requested email
    try:
        email = Email.objects.get(id=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email content
    if request.method == "GET":
        return JsonResponse(email.serialize())

    # Record users who have clicked phishing links
    elif request.method == "PUT":
        data = json.loads(request.body)
        if email.is_phishing and data.get("clicked_by") is not None:
            user_id = int(data["clicked_by"])
            user = User.objects.get(id=user_id)
            if user not in email.clicked_by.all():
                email.clicked_by.add(user)
                user.points -= 6 # Substract 6 points from employee cyber league table
                user.save()
            return HttpResponse(status=204)
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
   
@login_required(login_url="/login")
def phished(request):
    return render(request, "cyber/you_were_phished.html")

@login_required(login_url="/login")
def progress(request):
    user = User.objects.get(id=request.user.id)
    
    # Get phishing links clicked
    no_links_clicked = len(user.links_clicked.all())
    
    # Get phishing links unclicked
    emails = user.received_emails.filter(is_phishing=True)
    no_of_emails = len(emails)
    no_links_unclicked = no_of_emails - no_links_clicked
    
    # Get courses completed
    no_courses_completed = len(user.courses_completed.all())
    no_of_courses = len(user.courses.all())
    
    # Get quizzes completed
    no_quizzes_completed = len(user.quizzes_completed.all())
    no_of_quizzes = len(user.quizzes.all())
    
    data = {
        "phishing_labels": ["Links clicked", "Links unclicked"],
        "course_labels": ["Courses assigned", "Courses completed"],
        "quiz_labels": ["Quizzes assigned", "Quizzes completed"],
        "phishing": [no_links_clicked, no_links_unclicked],
        "course": [no_of_courses, no_courses_completed],
        "quiz": [no_of_quizzes, no_quizzes_completed]
    }
    
    return render(request, "cyber/progress.html", data)