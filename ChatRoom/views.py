from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.mail import send_mail,BadHeaderError
from blogsite.app import WEB_SITE_NAME
import uuid
from .models import Room, Topic, Message, User,Contact
from django.db.models import Q
from .forms import RoomForm, UserForm, MyUserCreationForm,ContactForm,RecoveryForm,PassCodeForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from blogsite.app import ACTIVE
from blogsite.settings import EMAIL_HOST_USER
from blogsite.helper import get_or_none

import random
from blogsite.helper import NotAllowed
def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User not found.')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username Or Password does not exist.')
    context = {'page': page}
    return render(request, 'ChatRoom/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    context = {'page': page, 'form': form}
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # clean up data
            user.username = user.username.lower()
            # save user
            user.save()
            #login new user
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during Registration')
    return render(request, 'ChatRoom/login_register.html', context)


def home(request):
    # select all room from table
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(
            name__icontains=q) | Q(description__icontains=q)
    )
    #topic__name__icontains icontains means match python in case of py pyt and case insensitive
    topics = Topic.objects.all()
    new_topics = []
    limit = 5
    i = 0
    for topic in topics:
        if i < limit:
            new_topics.append(topic)
        i += 1
    topic_count = topics.count()
    # count room
    room_count = rooms.count()
    #room messages
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': new_topics,
               'chat_active':ACTIVE,
               "topic_count":topic_count,
               "room_count": room_count, "room_messages": room_messages}
    return render(request, 'ChatRoom/home.html', context)


def room(request, pk):
    # select specific room from table
    room = Room.objects.get(id=pk)
    #query in message of specific room by parentTable.childTable_set.all()
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
        else:
            return redirect('login')
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {"room": room, "room_messages": room_messages,
               "participants": participants}
    return render(request, 'ChatRoom/room.html', context)
# user profile view


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    # get all the room of the user
    #through parent table user from room table
    rooms = user.room_set.all()
    #rooms messages
    room_messages = user.message_set.all()
    #all topics
    topics = Topic.objects.all()
    context = {'user': user, "rooms": rooms,
               "room_messages": room_messages, "topics": topics}
    return render(request, 'ChatRoom/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
       form = RoomForm(request.POST)
       #get topic from the request
       topic_name = request.POST.get('topic')
       # get or create a new topic
       topic, created = Topic.objects.get_or_create(name=topic_name)
       Room.objects.create(
           host=request.user,
           topic=topic,
           name=request.POST.get('name'),
           description=request.POST.get('description')
       )
       return redirect('home')
    context = {"form": form, "topics": topics}
    return render(request, 'ChatRoom/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    #form is initaly filed with room data
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return NotAllowed(request)
    if request.method == 'POST':
        # instance = Room means specific Room value will be updated
        # form = RoomForm(request.POST,instance=room)
        #get topic from the request
        topic_name = request.POST.get('topic')
        # get or create a new topic
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {"form": form, "topics": topics, 'room': room}
    return render(request, 'ChatRoom/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return NotAllowed(request)
    if request.method == 'POST':
        room.delete()
        return redirect("home")

    return render(request, 'ChatRoom/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        message.delete()
        return redirect("home")

    return render(request, 'ChatRoom/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile', pk=user.id)
    context = {'form': form}
    return render(request, 'ChatRoom/update_user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics": topics}
    return render(request, 'ChatRoom/topics.html', context)


def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'ChatRoom/activity.html', context)
def contactPage(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Contact.objects.create(
                name = request.POST.get('name'),
                email = request.POST.get('email'),
                body =request.POST.get('body')
            )
            return redirect('home')
    context ={
        'form': form,
        'title': f"{WEB_SITE_NAME} - Contact Page",
        'contact_active':ACTIVE
        
    }
    return render(request, 'ChatRoom/contact.html', context)

def forget(request):
    form = RecoveryForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_or_none(User, email=email)
        
        if user == None:
            messages.info(request,"User is not Exists")
            return redirect('forget')
        token = uuid.uuid4()
        code = random.randint(55555,9999999)
        request.session[f'{token}'] = code
        request.session[f'{token}-email'] = user.email
        subject = "Verification Code"
        message = f"Verification Code is {code}"
        try:
            send_mail(subject, message,EMAIL_HOST_USER,[email])
        except BadHeaderError:
            messages.error(request, 'Email is invalid')
            return redirect('forget')
        
        
        messages.success(request,"An email has been sent to your email.")
        return HttpResponseRedirect(f'/verify/?token={token}')
    context = {
        "form": form,
        "title":f'{WEB_SITE_NAME} - Recovery'
    }
    return render(request, 'ChatRoom/forget.html',context)
def verify(request):
    token = request.GET.get('token')
    if request.method == 'POST':
        code = int(request.POST.get('code'))
        if code == request.session.get(token):
            return HttpResponseRedirect(f"/update/passcode/?token={token}")
        
    context = {
                "title":f"{WEB_SITE_NAME}-Verify Code "
            }

    return render(request, 'ChatRoom/code.html',context)
def update_passcode(request):
    token = request.GET.get('token')
    
    form = PassCodeForm()
    if request.method == 'POST':
        email = request.session.get(f'{token}-email','')
        user = get_or_none(User, email=email)
        if user is not None:
            form = PassCodeForm(request.POST,instance=user)
            if form.is_valid():
                print("i am in if")
                form.save()
                #new user 
                # user = User.objects.get(id = user.id)
                login(request, user)
                return redirect('home')
                
    context = {
        "title":f"{WEB_SITE_NAME}-New Password",
        "form": form
    }
    return render(request,"ChatRoom/update_passcode.html",context)
    
    
