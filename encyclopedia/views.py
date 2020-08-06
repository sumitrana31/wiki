from django.shortcuts import render
import markdown2
from django.http import HttpResponse, HttpResponseRedirect
from . import util
from django import forms
from django.urls import reverse
import random



class SearchForm(forms.Form):
    search_form = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia"}) )

class NewEntry(forms.Form):
    title = forms.CharField(label="Title:",widget=forms.TextInput(attrs={"placeholder": "Enter Title"}))
    content = forms.CharField(label="Content:", widget=forms.Textarea(attrs={"class": 'entry_textarea',"placeholder": "Enter Markdown Content."}))

class PreContent(forms.Form):
    populated_form = forms.CharField(label="Edit:" ,widget=forms.Textarea(attrs={"class": 'edit_textarea'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
    })


def entry(request, title):
    content = util.get_entry(title)
    if title in util.list_entries():
        if request.method == 'GET':
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": markdown2.markdown(content),
                "form": SearchForm(),
                "md_file": util.get_entry(title)
            })
        else:
            if request.method == 'POST':
                updated_content = request.POST.get("textarea01")
                util.save_entry(title, updated_content)
                return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": markdown2.markdown(updated_content),
                "form": SearchForm(),
                "md_file": util.get_entry(title)
            })
    else:
        return render(request, "encyclopedia/error.html")


def search(request):
    if request.method == 'POST':
        submitted_data = SearchForm(request.POST)
        if submitted_data.is_valid():
            submitted_data_cleaned = submitted_data.cleaned_data["search_form"]
            if submitted_data_cleaned in util.list_entries():
                return HttpResponseRedirect(f"/wiki/{submitted_data_cleaned}")
            else:
                return render(request, "encyclopedia/search.html", {
                    'q': submitted_data_cleaned,
                    'entries': util.list_entries(),
                    "form": SearchForm(),
                })


def new_entry(request):
    if request.method == 'POST':
        submitted_data = NewEntry(request.POST)
        if submitted_data.is_valid():
            title = submitted_data.cleaned_data["title"]
            content = submitted_data.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/entry_error.html")
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
    else:
        return render(request, "encyclopedia/new_entry.html", {
            "form1" : NewEntry(),
            "form": SearchForm(),      
        })
        

def edit_entry(request):
    if request.method == 'POST':
        content = request.POST.get("initial-value")
        title = request.POST.get("ini_title")
        return render(request, "encyclopedia/edit_entry.html", {
            "form3": content,
            "form": SearchForm(),
            "title": title
                
            })



def random_entry(request):
    if request.method == 'GET':
        content = request.GET.get("initial-value")
        random_page = random.choice(util.list_entries())
        return render(request, "encyclopedia/title.html", {
            "title": random_page,
            "content": markdown2.markdown(util.get_entry(random_page)),
            "form": SearchForm(),
            "form3": content,
            "md_file": util.get_entry(random_page)
            })


