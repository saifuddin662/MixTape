from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from .models import Album, Song
from .form import UserForm, LoginForm
from django.conf import settings


class IndexView(LoginRequiredMixin, generic.ListView):
    model = Album
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(user=user)


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

    # Use this method to relate created data with Current User

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AlbumCreate, self).form_valid(form)


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class SongView(LoginRequiredMixin, generic.ListView):
    template_name = 'music/songs.html'
    context_object_name = 'all_songs'

    def get_queryset(self):
        user = self.request.user
        return Song.objects.filter(user)


class SongCreate(LoginRequiredMixin, CreateView):
    model = Song
    fields = ['song_title', 'audio_file']

    def form_valid(self, form):
        form.instance.album = self.request.album
        return super(SongCreate, self).form_valid(form)


class SongDelete(LoginRequiredMixin, DeleteView):
    model = Song
    success_url = reverse_lazy('music:detail')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            user = authenticate(request, username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'music/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if self.request.user.is_active:
            return redirect('music:index')
        else:
            form = self.form_class(request.POST)

            if form.is_valid():

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(request, username=username, password=password)

                if user is not None:

                    if user.is_active:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        return redirect('music:index')
                    else:
                        return render(request, self.template_name, {'error_message': 'Your account has been disabled'})

            return render(request, self.template_name, {'form': form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('music:login_user')





























