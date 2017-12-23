# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect,HttpRequest
from .models import Choice, Question

class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'
def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,
        'error_message':'You didnt select a choice'},)
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))
def index(request):
    latest_question_list=Question.objects.order_by('pub_date')[:5]
    num_visits=request.session.get('num_visits',0)
    request.session['num_visits']=num_visits+1
    context={'latest_question_list':latest_question_list,'num_visits':num_visits}
    return render(request,'polls/index.html',context)

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'