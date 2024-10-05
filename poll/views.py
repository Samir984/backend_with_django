from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, Vote
from .forms import PollForm,UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
   polls=Poll.objects.all()
   context={"polls":polls}
   if request.user.is_authenticated:
      votes=Vote.objects.filter(user=request.user)
      context["user"]=request.user
      context["votes"]=votes
      
 
   return render(request,"index.html",context=context)

def create_poll(request):
   print(request.user)
   if not request.user.is_authenticated:
      print(request.user)
      return redirect("/login")
      
   poll_form =PollForm()
   if request.method=="POST":
      poll_form=PollForm(request.POST)
      if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.creater = request.user
            poll.save()
            return redirect("/")
   
   else:
        poll_form = PollForm()
        return render(request, 'create_poll.html', {'form': poll_form})



def edit_poll(request,poll_id):
   poll=get_object_or_404(Poll,pk=poll_id)
   if request.method=="POST":
         poll_form=PollForm(request.POST,instance=poll)
         if poll_form.is_valid():
               poll = poll_form.save(commit=False)
               poll.user = request.user
               poll.save()
               return redirect("/")
      
   else:
         poll_form = PollForm(instance=poll)
         return render(request, 'edit_poll.html', {'form': poll_form})

@login_required  
def delete_poll(request, poll_id):
    if request.method == "POST":
        poll = get_object_or_404(Poll, pk=poll_id)
        
       
    return redirect("/")


@login_required
def vote(request, poll_id):
    if request.method == 'POST':
        poll = get_object_or_404(Poll, id=poll_id)
        user = request.user
        option = int(request.POST.get('option'))

        # Check if the user has already voted on this poll
        if Vote.objects.filter(user=user, poll=poll).exists():
            messages.error(request, 'You have already voted.')
            return redirect("/")  # Adjust redirect URL as needed

        # Increment the appropriate vote count
        if option == 1:
            poll.vote_count_opt1 += 1
        elif option == 2:
            poll.vote_count_opt2 += 1
        elif option == 3 and poll.option_3:  # Ensure option_3 exists
            poll.vote_count_opt3 += 1
        elif option == 4 and poll.option_4:  # Ensure option_4 exists
            poll.vote_count_opt4 += 1

        poll.save()

        # Create a Vote record
        Vote.objects.create(user=user, poll=poll, selected_option=option)

        return redirect("/")

def register_view(request):   
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("enter")
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            # Add an error message if the form is not valid
            messages.error(request, 'There was an error with your registration. Please correct the errors below.')
         
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})
 
 
def login_view(request):
   if request.method == 'POST':
     username = request.POST.get('username')
     password = request.POST.get('password')
     user = authenticate(request, username=username, password=password)
     print(user)
     if user is not None:
         login(request, user)
         messages.success(request, 'You have successfully logged in!')
         return redirect('/')  # Redirect to home or another page
     else:
        messages.error(request, 'Invalid username or password')
   return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')