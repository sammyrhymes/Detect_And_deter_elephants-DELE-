from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.http import urlencode
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SignupForm, LoginForm
from django.core.mail import send_mail
from django.http import HttpResponse


# from .models import Tournament, UserProfile


class LoginView(View):

    template_name = 'dashboard/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard:list_tournaments')  
        return render(request, self.template_name, {'error': 'Invalid login credentials'})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('dashboard:login') 


class SignupView(View):
    template_name = 'dashboard/signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return redirect('dashboard:signup')

            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('dashboard:login')
        else:
            form = SignupForm()
            return redirect(request.path, {'form' : form, 'error':'invalid credentials'})

class HomeView(LoginRequiredMixin,View):

    template_name = 'dashboard/list_tournaments.html'
    login_url  = 'dashboard:login'

    def get(self, request): 
        return render(request, self.template_name, { 'title': 'home'})

def send_email(request):
    if request.method == 'POST':
        subject = 'notification module success'
        message = 'Congratulations! your notification module works.'
        from_email = 'xrt5996@gmail.com'  # Change this to your email address
        to_email = ['virtualprey@gmail.com']  # Change this to the recipient's email address
        send_mail(subject, message, from_email, to_email, fail_silently=False)
        return HttpResponse('Email sent successfully!')
    else:
        return render(request, 'dashboard/list_tournaments.html')  # Replace 'your_template.html' with the template containing your button




# class CreateTournament(LoginRequiredMixin,View):

#     template_name = 'tournaments/create_tournaments.html'
#     login_url  = 'tournaments:login'

#     def get(self, request):   
#         form = TournamentForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = TournamentForm(request.POST, request.FILES)
#         if form.is_valid():
#             tournament = form.save(commit=False)
#             tournament.organizer = request.user
#             tournament.save()
#             return redirect('tournaments:list_tournaments')
#         error = "invalid form"
#         return redirect('tournaments:create_tournament', {'error':error})




# class View_Tournament( LoginRequiredMixin,View):

#     template_name = 'tournaments/view_tournament.html'
#     login_url  = 'tournaments:login'

#     def get(self, request, id):
#         tournament = get_object_or_404(Tournament, id=id)
#         user = request.user
#         is_participant = tournament.participants.filter(id=user.id).exists()
#         return render(request, self.template_name, {'tournament': tournament, 'is_participant': is_participant})

#     def post(self, request, id):
#         tournament = get_object_or_404(Tournament, id=id)
#         user = request.user
#         action = request.POST.get('action')

#         if action == 'join':
#             tournament.participants.add(user)
#         elif action == 'leave':
#             tournament.participants.remove(user)

#         return redirect('tournaments:list_tournaments')

# class EditTournament( UserPassesTestMixin,View):
    
#     template_name = 'tournaments/edit_tournament.html'
#     login_url  = 'tournaments:login'
    
#     def test_func(self):
#         tournament = get_object_or_404(Tournament, id=self.kwargs['id'])
#         return self.request.user == tournament.organizer
    
#     def handle_no_permission(self):
#         messages.error(self.request, "You don't have permission to edit this tournament.")
#         return redirect('tournaments:no_permission') 

#     def get(self, request, id):
#         tournament = get_object_or_404(Tournament, id=id)
#         form = TournamentForm(instance=tournament)
#         return render(request, self.template_name, {'form': form, 'tournament': tournament})

#     def post(self, request, id):
#         tournament = get_object_or_404(Tournament, id=id)
#         form = TournamentForm(request.POST, request.FILES , instance=tournament,)
#         if form.is_valid():
#             form.save()
#             return redirect('tournaments:view_tournament', id=id)
        
# class NoPermission(View):

#     template_name = 'tournaments/no_permission.html'

#     def get(self, request):
#         return render(request, self.template_name)
    
# class DeleteTournament(UserPassesTestMixin, View):
    
#     template_name = 'tournaments/delete_tournament.html'

#     def test_func(self):
#         tournament = get_object_or_404(Tournament, id=self.kwargs['id'])
#         return self.request.user == tournament.organizer
    
#     def handle_no_permission(self):
#         messages.error(self.request, "You don't have permission to edit this tournament.")
#         return redirect('tournaments:no_permission') 

#     def get(self, request, id):
#         tournament = get_object_or_404(Tournament, id=id)
#         return render(request, self.template_name, {'tournament': tournament})

#     def post(self, request, id):
#         tournament = get_object_or_404(Tournament, id=id)
#         tournament.delete()
#         return redirect('tournaments:list_tournaments')
    
# class ParticipatingTournaments(LoginRequiredMixin,View):

#     template_name = 'tournaments/participating_tournaments.html'
#     login_url  = 'tournaments:login'

#     def get(self, request):

#         tournaments = Tournament.objects.filter(participants=request.user)
#         participants = Tournament.participants

#         context = {'tournaments': tournaments, 'participants':participants}
#         return render(request, self.template_name, context)
    
# class Index(View):
#     template_name = 'tournaments/index.html'

#     def get(self, request):
#         return render(request, self.template_name)
    


# class MyTournaments(LoginRequiredMixin, View):
#     template_name = 'tournaments/mytournaments.html'
#     login_url = 'tournament:login'

#     def get(self, request):
#         tournaments = Tournament.objects.filter(organizer=request.user)
#         return render(request, self.template_name, {'tournaments': tournaments})

# class Participants(LoginRequiredMixin, View):

#     template_name = 'tournaments/participants.html'
#     login_url = 'tournament:login'

#     def get(self, request, tournament_id):
#         tournament = get_object_or_404(Tournament, id=tournament_id)
#         return render(request, 'tournaments/participants.html', {'tournament': tournament})
    
# class UserProfileView(LoginRequiredMixin, View):
#     template_name = 'user_profile.html'

#     def get(self, request, *args, **kwargs):
#         user_profile = UserProfile.objects.get(user=request.user)
#         return render(request, self.template_name, {'user_profile': user_profile})

# class EditUserProfile(UserPassesTestMixin, View):
#     model = UserProfile
#     form_class = UserProfile
#     template_name = 'edit_user_profile.html'
#     success_url = reverse_lazy('user_profile')

#     def get_object(self, queryset=None):
#         return self.model.objects.get(user=self.request.user)

