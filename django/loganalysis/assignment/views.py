from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Assignment, get_fuzzy_matches, create_form_from_object, summarize, get_vetter_matches
from .forms import AssignmentForm, FuzzForm

def index(request):
    """Fuzzy match approval"""
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            row = get_object_or_404(Assignment, pk=form.cleaned_data['query_id'])
            action = [k for k,v in request.POST.items() if k == v][0]
            row.take_action(action)
    matches = get_fuzzy_matches()
    matches = [(i, create_form_from_object(i, AssignmentForm)) for i in matches]
    context = {'matches': matches}
    return render(request, 'assignment/index.html', context)


def instructions(request):
    context = {"status":summarize()}
    return render(request, 'assignment/instructions.html', context)


def vetter(request):
    """Fuzzy match vetting"""
    if request.method == "POST":
        form = FuzzForm(request.POST)
        if form.is_valid():
            row = get_object_or_404(Assignment, pk=form.cleaned_data['query_id'])
            action = [k for k,v in request.POST.items() if k == v][0]
            row.take_vetting_action(action)
    matches = get_vetter_matches()
    matches = [(i, create_form_from_object(i, FuzzForm)) for i in matches]
    context = {'matches': matches}
    return render(request, 'assignment/vetter.html', context)
    

    
