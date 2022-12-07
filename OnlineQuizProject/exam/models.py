from django.db import models

# Create your models here.
class Quiz(models.Model):
    quiz_name= models.CharField(max_length = 20,null = True)
    quiz_date = models.DateTimeField(null = True)
    start_time = models.TimeField(null = True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False,null = True)
    duration = models.IntegerField(null = True)
    num_of_questions = models.IntegerField(null = True)
    maximum_marks = models.IntegerField(null = True)
    marks_per_question = models.IntegerField(null = True)
    question_negative_marks = models.IntegerField(null = True)

class Question(models.Model):
    question = models.TextField(null = True)
    option1 = models.CharField(max_length = 30,null = True)
    option2 = models.CharField(max_length = 30,null = True)
    option3 = models.CharField(max_length = 30,null = True)
    option4 = models.CharField(max_length = 30,null = True)
    choices= (('A', 'option1'), ('B', 'option2'), ('C', 'option3'), ('D', 'option4'))
    correct_answer = models.CharField(max_length=1, choices=choices)

    def __str__(self):
        return str(str(self.id) + '-' + self.question)  

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete = models.CASCADE,null = True)
    question = models.ForeignKey(Question,on_delete = models.CASCADE,null = True)
