from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, Vote
from django.forms.models import model_to_dict
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
    print(poll_id)
    if request.method == "POST":
        poll = get_object_or_404(Poll, pk=poll_id)
        print(poll)
        poll.delete()
          
       
    return redirect("/")


@login_required
def vote(request, poll_id):
    if request.method == 'POST':
        poll = get_object_or_404(Poll, id=poll_id)
        user = request.user
        option = int(request.POST.get('option'))

        # Check if the user has already voted on this poll
        past_vote = Vote.objects.filter(user=user, poll=poll).first()

        if past_vote is not None:
            # User has already voted
            previous_option = past_vote.selected_option
            
            if previous_option == option:
                # User is unvoting by selecting the same option
                past_vote.delete()  # Remove the previous vote
                vote_count_attr = f'vote_count_opt{previous_option}'
                if hasattr(poll, vote_count_attr):
                    current_vote_count = getattr(poll, vote_count_attr)
                    setattr(poll, vote_count_attr, current_vote_count - 1)  # Decrement the vote count
            else:
                # User is changing their vote
                # Decrement the count for the previous option
                previous_vote_count_attr = f'vote_count_opt{previous_option}'
                if hasattr(poll, previous_vote_count_attr):
                    previous_vote_count = getattr(poll, previous_vote_count_attr)
                    setattr(poll, previous_vote_count_attr, previous_vote_count - 1)  # Decrement the previous option count

                # Update the vote record with the new option
                past_vote.selected_option = option
                past_vote.save()  # Save the updated vote

                # Increment the count for the new option
                vote_count_attr = f'vote_count_opt{option}'
                if hasattr(poll, vote_count_attr):
                    current_vote_count = getattr(poll, vote_count_attr)
                    setattr(poll, vote_count_attr, current_vote_count + 1)  # Increment the new option count
        else:
            # New vote
            Vote.objects.create(user=user, poll=poll, selected_option=option)
            vote_count_attr = f'vote_count_opt{option}'
            if hasattr(poll, vote_count_attr):
                current_vote_count = getattr(poll, vote_count_attr)
                setattr(poll, vote_count_attr, current_vote_count + 1)  # Increment the selected option count

        poll.save()  # Save the updated poll
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