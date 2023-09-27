from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.db import connection
from django.db.models import Q


# Create your views here.

def index(request):
    user = request.session.get('userid')
    ct=""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    x = category.objects.all().order_by('-id')[0:6]
    pdata = myproduct.objects.all().order_by('-id')[0:3]
    men = myproduct.objects.all().filter(mcategory=1)[0:4]
    women = myproduct.objects.all().filter(mcategory=2)[0:4]
    kid = myproduct.objects.all().filter(mcategory=3)[12:16]
    mydict = {"data":x, "prodata":pdata, "cart":ct, "men":men, "women":women, "kid":kid}
    return render(request, 'user/index.html',context=mydict)

############################################################################

def about(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    return render(request, 'user/aboutus.html', {"cart":ct})

############################################################################

def product(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    return render(request, 'user/product.html', {"cart":ct})

###########################################################################

def myorder(request):
    user = request.session.get('userid')
    oid = request.GET.get('oid')
    pdata=""
    ddata=""
    if user:
        if oid is not None:
            morder.objects.all().filter(id=oid).delete()
            return HttpResponse("<script>alert('Your Order has been canclled..'); location.href='/user/myorder/'</script>")
        cursor = connection.cursor()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='"+str(user)+"' and o.remarks='Pending'")
        pdata = cursor.fetchall()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='" + str(user) + "' and o.remarks='Delivered'")
        ddata = cursor.fetchall()

    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()

    mydict={"cart":ct, "pdata":pdata, "ddata":ddata}
    return render(request, 'user/myorder.html', context=mydict)

#########################################################################

def enquiry(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    status = False
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("email")
        c=request.POST.get("mob")
        d=request.POST.get("msg")
        contactus(Name=a, Mobile=c, Email=b, Message=d).save()
        status = True
        #mdict={"Name":a, "Email":b, "Mobile":c, "Message":d}
    msg = {"m":status, "cart":ct}
    return render(request, 'user/enquiry.html',context=msg,)

#########################################################################

def signup(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("passwd")
        c=request.POST.get("email")
        d=request.POST.get("mob")
        e=request.FILES.get("ppic")
        f=request.POST.get("add")
        x=register.objects.all().filter(email=c).count()
        if x==0:
            register(name=a, email=c, mobile=d, ppic=e, passwd=b, address=f).save()
            return HttpResponse("<script>alert('You are registered Succesgully');location.href='/user/signup/'</script>")
        else:
            return HttpResponse("<script>alert('Email Id is already registered');location.href='/user/signup/'</script>")

    return render(request, 'user/signup.html',{"cart":ct})

#########################################################################

def myprofile(request):
    user = request.session.get('userid')
    x=""
    if user:
        if request.method=="POST":
            a = request.POST.get("name")
            b = request.POST.get("passwd")
            d = request.POST.get("mob")
            e = request.FILES.get("ppic")
            f = request.POST.get("add")
            register(name=a, email=user, mobile=d, ppic=e, passwd=b, address=f).save()
            return HttpResponse("<script>alert('Your Profile Updated Successfuly'); location.href='/user/profile/'</script>")
        x = register.objects.all().filter(email=user)
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    d= {"cart":ct, "mydata":x}
    return render(request, 'user/myprofile.html', context=d)

#########################################################################

def signin(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    if request.method=="POST":
        Email = request.POST.get("email")
        Passwd = request.POST.get("passwd")
        x = register.objects.all().filter(email=Email, passwd=Passwd).count()
        y = register.objects.all().filter(email=Email, passwd=Passwd)
        if x==1:
            request.session['userid']=Email
            request.session['userpic']=str(y[0].ppic)
            return HttpResponse("<script>alert('Login Successfully');location.href='/user/profile/'</script>")
        else:
            return HttpResponse("<script>alert('Your Email or Password is incorrect !!');location.href='/user/signin/'</script>")
    return render(request, 'user/signin.html',{"cart":ct})

#########################################################################

def mens(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('abc')
    cat = category.objects.all().order_by('-id')
    data = myproduct.objects.all().filter(mcategory=1)
    if cid is not None:
        data = myproduct.objects.all().order_by('-id').filter(mcategory=1, pcategory=cid)
    mydict = {"cats":cat, "prodata":data, "cart":ct}
    return render(request, 'user/mens.html', mydict)

#########################################################################

def womens(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('abc')
    cat = category.objects.all().order_by('-id')
    data = myproduct.objects.all().filter(mcategory=2)
    if cid is not None:
        data = myproduct.objects.all().order_by('-id').filter(mcategory=2, pcategory=cid)
    mydict = {"cats": cat, "prodata": data, "cart":ct}
    return render(request, 'user/womens.html',mydict)

#########################################################################

def kids(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('abc')
    cat = category.objects.all().order_by('-id')
    data = myproduct.objects.all().filter(mcategory=3)
    if cid is not None:
        data = myproduct.objects.all().order_by('-id').filter(mcategory=3, pcategory=cid)
    mydict = {"cats": cat, "prodata": data, "cart":ct}
    return render(request, 'user/kids.html',mydict)

#########################################################################

def viewproduct(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    a = request.GET.get('msg')
    x = myproduct.objects.all().filter(id=a)
    return render(request, 'user/viewproduct.html', {"pdata":x, "cart":ct})

#########################################################################

def signout(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    if request.session.get('userid'):
        del request.session['userid']
    return HttpResponse("<script>alert('You are signed out..'); location.href='/user/index/'</script>")

#########################################################################

def myordr(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    user = request.session.get('userid')
    pid = request.GET.get('msg')
    if user:
        if pid is not None:
            morder(userid=user, pid=pid, remarks="Pending", odate=datetime.now().date(), status=True).save()
            return HttpResponse("<script>alert('Your Order Confirmed ..'); location.href='/user/index/'</script>")
    else:
        return HttpResponse("<script>alert('You have to Login First ..'); location.href='/user/signin/'</script>")
    return render(request, 'user/myordr.html', {"cart":ct})

#########################################################################

def mycart(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    p = request.GET.get('pid')
    user = request.session.get('userid')
    if user:
        if p is not None:
            mcart(userid=user, pid=p, cdate=datetime.now().date(), status=True).save()
            return HttpResponse("<script>alert('Your Item is add in Cart'); location.href='/user/index/'</script>")
    else:
        return HttpResponse("<script>alert('You have to Login First'); location.href='/user/signin/'</script>")

    return render(request, 'user/mcart.html', {"cart":ct})

#########################################################################

def showcart(request):
    user = request.session.get('userid')
    cid = request.GET.get('cid')
    a = request.GET.get('msg')
    pid = request.GET.get('pid')
    data = ""
    if user:
        if a is not None:
            mcart.objects.all().filter(id=a).delete()
            return HttpResponse("<script>alert('Your Cart Product has been canclled..'); location.href='/user/showcart/'</script>")
        elif pid is not None:
            mcart.objects.all().filter(id=cid).delete()
            morder(userid=user, pid=pid, remarks="Pending", status=True, odate=datetime.now().date()).save()
            return HttpResponse("<script>alert('Your Order has been placed Successfuly..'); location.href='/user/myorder/'</script>")

        cursor = connection.cursor()
        cursor.execute("select p.*,c.* from user_myproduct p,user_mcart c where p.id=c.pid and c.userid='" + str(user) + "'")
        data = cursor.fetchall()

    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    return render(request, 'user/showcart.html', {"cart":ct, "odata":data})

#########################################################################

def cpdetail(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    c = request.GET.get('cid')
    p = myproduct.objects.all().filter(pcategory=c)
    return render(request, 'user/cpdetail.html', {"pdata":p, "cart":ct})

#########################################################################

def mypage(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    return render(request, 'user/mypage.html',{"cart":ct})

#########################################################################

def search(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    query = request.GET.get('query')
    allproduct = myproduct.objects.all().filter(Q(psize__icontains=query) | Q(pdel__icontains=query))
    return render(request, 'user/search.html', {"allpost":allproduct, "cart":ct})