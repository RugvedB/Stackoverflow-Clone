from django.shortcuts import render,redirect
from .models import Tags, Questions, Answer
from userauth.models import StackoverflowUser
from django.db import transaction
from django.db.models import Count,Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import reputation, performUpDownVote
from django.core.paginator import Paginator
# Create your views here.

  
def questions(request):
    main_query = Questions.objects
    if request.GET and ('q' in request.GET) and request.GET['q'] == 'mostviewed':
        all_questions = main_query.all().order_by('-views')
        marked = 'mostviewed'
    elif request.GET and ('q' in request.GET) and request.GET['q'] == 'unanswered':
        all_questions = main_query.filter(is_answered = False).order_by('-created_at')
        marked = 'unanswered'
    else:
        marked = 'latest'
        all_questions = main_query.all().order_by('-created_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(all_questions, 5)
    try:
        all_questions = paginator.page(page)
    # except EmptyPage:
    #     all_questions = paginator.page(paginator.num_pages)
    except Exception as e:
        all_questions = paginator.page(1)
    
    return render(request, 'main/questions.html',{'all_questions':all_questions,'marked' : marked})

@login_required
def questionsingle(request, pk):
    # user = StackoverflowUser.objects.get(pk=1)
    user = request.user
    try:
        if request.GET and request.GET['isQuestion'] and request.GET['id'] and request.GET['action_type']:
            result = performUpDownVote(user,request.GET['isQuestion'],request.GET['id'],request.GET['action_type'])
            redirect_to = '/question/'+str(pk)
            if 'page' in request.GET:
                redirect_to += '?page='+request.GET['page']
            if result == True:
                messages.success(request, 'Action successful')
            else:
                messages.error(request, 'Invalid Action')
            return redirect(redirect_to)
    except Exception:
        pass
    
    q = Questions.objects.get(pk = pk)
    if request.method == 'POST':
        questiontaken = request.POST.dict()
        answer = questiontaken.get('editor1') # Answer content
        a = Answer(ans_content=answer, answered_by=user, question_to_ans = q)
        a.save()
        q.answers.add(a)
        messages.success(request, 'Answer posted successfully')
    q.views = q.views + 1
    q.save()

    if q.author == user:
        showaccept = True
    else:
        showaccept = False

    # Pagination
    all_answers = q.answers.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_answers, 5)
    try:
        all_answers = paginator.page(page)
    except PageNotAnInteger:
        all_answers = paginator.page(1)
    except EmptyPage:
        all_answers = paginator.page(paginator.num_pages)

    
    return render(request, 'main/question-single.html',{'q':q,'all_answers':all_answers,'showaccept': showaccept })

@login_required
def askquestion(request):
    user = request.user
    print(user)
    if request.method == 'POST':
        questiontaken = request.POST.dict()
        title = questiontaken.get('title')
        content = questiontaken.get('queseditor')
        tags = questiontaken.get('tags')
        selfanswer = questiontaken.get('selfanswereditor')

      
        q = Questions(title=title, ques_content = content, author = user)
        if selfanswer != '':
            q.is_answered = True
        q.save()
        all_tags = tags.split(',')
       
        for a in all_tags:
            try:
                t = Tags.objects.get(tag_word = a)
                q.tags.add(t)
            except Exception:
                q.tags.create(tag_word = a)

            q.save()

        if selfanswer != '':     
            a = Answer(ans_content=selfanswer, answered_by=user, question_to_ans = q)
            a.is_accepted = True
            print(a)
            a.save()
            q.answers.add(a)
            q.has_accepted_answer = True
            
            q.save()
            user.ans_given.add(a)
        user.ques_asked.add(q)
        user.save()

        messages.success(request, 'Question posted successfully')
        
        return redirect('name_questionsingle',pk=q.pk)
    return render(request, 'main/askquestion.html')


def questionByTag(request,tag_word):
    main_query = Questions.objects.filter(Q(tags__tag_word__iexact = tag_word))

    if request.GET and request.GET['q'] == 'mostviewed':
        all_questions = main_query.all().order_by('-views')
        marked = 'mostviewed'
    elif request.GET and  request.GET['q'] == 'unanswered':
        all_questions = main_query.filter(is_answered = False)
        marked = 'unanswered'
    else:
        marked = 'latest'
        all_questions = main_query.all().order_by('-created_at')

    
    return render(request, 'main/questions.html',{'all_questions':all_questions,'marked' : marked})

@login_required
def profile(request, username):
    seeuser = StackoverflowUser.objects.get(username=username)
    showeditbutton = True if seeuser == request.user else False
    userques = Questions.objects.filter(author = seeuser).order_by('-created_at')
    ansgiven = Answer.objects.filter(answered_by = seeuser).order_by('-created_at')

    return render(request, 'main/profile.html',{'seeuser':seeuser, 'showeditbutton': showeditbutton, 'userques': userques, 'ansgiven': ansgiven})


@login_required
def is_accepted(request, pk, pk2):
    q = Questions.objects.get(pk = pk)
    a = Answer.objects.get(pk = pk2)

    q.has_accepted_answer = True
    q.save()

    a.is_accepted = True
    a.save()

    if q.author == request.user:
        showaccept = True
    else:
        showaccept = False

    # Pagination
    all_answers = q.answers.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_answers, 5)
    try:
        all_answers = paginator.page(page)
    except PageNotAnInteger:
        all_answers = paginator.page(1)
    except EmptyPage:
        all_answers = paginator.page(paginator.num_pages)

    return render(request, 'main/question-single.html',{'q':q,'all_answers':all_answers,'showaccept': showaccept })