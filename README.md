### Distinctiveness and Complexity

My capstone project is a Learning Management System (LMS), containing several features that are distinct from the other projects. Particularly this LMS is designed for learning cybersecurity in an organizational setting. For this reason, I named the web app **Cyber**.

At a very high level, the concept behind this LMS web app is that users are classified into two: *regular users* and *admin users*. Admin users can do many things such as creating educational contents (or courses) and assigning them to regular users (we will see the other things that admin users can do in later sections). Regular users on the other hand just receive and attend to assigned tasks.

The functionality of this web app can only be accessed when a user is logged in, hence all the views, in views.py, have a decorator directing users to the login page, if they are not logged in.

The web app has five (5) main features. They are listed below:

1. Course management
2. Quiz management
3. Phishing simulator
4. Progress dashboard
5. Employee cyber league: a gamification feature

**Course Management**

The course management feature allows an admin user to create courses and assign them to regular users. Admin users will create a course content, which is just a block of text, alongside other course information such as title, picture, skill level (or difficulty level), and duration. The admin user then assigns the courses to a list of other users.

Users who are assigned a course will see the course displayed on their home page (i.e. the index page). On completing the course (which is just scrolling to the bottom of the page), the user will earn them 3 points in the employee cyber league table (explanation of this will come in later sections).

**Quiz Management**

This is an entire quiz feature that allows admin users to create quizzes and assign those quizzes to other users. Admin users can only create quizzes with 10 questions, each question having 4 choices. To pass a quiz, a user must score at least 7 out of 10. Passing a quiz will earn a user 10 points in the employee cyber league table.

**Phishing Simulator**

A phishing email is an email sent to a person with an intention of stealing information personal to that person, such as passwords and credit card details. Phishing emails are sent by hackers to unsuspecting individuals. A phishing simulator is designed to test the susceptibility, of company employees, of falling for phishing emails or attacks. The idea behind this is to train employees on properly distinguishing between regular emails and phishing emails.

The phishing simulator feature in this web app allows an admin user to send both regular emails and phishing emails to other users, in order to test their ability on recognizing phishing emails. In this web app, phishing emails contain a link. If any user clicks the link (i.e. in the real-world, a malicious link), it will be recorded in the database that the user has clicked on a phishing link and they will then lose 6 points in the employee cyber league.

**Progress Dashboard**

The progress dashboard allows users to view their learning progress in a chart form. They can view their progress on assigned courses, assigned quizzes, and received phishing emails.

**Employee Cyber League**

This is a gamification feature that displays table within the application. The table shows total points gained by all users in a descending order (i.e. the users with the highest points appear top of the table). This allows users to compete with each other and encourages them to complete assigned tasks to gain more points.

The web app contains several Django models to cater for the different features such as Quiz models, Course model, and Email model. The web app also contains JavaScript to dynamically load web page contents such as dynamically loading items on the navigation bar. The web app is also mobile responsive.

### Explanation of each file

**layout.html**

This is the base/layout file for all the other html files. In the head tag, the file is linked to external CSS libraries for quick styling and for the use of icons. The `{% block script %}` section allows other html files to insert their respective script files. 

This file mainly contains the navigation bar functionality and the employee league table. JavaScript is used to dynamically expand hidden navigation bar items.

**assign_quiz.html**

This page extends the layout.html file. It allows the admin user to select a quiz (that was already created) and assign it to other users.

This page is only for admin users.

**compose.html**

This page extends the layout.html file. It allows the admin user to send an email to many recipients at once, and to also indicate whether the email is a phishing email or not.

This page is only for admin users.

**course_content.html**

This page extends the layout.html file. It only displays course title and course content, and checks if a user has completed the course, by scrolling to the end of the page, through a JavaScript `onscroll` event listener.

**course_search_result.html**

This page is just a block of html code that is used by the index.js file for dynamic display of search result. This functionality is for searching courses.

**create_content.html**

This page extends the layout.html file. It allows the admin user to create a course content which would be later used to create a course.

This page is only for admin users.

**create_course.html**

This page extends the layout.html file. It allows an admin user to create a course by inputting course details including an input field for uploading an image. The image is saved in the media folder, which is at the highest level of the project directory. The corresponding Django model field only stores the path to that image.

This page is only for admin users.

**create_quiz.html**

This page extends the layout.html file. It allows an admin user to create a quiz. The admin user will put in a quiz title, tie the quiz to a related course, and can only add 10 quiz questions. The questions are added dynamically with the create_quiz.js file.

**index.html**

This page extends the layout.html file. It displays courses assigned to the logged in user. The courses are displayed in a grid form. When a course is clicked, it takes the user to the course_content.html page.

This page also has a search functionality that dynamically displays results.

**login.html**

This displays the login form and a link to the registration page for users not registered. A user must log in before having access to any of the web app's functionality. This page also displays a logo of the web app sourcing the image from the static folder.

**mail.html**

This page extends the layout.html file. It displays the inbox of the logged in user. When a user clicks on an email, the page dynamically displays content of the email. The inbox.js script is responsible for the dynamic display of email content and also checks an email's content for https links through the use of regular expressions. If a user clicks on the link (i.e. a phishing link in the real world), they will be directed to a page telling them they were phished.

**manage_quiz.html**

This page extends the layout.html file. It displays links to enable admin users to create new quizzes and assign quizzes to users.

This page is only for admin users.

**privileges.html**

This page extends the layout.html file. The page displays users who have admin rights and allows the logged in admin user to assign admin rights to other users.

