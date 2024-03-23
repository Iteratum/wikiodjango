from django.shortcuts import render, redirect
import markdown
import random
from . import util
from rest_framework.response import Response
from rest_framework.decorators import api_view
from wikio.models import Entry
from wikio.serializers import EntrySerializer
import json
import random
from django.http import HttpResponse

@api_view(['GET'])
def get_data(request, id):
    result = Entry.objects.filter(pk=id)
    serializer = EntrySerializer(result, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def index(request):
    index_entries = Entry.objects.all()
    serializer = EntrySerializer(index_entries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def randoms(request):
   total = Entry.objects.all().count()
   pk = random.randint(1, total)
   result = Entry.objects.filter(pk=pk)
   serializer = EntrySerializer(result, many=True)
   return Response(serializer.data)
    
@api_view(['POST', 'GET'])
def newPage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        thumbnail = request.FILES.get("thumbnail")
        print(thumbnail)
        
        title_exists = Entry.objects.filter(title__contains=title).exists()
        if title_exists:
            response = "Content already exists"
            return HttpResponse(response)
        else:
            #util.save_entry(title, content)
            #body = markdown.markdown(util.get_entry(title))
            uploaded_data = Entry(title=title, content=content, thumbnail=thumbnail)
            uploaded_data.save()
            response = "Content saved"
            return HttpResponse(response)
    
    
    
def editPage(request):
    if request.method == "GET":
        title = request.GET['tle']
        cont = util.get_entry(title)
        return render(request, "wikio/editPage.html", {
            "title": title,
            "content": cont
        })
    else:
        if request.method == "POST":
            saved_title = request.POST['title']
            saved_content = request.POST['content']
        util.save_entry(saved_title, saved_content)
        saved_cont = markdown.markdown(util.get_entry(saved_title))
        return render(request, "wikio/entries.html", {
            "title": saved_title,
            "content": saved_cont
        })


def search(request):
    search_keyword = request.POST.get("q")
    database_content_title = Entry.objects.all()
    for list in database_content_title:
        if search_keyword.lower() == str(list).lower():
            body = markdown.markdown(util.get_entry(search_keyword))
            return render(request, "wikio/entries.html", {
            "title": search_keyword,
            "content": body
        })
        else:
            if search_keyword.lower() in str(list).lower():
                sub_list = [i for i in database_content_title if search_keyword.lower() in str(i).lower()]
                return render(request, "wikio/search.html", {
                    "title": search_keyword,
                    "recs": sub_list
                })
            