from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import WordBook, WordUnit
# Create your views here.

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
            wb_info = []
            for wb in wordbookunit:
                info = {}
                info['unit_name'] = 'unit' + str(wb.unit_order)
                info['word_num'] = wb.word_num
                all_words_num += wb.word_num
                wb_info.append(info)
            passed['allunits'] = wb_info
            passed['word_num'] = all_words_num   
            passed['wordbook_id'] = wordbook_id
    return render(request, 'wordbookunit.html', passed)


