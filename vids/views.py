from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Favorites, Video
from .forms import VideoForm, SearchForm
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
import urllib
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

YOUTUBE_API_KEY = 'AIzaSyDDUsTzkQhfzSl3ieb0kfjPheJnrNvflKo'

# Create your views here.


def home(request):
    recent_faves = Favorites.objects.all().order_by('-id')[:3]
    # popular_faves = [Favorites.objects.get(pk=6), Favorites.objects.get(pk=7)]
    return render(request, 'vids/home.html', {'recent_faves': recent_faves})


@login_required
def dashboard(request):
    favorites = Favorites.objects.filter(user=request.user)
    return render(request, 'vids/dashboard.html', {'favorites': favorites})


def full_list(request):
    favorites = Favorites.objects.all().order_by('-id')
    return render(request, 'vids/list.html', {'favorites': favorites})


@login_required
def add_video(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    faves = Favorites.objects.get(pk=pk)

    if not faves.user == request.user:
        raise Http404

    if request.method == 'POST':
        # Create
        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.favorites = faves
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(
                    f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('dashboard')
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a valid YouTube URL')

    return render(request, 'vids/add_video.html', {'form': form, 'search_form': search_form, 'faves': faves})


@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(
            search_form.cleaned_data['search_term'])
        response = requests.get(
            f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={YOUTUBE_API_KEY}')

        return JsonResponse(response.json())

    return JsonResponse({'error': 'Not able to validate form'})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateFaves(LoginRequiredMixin, generic.CreateView):
    model = Favorites
    fields = ['title']
    template_name = 'vids/create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateFaves, self).form_valid(form)
        return redirect('dashboard')


class DetailFaves(generic.DetailView):
    model = Favorites
    template_name = 'vids/detail.html'


class UpdateFaves(LoginRequiredMixin, generic.UpdateView):
    model = Favorites
    template_name = 'vids/update_faves.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        favorites = super(UpdateFaves, self).get_object()
        if not favorites.user == self.request.user:
            raise Http404
        return favorites


class DeleteFaves(LoginRequiredMixin, generic.DeleteView):
    model = Favorites
    template_name = 'vids/delete_faves.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        favorites = super(DeleteFaves, self).get_object()
        if not favorites.user == self.request.user:
            raise Http404
        return favorites


class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'vids/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        print(video)
        if not video.favorites.user == self.request.user:
            raise Http404
        return video
