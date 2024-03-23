from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
import random
from django.utils.html import mark_safe
from . import util
import markdown


def convert_md_html(markdown_text):
    return mark_safe(markdown.markdown(markdown_text))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/404.html", {"title": title})

    html_content = convert_md_html(content)
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "content": html_content
    })


def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search_results.html", {"query": query, "entries": matching_entries})


def newPage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {"error_message": "An entry with this title already exists."})
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('wiki', args=[title]))
    return render(request, "encyclopedia/new_page.html")


def editEntry(request, title):
    content = util.get_entry(title)
    if request.method == 'POST':
        new_content = request.POST['content']
        util.save_entry(title, new_content)
        return HttpResponseRedirect(reverse('wiki', args=[title]))
    return render(request, "encyclopedia/edit_entry.html", {
        "title": title,
        "content": content
    })


def randomPage(request):
    entries = util.list_entries()
    selected_page = random.choice(entries)
    return redirect('wiki', title=selected_page)


def deleteEntry(request, title):
    try:
        util.delete_entry(title)
        return HttpResponseRedirect(reverse('index'))
    except FileNotFoundError:
        return render(request, "encyclopedia/404.html", {"title": title})



