from django.shortcuts import render
from .models import *
from userauth.models import *
from django.db import transaction
from django.db.models import Count
# Create your views here.


def questions(request):
    all_questions = Questions.objects.all()
    return render(request, 'main/questions.html',{'all_questions':all_questions})

def questionsingle(request, pk):
    user = StackoverflowUser.objects.get(pk=1)
    q = Questions.objects.get(pk = pk)
    if request.method == 'POST':
        questiontaken = request.POST.dict()
        answer = questiontaken.get('editor1') # Answer content
        a = Answer(ans_content=answer, answered_by=user, question_to_ans = q)
        a.save()
        q.answers.add(a)
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

def profile(request):
    return render(request, 'main/profile.html')