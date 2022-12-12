from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# register user method

def register(request):
  if request.method == 'POST':
    # messages.error(request, 'Testing error messages')
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    #check if passwords match
    if password == password2:
      #check User
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')

      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('register')
        
        else:
          #Looks good
          user = User.objects.create_user(username=username, password=password, email=email,first_name=first_name, last_name=last_name )
          # login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now loged in')
          # return redirect(request, 'index')
          user.save();
          messages.success(request, 'You are now registered and can log in')
          return redirect('login')

    else:
      messages.error(request, 'password do not match')
      return redirect('register')
  else:  
    return render (request, 'accounts/register.html')
  

# login method

def login(request):
  if request.method == 'POST':
    # login User logic
    username = request.POST['username']
    password = request.POST['password']
    
    user = auth.authenticate(username = username, password = password)
    if user is not None:
      #means user is found in database
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('dashboard')

    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')

  else:
    return render (request, 'accounts/login.html')


# logout method

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now loged out')
    return redirect ('index')


# dashboard

def dashboard(request):
  user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id) 

  context={
    'contacts':user_contacts
  }
  return render (request, 'accounts/dashboard.html',context)
  
