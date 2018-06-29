from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from learn.constants import *

from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.urls import reverse
# Create your views here.

import datetime

try:
    from django.utils import simplejson as json
except ImportError:
    import json

class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, date):  
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj) 

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

@login_required
def wordbook(request):
    user = request.user
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
        user_name = user.username
    return render(request, 'workbook.html', {'data': wordbook_info, 'username': user_name})

@login_required
def wordbookunit(request):
    passed = {}
    passed['wordbook_info'] = get_all_books()
    user = request.user
    if request.method == "GET":
        if 'id' in request.GET:
            all_words_num = 0
            wordbook_id = request.GET['id']
            get_book = WordBook.objects.get(id=wordbook_id)
            passed['title'] = get_book.title
            passed['description'] = get_book.description
            #passed['word_num'] = get_book.word_num
            passed['uploaded_user'] = get_book.uploaded_user.username
            passed['username'] = user.username
            wordbookunit = WordUnit.objects.filter(book=get_book)
            if LearningPlan.objects.filter(user=user, wordbook=get_book).count() > 0:
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
        if LearningPlan.objects.filter(user=user, wordbook=get_book).count() > 0:
            LearningPlan.objects.get(user=user, wordbook=get_book).delete()
            lr = LearningRecord.objects.get(user=user, wordbook=get_book)
            lr.islearning = 0
            lr.save()
        else:
            lp = LearningPlan(user=user, wordbook=get_book)
            lp.save()
            if LearningRecord.objects.filter(user=user, wordbook=get_book).count() == 0:
                lr = LearningRecord(user=user, wordbook=get_book)
                if LearningRecord.objects.filter(user=user, islearning=1).count() == 0:
                    lr.islearning = 1
                lr.save()
            else:
                r = LearningRecord.objects.get(user=user, islearning=1)
                r.islearning = 0
                r.save()
                lr = LearningRecord.objects.get(user=user, wordbook=get_book)
                lr.islearning = 1
                lr.save()
        ctx = {'message': user.username}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
        #plan = LearningPlan(user=get_book.uploaded_user,wordbook=get_book)
        #plan.save()
    return render(request, 'wordbookunit.html', passed)

@login_required
def wordlist(request):
    passed = {}
    user = request.user
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
            passed['username'] = user.username
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


@login_required
def mywordbook(request):
    passed = {}
    user = request.user
    passed['username'] = user.username
    passed['wordbook_info'] = get_all_books()

    #pdb.set_trace()
    print(request.method)
    if request.method == 'POST' and request.is_ajax():
        learning_id = request.POST.get('learning_id', None)
        learning_book = WordBook.objects.get(id=int(learning_id))
        learningrecord = LearningRecord.objects.get(user=user, wordbook=learning_book)
        learningrecord.islearning = 0
        learningrecord.save()

        value = request.POST.get('value', None)
        get_book = WordBook.objects.get(id=int(value))
        changedrecord = LearningRecord.objects.get(user=user, wordbook=get_book)
        changedrecord.islearning = 1
        changedrecord.save()

    userplans = LearningPlan.objects.filter(user=user)
    plan_books = []
    for plan in userplans:
        record = LearningRecord.objects.get(user=user, wordbook=plan.wordbook)
        if record.islearning:
            passed['learningbook'] = plan.wordbook.title
            passed['learningbook_num'] = plan.wordbook.word_num
            passed['learningbook_rate'] = 0 if plan.wordbook.word_num == 0 else "%.3f" % (record.haslearned/plan.wordbook.word_num)
            passed['learning_book_time'] = record.learn_time
            passed['learning_book_score'] = "%.3f" % record.correct_rate
            passed['learningbook_id'] = plan.wordbook.id
            #continue
        info = {}
        info['title'] = plan.wordbook.title
        info['num'] = plan.wordbook.word_num
        if plan.wordbook.word_num == 0:
            info['rate'] = float(0)
        else:
            info['rate'] = "%.3f" % (record.haslearned/plan.wordbook.word_num)
        info['book_id'] = plan.wordbook.id
        plan_books.append(info)
    passed['plan_book'] = plan_books

    #pdb.set_trace()
    if request.method == "GET":
        return render(request, 'mywordbook.html', passed)
    else:
        return HttpResponse(json.dumps(passed, cls=DateEncoder), content_type='application/json')

@login_required
def learnindex(request):
    user = request.user
    passed = {}
    passed['username'] = user.username
    if LearningRecord.objects.filter(user=user, islearning=1).count() == 1:
        lr = LearningRecord.objects.get(user=user, islearning=1)
        learningbook = lr.wordbook
        
        passed['title'] = learningbook.title
        passed['description'] = learningbook.description
        passed['word_num'] = learningbook.word_num
        passed['uploaded_user'] = learningbook.uploaded_user
        
        setting = UserSetting.objects.get(user=user)
        passed['plan_num'] = setting.dailyword
        passed['learned_num'] = lr.haslearned

    return render(request, "learnindex.html", passed)

