from django.shortcuts import render,redirect
from .models import *
from userauth.models import *
from django.db import transaction
from django.db.models import Count,Q
# Create your views here.


def performUpDownVote(user,isQuestion,id,action_type):
    id = int(id)
    if isQuestion == 'True':
        print('------> isQ')
        q = Questions.objects.get(pk = id)
    else:
        print('------> isNotQ')
        q = Answer.objects.get(pk = id)

    existsInUpvote = True if user in q.upvotes.all() else False
    existsDownUpvote = True if user in q.downvotes.all() else False
    if existsInUpvote:
        if action_type == 'downvote':
            q.upvotes.remove(user)
            q.downvotes.add(user)
            q.votes = q.votes - 2
    elif existsDownUpvote:
        if action_type == 'upvote':
            q.downvotes.remove(user)
            q.upvotes.add(user)
            q.votes = q.votes + 2
    else:
        if action_type == 'downvote':
            q.downvotes.add(user)
            q.votes = q.votes - 1
        if action_type == 'upvote':
            q.upvotes.add(user)
            q.votes = q.votes + 1
    q.save()
    

def questions(request):
    main_query = Questions.objects
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

def questionsingle(request, pk):
    user = StackoverflowUser.objects.get(pk=1)
    if request.GET and request.GET['isQuestion'] and request.GET['id'] and request.GET['action_type']:
        performUpDownVote(user,request.GET['isQuestion'],request.GET['id'],request.GET['action_type'])
        return redirect('/question/'+str(pk))

    
    q = Questions.objects.get(pk = pk)
    if request.method == 'POST':
        questiontaken = request.POST.dict()
        answer = questiontaken.get('editor1') # Answer content
        a = Answer(ans_content=answer, answered_by=user, question_to_ans = q)
        a.save()
        q.answers.add(a)
    q.views = q.views + 1
    q.save()
    return render(request, 'main/question-single.html',{'q':q })

def askquestion(request):
    user = StackoverflowUser.objects.get(pk=1)
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
            print(a)
            a.save()

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

# def upvote(request,type,question_id):
#     pass

# def downvote(request,type,question_id):
#     pass

def profile(request):
    return render(request, 'main/profile.html')