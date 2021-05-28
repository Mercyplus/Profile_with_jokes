from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
import requests
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Jokes


def home(request):
    return render(request, 'home.html')


def user_login(request):
    # авторизация пользователя
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Учетная запись отключена')
            else:
                return redirect('signup')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    # регистрация пользователя
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создает новый объект пользователя, но пока не сохраняет его
            new_user = user_form.save(commit=False)
            # Устанавливает выбранный пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняет объект пользователя
            new_user.save()
            # при создании нового пользователя, создается пустой профиль
            profile = Profile.objects.create(user=new_user)
            return render(request, 'register_done.html', {'new_user': new_user, 'profile': profile})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def signoutView(request):
    # выход пользователя
    logout(request)
    return redirect('home')


@login_required
def edit(request):
    # получаем все шутки текущего пользователя из бд
    jokes = Jokes.objects.filter(joke=request.user)
    if request.method == 'POST':
        # если была нажата кнопка generate, то генерируется случайная шутка
        if request.POST.get('generate'):
            joke = requests.get('https://geek-jokes.sameerkumar.website/api')
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)

            return render(request, 'edit.html', {'joke': joke.text,
                                                 'user_form': user_form,
                                                 'profile_form': profile_form})
        # если была нажата кнопка save, то обновленные настройки профиля сохраняются в бд
        if request.POST.get('save'):
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
            # если формы валидны, то они сохраняются в бд
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('home')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form, 'jokes': jokes})