@login_required
def bdcsetting(request):
    user = request.user
    usersetting = UserSetting.objects.get(user=user)
    ctx = {}
    ctx['username'] = user.username
    ctx['dailyword_list'] = dailyword_list
    ctx['showmeaning_list'] = showmeaning_list
    ctx['learntype_list'] = learntype_list
    #if request.method == "GET":
    #    ctx['dailyword'] = usersetting.dailyword
    #    ctx['showmeaning'] = usersetting.showmeaning
    #    ctx['learntype'] = usersetting.learntype
        
    if request.method == 'POST':
        definition = request.POST.get('definition', None)
        target_level = request.POST.get('target_level', None)
        quota = request.POST.get('quota', None)
        usersetting.dailyword = int(quota)
        usersetting.showmeaning = int(definition)
        usersetting.learntype = int(target_level)
        usersetting.save()

    ctx['dailyword'] = usersetting.dailyword
    ctx['showmeaning'] = usersetting.showmeaning
    ctx['learntype'] = usersetting.learntype

    return render(request, "bdcsetting.html", ctx)

@login_required
def learnwords(request):
    user = request.user
    if request.method == 'POST' and request.is_ajax():
        lr = LearningRecord.objects.get(user=user, islearning=1)
        lr.haslearned += 1
        lr.save()
        return HttpResponse(json.dumps({}, cls=DateEncoder), content_type='application/json')
    ctx = {} 
    ctx['username'] = user.username
    learningbook = LearningRecord.objects.get(user=user, islearning=1).wordbook
    ctx['bookname'] = learningbook.title
    units = WordUnit.objects.filter(book=learningbook)
    words = []
    for unit in units:
        wordinunits = WordInUnit.objects.filter(wordunit=unit)
        for w_u in wordinunits:
            words.append(w_u.word)
    usersetting = UserSetting.objects.get(user=user)
    haslearned = LearningRecord.objects.get(user=user, islearning=1).haslearned
    dailyword = usersetting.dailyword

    data = []
    for i in range(haslearned,haslearned+dailyword,2):
        info = {}
        if usersetting.showmeaning == 1:
            info['word1_name'] = words[i].spelling
            info['word2_name'] = words[i+1].spelling
        else:
            info['word1_name'] = words[i].spelling + ': ' + words[i].meaning
            info['word2_name'] = words[i+1].spelling + ': ' + words[i+1].meaning
        info['word1_id'] = words[i].id
        info['word2_id'] = words[i+1].id
        data.append(info)
    ctx['data'] = data
    return render(request, "learnwords.html", ctx)

@login_required
def mywords(request):
    ctx = {}
    user = request.user
    ctx['username'] = user.username
    uds = UserDefWords.objects.filter(user=user)
    words_list = []
    for ud in uds:
        word_info = {}
        word_info['spelling'] = ud.word.spelling
        word_info['mean'] = ud.word.meaning
        words_list.append(word_info)
    ctx['all_words'] = words_list
    ctx['wordbook_info'] = get_all_books()

    return render(request, "mywords.html", ctx)

@login_required
def handleselfword(request):
    ctx = {}
    user = request.user
    if request.method == 'POST' and request.is_ajax():
        spell = request.POST.get('name', None)
        mean = request.POST.get('mean', None)
        if spell and mean:
            word = Word(spelling=spell, meaning=mean)
            word.save()
            ud = UserDefWords(user=user, word=word)
            ud.save()
            ctx['msg'] = "写入成功!" + request.POST.get('name', None) + ": " + request.POST.get('mean', None)
        else:
            ctx['msg'] = "写入失败！输入框不能为空"
    return HttpResponse(json.dumps(ctx, cls=DateEncoder), content_type='application/json')

@login_required
def voctest(request):
    ctx = {}
    user = request.user
    ctx['username'] = user.username
    lr = LearningRecord.objects.get(user=user, islearning=1)
    if request.method == 'GET':
        import random
        learningbook = lr.wordbook
        ctx['bookname'] = learningbook.title
        units = WordUnit.objects.filter(book=learningbook)
        chooceunit = random.randint(0, units.count()-1)
        getunit = units[chooceunit]

        words = WordInUnit.objects.filter(wordunit=getunit)
        data = []
        if words.count() > TEST_NUM:
            rand_words = random.sample(range(words.count()), TEST_NUM)
            for i in rand_words:
                #print(words[i].word.spelling)
                info={}
                info['mean'] = words[i].word.meaning
                info['id'] = words[i].word.id
                # print(info['id'])
                data.append(info)
            ctx['data'] = data
            ctx['testnum'] = TEST_NUM
        else:
            for w in words:
                # print(w.word.spelling)
                info={}
                info['mean'] = words[i].word.meaning
                info['id'] = words[i].word.id
                data.append(info)
            ctx['data'] = data
            ctx['testnum'] = words.count()
        return render(request, "voctest.html", ctx)
    if request.method == 'POST':
        correct = 0
        ids = request.POST.getlist('id', None)
        spellings = request.POST.getlist('spelling', None)
        for i, s in zip(ids, spellings):
            real_word = Word.objects.get(id=int(i)).spelling
            ans_spell = s
            if real_word == ans_spell.strip():
                correct += 1
        #print(ids)
            lr.correct_rate = int(correct/TEST_NUM)
            lr.save()
        return redirect('mywordbook')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:index'))