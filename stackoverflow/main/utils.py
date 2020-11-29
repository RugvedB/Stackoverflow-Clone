from .models import Tags, Questions, Answer
from userauth.models import StackoverflowUser
from django.db.models import Count,Q


def reputation(booleanval, rate, ques_obj):
    if booleanval == False:
        userrepu = ques_obj.author
    else:
        userrepu = ques_obj.answered_by

    userrepu.reputation_score += rate
    userrepu.save()

def performUpDownVote(user,isQuestion,id,action_type):
    id = int(id)
    flag = False
    if isQuestion == 'True':
        print('------> isQ')
        q = Questions.objects.get(pk = id)
        if q.author == user:
            return False
    else:
        print('------> isNotQ')
        flag=True
        q = Answer.objects.get(pk = id)
        if q.answered_by == user:
            return False

    existsInUpvote = True if user in q.upvotes.all() else False
    existsDownUpvote = True if user in q.downvotes.all() else False
    if existsInUpvote:
        if action_type == 'downvote':
            q.upvotes.remove(user)
            q.downvotes.add(user)
            reputation(flag,-20, q)
            q.votes = q.votes - 2
    elif existsDownUpvote:
        if action_type == 'upvote':
            q.downvotes.remove(user)
            q.upvotes.add(user)
            reputation(flag,20, q)
            q.votes = q.votes + 2
    else:
        if action_type == 'downvote':
            q.downvotes.add(user)
            reputation(flag,-10, q)
            q.votes = q.votes - 1
        if action_type == 'upvote':
            q.upvotes.add(user)
            reputation(flag,10, q)
            q.votes = q.votes + 1
    q.save()
    return True