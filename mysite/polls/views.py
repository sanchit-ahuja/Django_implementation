# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import View
from django.utils import timezone
from django.contrib.auth import authenticate
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect,HttpRequest
from .models import Choice, Question
from django.contrib.auth.decorators import login_required
from .forms import UserForm

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
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

    #return Question.objects.filter(pub_date__lte=timezone.now())
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
def register(request):
    if request.method=='POST':
        form =UserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['passsword']
            user.set_passsword(password)
            user.save()
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('polls:index')
        else:
            form=UserForm()
    return render(request,'polls/register.html',{'form':form})