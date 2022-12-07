import datetime
from datetime import datetime as dt,timedelta
from django.shortcuts import render,redirect
from exam.models import Quiz,Question,QuizQuestion
from candidateApp.models import CandidateQuiz,CandidateQuizQuestions,Candidate
import pytz
from accounts.authorization import isAuthorized
from django.contrib.auth.decorators import login_required

# Create your views here.

def candidateQuiz(request):
    user_email = isAuthorized(request)
    today_date = datetime.date.today()
    print(today_date)
    timezone = pytz.timezone("Asia/Kolkata")
    time_now = datetime.datetime.now(tz=timezone).time()
    today_quiz = Quiz.objects.filter(quiz_date = today_date).values()

    quiz_ready_to_start =[]
    for quiz in today_quiz:
        #(print(quiz,'quiz',type(quiz))
        print(quiz['start_time'],time_now,quiz['end_time'])
        if quiz['start_time'] <= time_now and time_now <= quiz['end_time'] :
            quiz_ready_to_start.append(quiz['id'])
    print(quiz_ready_to_start,'available ids')
    context = {
                'today_quiz':today_quiz,
                'quiz_ready_to_start':quiz_ready_to_start,
            }
    return render(request,'candidateApp/list_candidate_quiz.html',context)

def quiz(request,**kwargs):
    user_email = isAuthorized(request)
    candidate_obj = Candidate.objects.get(email = user_email)
    quiz_id = kwargs['pk']
    quiz_obj = Quiz.objects.get(id = quiz_id)
    quiz_details = Quiz.objects.filter(id = quiz_id).values()[0]
    quiz_question_ids = list(QuizQuestion.objects.values_list('question').filter(quiz = quiz_details['id']))
    ids=[]
    
    timezone = pytz.timezone("Asia/Kolkata")
    timenow = dt.now(tz=timezone)
    duration = quiz_details['duration']
    addtime= timenow + timedelta(hours=duration)
    endtime = addtime. strftime("%m/%d/%Y, %H:%M:%S")

    quiz_end = quiz_details['end_time']
    today_date = datetime.date.today()
    quiz_end_time = datetime. datetime. combine(today_date, quiz_end)
    quiz_end_time = quiz_end_time.strftime("%m/%d/%Y, %H:%M:%S")
    print(quiz_end_time,'end timequiz')

    check_candidate = CandidateQuiz.objects.filter(quiz = quiz_obj,candidate = candidate_obj).values()[0]
    if check_candidate == None:
        context = {
            'message': 'You already attend this quiz, Thank you!'
        }
    else:
        for i in quiz_question_ids:
            ids.append(i[0])
        quiz_questions = list(Question.objects.filter(id__in = ids).values())
        context = {
            'quiz' : quiz_details,
            'quizQuestions' : quiz_questions,
            'endtime'  : endtime,
            'quiz_end_time':quiz_end_time
        }


    if request.method == 'POST':

        for id in ids:
            question_id = id
            questionobj = Question.objects.filter(id = question_id).values()[0]
            quest_obj = Question.objects.get(id = question_id)
            answer = request.POST.get(str(id))
            if answer:
                is_attempted = True
                is_correct = True if questionobj['correct_answer'] == answer else False
                if(is_correct == True):
                    mark = quiz_details['marks_per_question']
                else:
                    mark = quiz_details['question_negative_marks']
            else:
                is_attempted = False
                mark = 0
                is_correct = False
            answerObj = CandidateQuizQuestions.objects.create(candidate = candidate_obj, quiz= quiz_obj , question = quest_obj,is_correct = is_correct,marks = mark,is_attempted=is_attempted)
            answerObj.save()

        # Section For Candidate Quiz
        no_of_attempted = CandidateQuizQuestions.objects.filter(quiz = quiz_obj,candidate = candidate_obj,is_attempted = True).count()
        print(no_of_attempted,'attempted')
        no_of_correct_questions = CandidateQuizQuestions.objects.filter(quiz = quiz_obj,candidate = candidate_obj,is_correct = True).count()
        print(no_of_correct_questions,'corrct answer')
        #total_no_questions = quiz_details['num_of_questions]

        no_of_incorrect_questions = no_of_attempted - no_of_correct_questions
        print(no_of_incorrect_questions,'incorrect')
        total_mark = (no_of_correct_questions * quiz_details['marks_per_question']) + (no_of_incorrect_questions * quiz_details['question_negative_marks'])
        print(total_mark,'total mark')
        result = CandidateQuiz.objects.create(candidate = candidate_obj,quiz = quiz_obj,num_attempted_questions = no_of_attempted,num_correct_questions =no_of_correct_questions,num_incorrect_questions = no_of_incorrect_questions,total_marks = total_mark)
        result.save()
        return redirect('candidatehome')
    return render(request,'candidateApp/quiz.html',context)

def candidateHome(request):
    user_email = isAuthorized(request)

    return render(request,'candidateApp/candidatehome.html')

def results(request):
    user_email = isAuthorized(request)
    print(user_email,'user name')
    if(user_email):
        candidate_obj = Candidate.objects.filter(email = user_email).first()
        results = CandidateQuiz.objects.filter(candidate = candidate_obj)
    
    return render(request,'candidateApp/results.html',{'results':results})
