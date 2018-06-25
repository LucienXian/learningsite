from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import WordBook, WordUnit, WordInUnit, LearningPlan
from learn.constants import *
# Create your views here.

try:
    from django.utils import simplejson as json
except ImportError:
    import json

def get_all_books():
    all_wordbooks = WordBook.objects.all()
    wordbook_info = []
    for wordbook in all_wordbooks:
        info = {}
        info['title'] = wordbook.title
        info['description'] = wordbook.description
        info['uploaded_user'] = wordbook.uploaded_user.username
        info['word_num'] = wordbook.word_num
        info['wordbook_id'] = wordbook.id
        wordbook_info.append(info)
    return wordbook_info

# @login_required
def wordbook(request):
    all_wordbooks = WordBook.objects.all()
    wordbook_info = []
    for wordbook in all_wordbooks:
        info = {}
        info['title'] = wordbook.title
        info['description'] = wordbook.description
        info['uploaded_user'] = wordbook.uploaded_user.username
        info['word_num'] = wordbook.word_num
        info['wordbook_id'] = wordbook.id
        wordbook_info.append(info)
        user_name = wordbook.uploaded_user.username
    return render(request, 'workbook.html', {'data': wordbook_info, 'username': user_name})

# @login_required
def wordbookunit(request):
    passed = {}
    passed['wordbook_info'] = get_all_books()
    if request.method == "GET":
        if 'id' in request.GET:
            all_words_num = 0
            wordbook_id = request.GET['id']
            get_book = WordBook.objects.get(id=wordbook_id)
            passed['title'] = get_book.title
            passed['description'] = get_book.description
            #passed['word_num'] = get_book.word_num
            passed['uploaded_user'] = get_book.uploaded_user.username
            passed['username'] = get_book.uploaded_user.username
            wordbookunit = WordUnit.objects.filter(book=get_book)
            if LearningPlan.objects.filter(user=get_book.uploaded_user, wordbook=get_book).count() > 0:
                passed['save_button_name'] = SAVE_BUTTON[1]
            else:
                passed['save_button_name'] = SAVE_BUTTON[0]
            wb_info = []
            for wb in wordbookunit:
                info = {}
                info['unit_name'] = 'unit' + str(wb.unit_order)
                info['word_num'] = wb.word_num
                info['unit_id'] = wb.id
                all_words_num += wb.word_num
                wb_info.append(info)
            passed['allunits'] = wb_info
            passed['word_num'] = all_words_num   
            passed['wordbook_id'] = wordbook_id
    if request.method == 'POST':
        value = request.POST.get('value', None)
        get_book = WordBook.objects.get(id=int(value))
        if LearningPlan.objects.filter(user=get_book.uploaded_user, wordbook=get_book).count() > 0:
            LearningPlan.objects.get(user=get_book.uploaded_user, wordbook=get_book).delete()
        else:
            lp = LearningPlan(user=get_book.uploaded_user, wordbook=get_book)
            lp.save()
        ctx = {'message': get_book.uploaded_user.username}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
        #plan = LearningPlan(user=get_book.uploaded_user,wordbook=get_book)
        #plan.save()
    return render(request, 'wordbookunit.html', passed)

# @login_required
def wordlist(request):
    passed = {}
    passed['wordbook_info'] = get_all_books()
    if request.method == "GET":
        if 'id' in request.GET:
            unit_id = request.GET['id']
            get_unit = WordUnit.objects.get(id=unit_id)
            get_book = get_unit.book
            passed['title'] = get_book.title
            passed['unit'] = 'unit' + str(get_unit.unit_order)
            passed['word_num'] = get_unit.word_num
            passed['uploaded_user'] = get_book.uploaded_user.username
            passed['username'] = get_book.uploaded_user.username
            passed['wordbook_id'] = get_book.id
            all_words = WordInUnit.objects.filter(wordunit=get_unit)
            
            words_list = []
            for wordunit in all_words:
                word_info = {}
                word_info['spelling'] = wordunit.word.spelling
                word_info['mean'] = wordunit.word.meaning
                words_list.append(word_info)
            passed['all_words'] = words_list
    return render(request, 'wordlist.html', passed)

