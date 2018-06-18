from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import WordBook
# Create your views here.

#@login_required
def wordbook(request):
    all_wordbooks = WordBook.objects.all()
    wordbook_info = []
    for wordbook in all_wordbooks:
        info = {}
        info['title'] = wordbook.title
        info['description'] = wordbook.description
        info['uploaded_user'] = wordbook.uploaded_user.username
        info['word_num'] = wordbook.word_num
        wordbook_info.append(info)
        user_name = wordbook.uploaded_user.username
    return render(request, 'workbook.html', {'data': wordbook_info, 'username': user_name})
