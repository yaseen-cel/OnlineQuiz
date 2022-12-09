from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from candidateApp.models import Candidate
import jwt
from datetime import datetime,timedelta
from django.conf import settings
from django.contrib.auth import authenticate,login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .authorization import isAuthorized
# Create your views here.

def register(request):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    if request.method=='POST':
        first_name=request.POST['first_name']
        username=request.POST['email']
        email=request.POST['email']
        mobile =request.POST['mobile']
        password=request.POST['password']
        password1=request.POST['password1']

        if password == password1:
            if User.objects.filter(username = username).exists():
                messages.info(request,'username already exist')
                return redirect('register')

            # elif User.objects.filter(email = email).exists():
            #     messages.info(request,'email already exist')
            #     return redirect('register')

            else:
                user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name)
                user.save()
                user_details = User.objects.get(username = username) 
                print(user_details,'userdetails')
                user1 = Candidate(email=email,name=first_name,mobile = mobile,user = user_details)
                user1.save()
                print("user created")
                return redirect('register')
        else:
            messages.info(request,'Password didnt match')
            return redirect('register')
    else:    
        return render(request,"accounts/register.html",)

# def log_view(request):
#     if request.method == "POST":
#         username=request.POST['username']
#         password=request.POST['password']
#         user=authenticate(request,username=username, password=password )
#         if user is not None:
#             login(request,user)
#             token=jwt.encode({'username':username,'password':password,
#             'exp':datetime.utcnow()+timedelta(hours=24)},
#             settings.SECRET_KEY,algorithm='HS256')
#             return render(request,"accounts/index.html",{'token':token})
#         messages.success(request,("please give correct information"))
#         return redirect('login')
#     return render(request,"accounts/login.html")
class LoginView(APIView):
    def post(self,request):
        if request.method == "POST":
            print('inside post')
            username=request.POST.get('username')
            print(username,'username')
            password=request.POST.get('password')
            user=authenticate(request,username=username, password=password )
            if user is not None:
                login(request,user)
                token=jwt.encode({'username':username,'password':password,
                'exp':datetime.utcnow()+timedelta(minutes=15)},
                settings.SECRET_KEY,algorithm='HS256')
                request.session['Authorization'] = token.decode('utf-8')

                '''To pass token through headers:-

                response = redirect('http://localhost:8000/index/')
                response['Authorization'] = token
                
                return response'''
                if(Candidate.objects.filter(email = username).exists()):
                    return redirect('candidatehome')
                else:
                    return redirect('examinerHome')
            messages.success(request,("please give correct information"))
            return redirect('login')
    def get(self,request):
        
        return render(request,"accounts/login.html")
def index(request):
    if request.method == 'POST':
        return redirect('login')
    else:
        #del request.session['Authorization']
        user = isAuthorized(request)
        print(user,'user')
        return render(request,"accounts/index.html")
def logout(request):
    if(request.session['Authorization']):
        print('inside')
        del request.session['Authorization']
        print('in')
    return redirect('login')
 
def authRedirect(request):
    print('abcd')
    return render(request,"accounts/login.html")