This page is only for admin users.

**progress.html**

This page extends the layout.html file. It displays the logged in user's progress, in a chart form, regarding phishing links clicked, courses completed, and quizzes attempted. Django templating language is used to pass Django context variables to the progress_chart.js file.

**quizzes.html**

This page extends the layout.html file. It displays the logged in user's assigned quizzes. It shows the completed quizzes and allows users to attempt quizzes.

This page also has a search functionality that dynamically displays results.

**quiz_detail.html**

This page extends the layout.html file. It displays the details of a created quiz. When an admin user creates a new quiz from the create_quiz.html page, they will be directed to the quiz_detail.html page.

This page is only for admin users.

**quiz_result.html**

This page extends the layout.html file. It displays the result of a just-taken quiz from the take_quiz.html page. It indicates whether the user has passed the quiz or not. The pass mark is 7 out of 10.

**quiz_search_result.html**

This page is just a block of html code that is used by the quizzes.js file for dynamic display of search result. This functionality is for searching quizzes.

**register.html**

This displays a form that allows users to sign up to the web app by entering their emails and desired passwords. This page displays a logo of the web app sourcing the image from the static folder.

**take_quiz.html**

This page extends the layout.html file. It allows a user to take a quiz by answering 10 questions. On submitting, the user is directed to the quiz_result.html page.

**you_were_phished.html**

This page extends the layout.html file. Users who clicked on phishing links, from the mail.html page, will be directed to this page. This page only tells users that they were phished.

**base.js**

The content of this file is available in all the other JavaScript files. This is responsible for expanding the navigation bar, for smaller screen sizes, to display navigation bar items. W3.CSS is heavily used to achieve this functionality.

**course_completion.js**

This code is for the course_content.html page. By using an `onscroll` event listener, it checks if the user has reached the end of the page. It then sends the user ID to the backend server through an API.

**create_quiz.js**

This script extends the code from base.js. Additionally, it contains code that dynamically adds quiz questions on the create_quiz.html page, by listening to a button's `onclick` event. When the `questionCount` reaches 10, it allows the admin user to create / register the quiz in the database.

**inbox.js**

This script extends the code from base.js. It also contains code to load the content of an email when the email is clicked and to load the user's mailbox when the back arrow is clicked.

When an email content is loaded, the `/https:\/\/.*?\.com/g` regex checks if the content contains a https link and loads the you_were_phished.html page when the link is clicked.

**index.js**

This script extends the code from base.js. It contains code to instantly/dynamically present search result for courses, by sending an asynchronous request to the course_search_result function in views.py.

**progress_chart.js**

This script extends the code from base.js. It displays user learning progress in a chart form by using the famous Chart.js library. The code snippet `JSON.parse()` is utilized to pass Django template variables for use in JavaScript.

**quizzes.js**

This script extends the code from base.js. It contains code to instantly/dynamically present search result for quizzes, by sending an asynchronous request to the quiz_search_result function in views.py.

**styles.css**

This is web app's custom CSS. It is used across all web pages.

**settings.py**

Changes made to this file are as follows:

- 'cyber' app was added to INSTALLED_APPS.
- 'cyber.context_processors.global_context' was added to TEMPLATES to enable use of Django context variables in all templates or html codes.
- `AUTH_USER_MODEL = "cyber.User"` was added for user login and registration functionality.
- `TIME_ZONE = 'Africa/Lagos'` was added to change time zone to WAT (West Africa Time).
- `MEDIA_URL = '/media/'` was added for serving media files.
- `MEDIA_ROOT = BASE_DIR / 'media'` was added for the path where media files would be stored.

**Project's url.py**

Changes made to this file are as follows:

- `path("", include("cyber.urls"))` was added for the cyber app's url configuration.
- The `if settings.DEBUG:` section is used to serve media files during development.

**App's url.py**

The file contains the following:

- All routes (including API routes) are added to `urlpatterns` list.

**admin.py**

Changes made to this file are as follows:

- The models that need to be access at the Django admin portal are added.

**context_processors.py**

The file contains the following:

- The code contains Django context variable that can be accessed by all html templates.

**forms.py**

The file contains the following:

- Django model form for use in views.py

**models.py**

This contains all the models for the cyber web app, including serialized function for returning JSON output. The `models.ImageField(upload_to="courses/")` code snippet uploads images to the media/courses directory.

**views.py**

This contains all the functions that render html views. It also contains functions for handling API backend functionality.

### Some important folders that were created

**cyber/static/cyber/images**

The images here are used in html and CSS codes to render images.

**media/courses**

This is used by the Django SQLite database to store and retrieve images.

### How to the application

The following are the steps for running the application:

1. Download the distribution code.
2. In your terminal, `cd` into the capstone directory.
3. Run `python manage.py makemigrations cyber` to make migration for the cyber app.
4. Run `python manage.py migrate` to apply migrations to the database.
5. Run `python manage.py createsuperuser` to create a Django super admin.
6. Run `python manage.py runserver` and open the app in your web browser.
7. You will be taken directly to the login page, click "sign up" to register a regular user.
8. Spin up an incognito interface or use a different browser to log in to Django admin portal at http://127.0.0.1/admin.
9. Go to the User model and click the email address of your newly registered regular user. Check the "Is admin" button.
10. Go back to your initial browser interface and reload. Your newly registered regular user will now be an admin user. Subsequent admin rights can be assigned from the *admin panel > user privileges* page.