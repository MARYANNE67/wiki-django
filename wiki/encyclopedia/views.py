from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown
from . import util
import random

def index(request):
    return render(request, "index.html", {
        "entries": util.list_entries()
    })

#convert md to html using markup   
def convert_md(title):
    md_file = util.get_entry(title)
    html_page = markdown.Markdown().convert(md_file)
    if html_page == None:
        return None
    else:
        return html_page;


def entry_page(request, title):
    html_page = convert_md(title)
    if html_page == None:
        return render(request, "error.html",{
            "errorMessage": "Page Not Found For Entry",
        })
    else:
        return render(request, "entry.html",{
            "entry": title,
            "content": html_page,
        })

def search_page(request):
    if request.method == 'POST':
        query = request.POST['q']
        listEntries = util.list_entries()
        
        if query in listEntries:
            return render(request, "entry.html",{
                "entry": query,
                "content": util.get_entry(query),
            })
        else:
            recommendation =[]
            for entry in listEntries:
                if query.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "search_result.html",{
                'entry': query,
                "recommendation": recommendation,
            })


        
# def new_page(request):
#     return render(request, 'encyclopedia/new.html')  

def new_page(request):
    if request.method == 'GET':
        return render(request, 'new.html') 
    else:
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            entryExist = util.get_entry(title)
            
            if entryExist is not None:
                return render(request, 'foundError.html',{
                'title': title,
            })
                
            else:
                util.save_entry(title, content)
                html_page = convert_md(title)
                
                return render(request, 'entry.html',{
                    'entry': title,
                    'content': html_page
                })
            
           
#render the edit.html with the title and content
         
def edit_page(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, 'edit.html',{
            'title': title,
            'content':  content
        })  

#save edited changes and if delete button is activated delete entry and redirect user to list of entries avai
def save_page(request):
    title = request.POST['title']
    content = request.POST['content']
    to_delete = request.POST.get('to_delete', '')

    if to_delete:
        util.delete_entry(title)
        entries = util.list_entries()
        return render(request, 'index.html',{
            'entries': entries
        })
            
    else:  
        util.save_entry(title, content)
        html_page = convert_md(title)
        
        return render(request, 'entry.html',{
            'entry': title,
            'content': html_page,
        })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    html_page = convert_md(random_entry)
    
    return render(request, 'entry.html',{
        'entry': random_entry,
        'content': html_page,
    })
        
            
    