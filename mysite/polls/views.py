# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views import generic
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
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

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'