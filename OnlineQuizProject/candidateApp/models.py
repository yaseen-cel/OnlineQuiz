from django.db import models
from exam.models import Quiz,Question
from django.contrib.auth.models import User
# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length = 100,null = True)
    email = models.CharField(max_length = 100,null = True)
    user = models.ForeignKey(User,null = True,on_delete = models.CASCADE)
    mobile = models.IntegerField(null = True)
    created_at = models.DateTimeField(auto_now_add =True,null = True)
    modified_at = models.DateTimeField(auto_now=True,null = True)

class CandidateQuiz(models.Model):
    candidate = models.ForeignKey(Candidate,on_delete = models.CASCADE,null = True)
    quiz = models.ForeignKey(Quiz,on_delete = models.CASCADE,null = True)
    num_attempted_questions = models.IntegerField(null = True,default =0)
    num_correct_questions = models.IntegerField(null = True,default =0)
    num_incorrect_questions = models.IntegerField(null = True,default =0)
    total_marks = models.IntegerField(null = True,default =0)

class CandidateQuizQuestions(models.Model):
    candidate = models.ForeignKey(Candidate,on_delete = models.CASCADE,null = True)
    quiz = models.ForeignKey(Quiz,on_delete = models.CASCADE,null = True)
    question = models.ForeignKey(Question,on_delete = models.CASCADE,null = True)
    is_correct = models.BooleanField(null = True,default = False)
    marks = models.IntegerField(null = True,default = 0)
    is_attempted = models.BooleanField(default = False,null =True)


