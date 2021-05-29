from django.shortcuts import render , HttpResponse,redirect
from home.models import Contact
from django.contrib import  messages
from blog.models import Post
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
#HTML pages
def home(request):
    return render(request,'home/home.html')

def about(request):
    return render(request,'home/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<2  or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content = content)
            contact.save()
            messages.success(request,'Your message has been successfully sent')
    
    return render(request,'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allposts = allPostsTitle.union(allPostsContent)
    if allposts.count() == 0:
        messages.warning(request,'No search results found. please refine your query')

    params ={'allposts': allposts, 'query':query}
    return render(request,'home/search.html',params)

# Authentication APIS
def handlesignup(request):
        if request.method == 'POST':
            #Get the post parameters
            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            
            # check for errorneous inputs
            if len(username) > 10:
                messages.error(request, "Username must be under 10 characters")
                return redirect('home')

            # username should be alphanumeric
            if not username.isalnum():
                messages.error(request, "Username should only contains letters and numbers")
                return redirect('home')
            
            # passwords should match  
            if pass1 != pass2:
                messages.error(request, "password does not match")
                return redirect('home')

            #create the user    
            myuser = User.objects.create_user(username,email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your BlogFriends account has been successfully created")
            return redirect('home')
        else:
            return HttpResponse('404-Not found')    

def handlelogin(request):
        if request.method == 'POST':
            loginusername = request.POST['loginusername']
            loginpassword = request.POST['loginpassword']
            user = authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('home')

        return HttpResponse('404 - Not Found')        

def handlelogout(request):
            logout(request)
            messages.success(request,"Successfully Logged Out")
            return redirect('home')
            return HttpResponse('logout')        
