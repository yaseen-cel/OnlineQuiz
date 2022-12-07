from django.shortcuts import render,redirect
from .models import Quiz,Question,QuizQuestion
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from accounts.views import isAuthorized

# Create your views here.
#Quiz Related Views
class QuizCreateView(CreateView):
    model = Quiz
    fields = '__all__'
    success_url = reverse_lazy('listQuiz')

class QuizListView(ListView):
    model = Quiz
    ordering = ['-quiz_date']

class QuizUpdateView(UpdateView):
    model = Quiz
    fields = '__all__'
    success_url = reverse_lazy('listQuiz')

class QuizDeleteView(DeleteView):
    model = Quiz
    success_url = reverse_lazy('listQuiz')

#Question Related Views
class QuestionCreateView(CreateView):
    model = Question
    fields = '__all__'
    success_url = reverse_lazy('listQuestion')

class QuestionListView(ListView):
    model = Question
    ordering = ['-id']

class QuestionUpdateView(UpdateView):
    model = Question
    fields = '__all__'
    success_url = reverse_lazy('listQuestion')

class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('listQuestion')

#QuizQuestion related Views
def ListQuizQuestion(request,**kwargs):

    quiz= Quiz.objects.get(id=kwargs['pk'])
    no_of_questions = quiz.num_of_questions
    question = Question.objects.all()

    #To show particular quiz questions
    quiz_questions_ids = list(QuizQuestion.objects.values_list('question').filter(quiz = quiz))
    ids=[]
    for i in quiz_questions_ids:
        ids.append(i[0])
    quiz_questions = list(Question.objects.filter(id__in = ids).values())

    if request.method == 'POST':
        ques = request.POST.get('question')
        ques_obj = Question.objects.get(id = ques)
        #to check duplication
        ques1 = QuizQuestion.objects.filter(quiz = quiz,question = ques_obj)
        if ques1:
            messages.info(request,'Question Already satisfied!')

        elif QuizQuestion.objects.filter(quiz = quiz).count() >= no_of_questions:
            messages.info(request,'There are no more questions needed for this quiz!')

        elif ques is not None:
            quizQuestion = QuizQuestion.objects.create(quiz = quiz , question= ques_obj)
            quizQuestion.save()
            messages.info(request,'Saved!')

        return redirect('addquestions',kwargs['pk'])
    return render(request,'exam/listQuizQuestion.html',{'quiz':quiz,'questions':question,'quizQuestions': quiz_questions})

def removeQuizQuestion(request,**kwargs):
    pass
def examinerHome(request):
    user_email = isAuthorized(request)

    return render(request,'exam/examinerHome.html')