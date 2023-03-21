from django.shortcuts import render,HttpResponse,redirect
from ChatRoom.models import Topic
from django.db.models import Q                
from blogsite.app import WEB_SITE_NAME,ACTIVE
from blogsite.helper import slugify,NotAllowed
from django.contrib.auth.decorators import login_required
from .models import Post,Post_Message
from .form import PostForm
# Create your views here.

def tutorial(request):
    page = "tutorial"
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    title = f'{WEB_SITE_NAME}-Our Exclusive Tutorials'
    # get all topics
    topics = Topic.objects.all()
    new_topics=[]
    limit = 8
    i = 0
    for topic in topics:
        if i< limit:
            new_topics.append(topic)
        i += 1
    topic_count = topics.count()
    posts = Post.objects.filter(
        # if topic contain q get the post
        Q(topic__name__icontains=q) | 
        #title contain q get the post
        Q(title__icontains=q) | 
        # if content contain q get the post
        Q(content__icontains=q)
    )
    current_topic =  q
    flug = 0
    if q != "" and posts.count() > 0:
        for post in posts:
            if flug == 0:
                current_topic = post.topic
            elif post.topic == current_topic:
                flug += 1
    print(f"courrent topic: {current_topic}")   
    post_messages = Post_Message.objects.all()
    if q  == "":
        btn="activity"
        right_components = "Tutorial/activity_component.html"
    else:
        btn = "tutorial"
        right_components = "Tutorial/topic_content_component.html"
    
    context = {
        'title':title,
        'btn':btn,
        'page':page,
        'current_topic':current_topic,
        'tutorial_active':ACTIVE,
        'right_components':right_components,
        'topic_count': topic_count,
        'topics': new_topics, 
        'posts': posts,
        'post_messages': post_messages,
        }

    return render(request,'Tutorial/posts.html', context)

def post(request,pk,title):
    page = "tutorial",
    
    post = Post.objects.get(id=pk)
    #increment view count
    if post.view is None:
        post.view = 1
    else:
        post.view += 1
    #save post to database
    post.save()
    all_similar_posts = Post.objects.filter(topic=post.topic).order_by('created')
    
    web_title = f"{WEB_SITE_NAME}-{post.title}"
    if post.slug != title:
        return redirect('post',pk=pk,title=post.slug)
    if request.method == 'POST':
        message = Post_Message.objects.create(
            user= request.user,
            post=post,
            body=request.POST.get('body')
        )
        message.save()
        return redirect('post',pk=post.id,title=post.slug)
    post_messages = post.post_message_set.all()
    context ={
        "title": web_title,
        'page':page,
        "post": post,
        "post_messages": post_messages,
        "all_similar_posts": all_similar_posts,
    }
    return render(request, 'Tutorial/post.html',context=context)
    
def all_tutorial(request):
    page = 'tutorial'
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    web_title = f"{WEB_SITE_NAME}-All Topic"
    context = {
        'page': page,
        'title':web_title,
        'topics': topics,
    }
    return render(request, 'Tutorial/topics.html',context)
@login_required(login_url='login')
def createPost(request):
    page = 'tutorial'
    web_title = f"{WEB_SITE_NAME}-Create A Tutorial"
    form = PostForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        topic_name = request.POST.get('topic')
        #get or create a new topic
        topic,created = Topic.objects.get_or_create(name=topic_name)
        post=Post.objects.create(
            host=request.user,
            topic=topic,
            cover_img_id = request.POST.get('cover_img_id'),
            title=request.POST.get('title'),
            content = request.POST.get('content'),
            video=request.POST.get('video') if request.POST.get('video') != None else "",
            slug= slugify(request.POST.get('title'))
        )
        id = post.pk
        
        return redirect('post',pk=id,title=post.slug)
    context = {
        'page':page,
        'title':web_title,
        'form':form,
        'topics':topics
    }
    return render(request,'Tutorial/post_form.html',context)

@login_required(login_url='login')
def updatePost(request,pk,title):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    topics = Topic.objects.all()
    if request.user != post.host:
        return NotAllowed(request)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        post.title = request.POST.get('title')
        post.slug = slugify(post.title)
        post.topic = topic
        post.cover_img_id = request.POST.get('cover_img_id')
        post.content = request.POST.get('content')
        post.video = request.POST.get('video')
        post.save()
        return redirect('post',pk=post.pk, title=post.slug)
    
    context = {
        'page':'tutorial',
        "title":f"{WEB_SITE_NAME}-Update Post ",
        'form': form,
        'topics':topics,
        }
    return render(request, 'Tutorial/post_form.html',context)


@login_required(login_url='login')
def deletePost(request, pk,title):
    post = Post.objects.get(id=pk)
    context = {
        'obj': post.title,
        'page':'tutorial',
        'title':f"{WEB_SITE_NAME} - Delete Post"
        }
    if request.user != post.host:
        return NotAllowed(request)
    if request.method == 'POST':
        post.delete()
        return redirect("tutorial")

    return render(request, 'ChatRoom/delete.html',context)
@login_required(login_url='login')
def deletePostMessage(request, pk):
    message = Post_Message.objects.get(id=pk)

    post = message.post
    if request.user != message.user:
        return NotAllowed(request)
    if request.method == 'POST':
        message.delete()
        return redirect('post',pk=post.id,title=post.slug)
    context = {
        'obj': message,
        'page':'tutorial',
        'title':f"{WEB_SITE_NAME} - Delete Message",
        }
    return render(request, 'ChatRoom/delete.html', context)


def activityPage(request):
    post_messages = Post_Message.objects.all()
    context = {
        'page':"tutorial",
        'title':f"{WEB_SITE_NAME}-Post Activity",
        'post_messages': post_messages
        }
    return render(request, 'Tutorial/activity.html', context)

def ContentTopic(request,topic_name):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q != "":
        posts = Post.objects.filter(Q(title__icontains=q) | Q(slug__icontains=q)|Q(content__icontains=q))
    else:
        posts = Post.objects.filter(Q(topic__name__icontains=topic_name))
    
    context = {
        'page':"tutorial",
        'topic':topic_name,
        'title':f"{WEB_SITE_NAME}-{topic_name} Content",
        'posts': posts
        }
    return render(request, 'Tutorial/tutorial_content.html',context)