from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import User, Textbook
from .forms import TextbookUploadForm
import requests
import os
import json


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST.get('first_name', '')
        email = request.POST.get('email', '')
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        grade_level = request.POST['grade_level']

        if password1 != password2:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'error': 'Username already taken'})

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            email=email,
            password=password1,
            grade_level=grade_level
        )
        login(request, user)
        return redirect('/dashboard/')

    return render(request, 'auth/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('Attempting login for:', username)
        user = authenticate(request, username=username, password=password)
        print('Authenticate result:', user)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        return render(request, 'auth/login.html', {'error': 'Invalid username or password'})

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def dashboard(request):
    textbooks = request.user.textbooks.all()
    return render(request, 'dashboard.html', {'textbooks': textbooks})


@login_required
def textbook_upload(request):
    if request.method == 'POST':
        form = TextbookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            textbook = form.save(commit=False)
            textbook.user = request.user
            textbook.save()
            messages.success(request, f'"{textbook.title}" uploaded successfully!')
            return redirect('dashboard')
    else:
        form = TextbookUploadForm()
    return render(request, 'textbook_upload.html', {'form': form})


@login_required
def textbook_reader(request, pk):
    textbook = get_object_or_404(Textbook, pk=pk, user=request.user)
    return render(request, 'textbook_reader.html', {'textbook': textbook})


@login_required
def textbook_delete(request, pk):
    textbook = get_object_or_404(Textbook, pk=pk, user=request.user)
    if request.method == 'POST':
        textbook.pdf_file.delete(save=False)
        textbook.delete()
        messages.success(request, f'"{textbook.title}" removed.')
    return redirect('dashboard')


@login_required
@require_POST
def chat(request):
    try:
        body = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    question = (body.get('question') or body.get('message') or '').strip()
    if not question:
        return JsonResponse({'error': 'No message provided'}, status=400)

    try:
        from agent.AIBrain.chat import ask_math_1050
        reply = ask_math_1050(question)
    except Exception:
        return JsonResponse({'error': 'Chat service unavailable'}, status=500)

    return JsonResponse({'reply': reply})


@login_required
@require_POST
def speak(request):
    body = json.loads(request.body)
    text = body.get('text', '')

    if not text:
        return JsonResponse({'error': 'No text provided'}, status=400)

    api_key  = os.environ.get('ELEVENLABS_API_KEY')
    voice_id = os.environ.get('ELEVENLABS_VOICE_ID')

    response = requests.post(
        f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}',
        headers={
            'xi-api-key': api_key,
            'Content-Type': 'application/json',
        },
        json={
            'text': text,
            'model_id': 'eleven_turbo_v2_5',
            'voice_settings': {
                'stability': 0.5,
                'similarity_boost': 0.75,
            }
        }
    )

    print('API KEY:', api_key)
    print('VOICE ID:', voice_id)

    if response.status_code != 200:
        print('ElevenLabs error:', response.status_code, response.text)
        return JsonResponse({'error': 'ElevenLabs error'}, status=500)
    return HttpResponse(response.content, content_type='audio/mpeg')