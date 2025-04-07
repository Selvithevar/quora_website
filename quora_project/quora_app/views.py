from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import RegisterForm, QuestionForm, AnswerForm

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'questions': questions})

@login_required
def post_question(request):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        q = form.save(commit=False)
        q.author = request.user
        q.save()
        return redirect('index')
    return render(request, 'post_question.html', {'form': form})

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    form = AnswerForm(request.POST or None)
    if form.is_valid():
        ans = form.save(commit=False)
        ans.question = question
        ans.author = request.user
        ans.save()
        return redirect('question_detail', pk=pk)
    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.likes.add(request.user)
    return redirect('question_detail', pk=answer.question.id)
