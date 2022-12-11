from django.shortcuts import render, redirect
from EMBRASSER.models import Members
from django.http import HttpRequest, JsonResponse, HttpResponse

# Create your views here.

# 관리자 회원가입
def join (request):
    return render(request,'join.html')

# 관리자 확인
def idDuplicateCheck (request):
    print("Ajax 들어옴?")
    userid = request.GET.get('userid')
    try:
        id_checked = Members.objects.get(id=userid)
        pass
    except:
        id_checked = None

    if id_checked is None:
        checkresult = "pass"
    else:
        checkresult = "fail"

    print("checkresult : ", checkresult)
    context = {
        'checkresult' : checkresult
    }

    return JsonResponse(context)

# 관리자 DB에 생성
def createMember(request:HttpRequest):
    id = request.POST.get("id")
    pw = request.POST.get("pw")

    print("=" * 30)
    print("id:", id)
    print("pw:", pw)

    try:
        Members.objects.create(
            id = id,
            pw = pw
        )
    except Exception as e:
        print(e)
        return redirect('/member/join/')

    return render(request,'login.html')

# 관리자 로그인
def login(request:HttpRequest):
    id = request.GET.get("id")
    #result = request.GET.get("result")
    print('login/id : ', id)
    check = False
    if id == None:
        print('login/id : ', id)
        id = request.COOKIES.get("checkedid")
        if id != None:
            check = True

    print('login/check : ', check)
    context = {
        'id' : id,
        "check" : check,
    }

    return render(request,'login.html',context)

# 관리자 아이디 비번 확인
def checkLogin(request:HttpRequest):
    id = request.POST.get("id")
    pw = request.POST.get("pw")
    
    result = None

    try:
        member = Members.objects.get(id=id,pw=pw)
    except Exception as e:
        result = True
        return redirect('/member/login/?result=' + result)
    else:
        request.session['login'] = member.members_idx
    
    response = render(request,'main.html')

    if result:
        checkedid = request.POST.get("checkedid")
        print("checkLogin/checkedid : ", checkedid)

        cookieid = request.COOKIES.get('checkedid')
        print("checkLogin/cookieid : ", cookieid)
        
        if checkedid != None:
            if cookieid == None:
                response.set_cookie("checkedid",id,max_age=60*60*48)
            elif cookieid != id:
                response.set_cookie("checkedid",id,max_age=60*60*48)
        else:
            if cookieid == id:
                response.delete_cookie("checkedid")

    return redirect('/')

# 관리자 로그아웃
def logout(request:HttpRequest):
    request.session.pop('login')
    return redirect('/')