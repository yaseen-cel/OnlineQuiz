"""OnlineQuizProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as ac_views
from exam import views as exam_views
from candidateApp import views as ca_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    #path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('register/',ac_views.register,name='register'),
    path('login/',ac_views.LoginView.as_view(),name='login'),
    path('logout/',ac_views.logout),
    path('index/',ac_views.index,name='index'),
    path('redirect/',ac_views.authRedirect,name='redirect'),
    #Quiz related Url's
    path('examiner/',exam_views.examinerHome,name='examinerHome'),
    path('addquiz/',exam_views.QuizCreateView.as_view(),name='createQuiz'),
    path('listquiz/',exam_views.QuizListView.as_view(),name='listQuiz'),
    path('updatequiz/<int:pk>/',exam_views.QuizUpdateView.as_view()),
    path('deletequiz/<int:pk>/',exam_views.QuizDeleteView.as_view()),
    #Question Related Url's
    path('question/',exam_views.QuestionCreateView.as_view(),name='createQuestion'),
    path('listquestion/',exam_views.QuestionListView.as_view(),name='listQuestion'),
    path('updatequestion/<int:pk>/',exam_views.QuestionUpdateView.as_view()),
    path('deletequestion/<int:pk>/',exam_views.QuestionDeleteView.as_view()),
    #Quiz Qustion Related Url's
    path('addquestions/<int:pk>/',exam_views.ListQuizQuestion,name='addquestions'),
    # path('removequestions/<int:pk>/',exam_views.ListQuizQuestion,name='addquestions'),

    #CandidateApp related url's
    path('quiztoday/',ca_views.candidateQuiz,name='quiztoday'),
    path('quiz/<int:pk>/',ca_views.quiz,name='quiz'),
    path('candidatehome/',ca_views.candidateHome,name='candidatehome'),
    path('results/',ca_views.results,name='results'),
    
]
