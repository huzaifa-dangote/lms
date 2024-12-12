from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_content", views.create_content, name="create-content"),
    path("create_course", views.create_course, name="create-course"),
    path("course_content/<int:course_id>", views.course_content, name="course-content"),
    path("course_search_result/<int:user_id>", views.course_search_result, name="course-search-result"),
    path("create_quiz", views.create_quiz, name="create-quiz"),
    path("quiz_detail/<int:quiz_id>", views.quiz_detail, name="quiz-detail"),
    path("quiz_result/<int:quiz_id>", views.quiz_result, name="quiz-result"),
    path("take_quiz/<int:quiz_id>", views.take_quiz, name="take-quiz"),
    path("manage_quiz", views.manage_quiz, name="manage-quiz"),
    path("assign_quiz", views.assign_quiz, name="assign-quiz"),
    path("quizzes/<int:user_id>", views.quizzes, name="quizzes"),
    path("quiz_search_result/<int:user_id>", views.quiz_search_result, name="quiz-search-result"),
    path("mail", views.mail, name="mail"),
    path("compose", views.compose, name="compose"),
    path("you_were_phished", views.phished, name="phished"),
    path("progress", views.progress, name="progress"),
    path("privileges", views.privileges, name="privileges"),
    
    # API routes
    path("course_completion/<int:course_id>", views.course_completion, name="course-completion"),
    path("email/<int:email_id>", views.email, name="email")
]