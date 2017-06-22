# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseRedirect
from mysite.models import *
from mysite.forms import *
from django.db.models import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import time
now_url = '/index/'

def index(request):
	global now_url 
	now_url = request.path
	session_username = request.session.get('session_username')
	top_url = Top_url.objects.all()
	sort_tag = Sort_tag.objects.all()
	blog_hot = Blog.objects.filter(IS_TOP = 'Y')
	news_tag_list = News_tag.objects.annotate(arcticle_num = Count('news')).order_by('-arcticle_num')[:12]
	blog_tag_list = Blog_tag.objects.annotate(arcticle_num = Count('blog')).order_by('-arcticle_num')[:12]
	news =  News.objects.annotate(comment_num = Count('news_comment')).order_by('-comment_num')[:4]
	blog = Blog.objects.annotate(comment_num = Count('blog_comment')).order_by('-comment_num')[:6]
	share = Share.objects.all()[:4]
	return render(request,'index.html',locals())

def news_index(request):
	global now_url 
	now_url = request.path
	session_username = request.session.get('session_username')
	comment_num = News.objects.annotate(comment_num = Count('news_comment')).order_by('-comment_num')[:5]
	news_tag = News_tag.objects.all()
	news_list = News.objects.all()
	paginator = Paginator(news_list,5)
	page = int(request.GET.get('page',1))
	try:
		news = paginator.page(page)
	except (EmptyPage,PageNotAnInteger,InvalidPage):
		news = paginator.page(1)

	return render(request,'news-index.html',locals())

def news_detail(request,pk):
	global now_url 
	now_url = request.path
	session_username = request.session.get('session_username')
	news = News.objects.get(pk = pk)
	news_tag_list = News_tag.objects.filter(news__pk = pk)
	if request.method == 'POST':
		cf = CommentForm(request.POST)
		if cf.is_valid():
			author = Reg_vip.objects.get(username = username)
			add_comment = News_comment.objects.create(news_title = news,comment = author,
				comment_text = cf.cleaned_data['comment_text'])
			response = redirect(now_url+'#newsdetail-comment')
			return response
	else:
		cf = CommentForm()
	return render(request,'news-detail.html',locals())

def blog_index(request):
	global now_url 
	now_url = request.path
	session_username = request.session.get('session_username')
	blog_tag = Blog_tag.objects.all()
	comment_num = Blog.objects.annotate(comment_num = Count('blog_comment')).order_by('-comment_num')[:5]
	blog_num = Reg_vip.objects.annotate(blog_num = Count('blog')).order_by('-blog_num')[:5]
	blog_list = Blog.objects.filter(IS_TOP = 'N')
	paginator = Paginator(blog_list,5)
	page = int(request.GET.get('page',1))
	try:
		blog = paginator.page(page)
	except (EmptyPage,PageNotAnInteger,InvalidPage):
		blog = paginator.page(1)

	return render(request,'blog-index.html',locals())

def blog_detail(request,pk):
	global now_url 
	now_url = request.path
	session_username = request.session.get('session_username')
	blog = Blog.objects.get(pk = pk)
	if request.method == 'POST':
		author = Reg_vip.objects.get(username = username)
		cf = CommentForm(request.POST)
		if cf.is_valid():
			blog_title = Blog.objects.get(pk = pk)
			add_comment = Blog_comment.objects.create(blog_title = blog_title,comment = author,
				comment_text = cf.cleaned_data['comment_text'])
			response = redirect(now_url+'#blogdetail-comment')
			return response
	else:
		cf = CommentForm()
	return render(request,'blog-detail.html',locals())

def tag(request,tag):
	global now_url 
	now_url = request.path
	username = request.session.get('session_username')
	try:
		news_tag = News_tag.objects.get(name = tag)
	except:
		try:
			blog_tag = Blog_tag.objects.get(name = tag)
		except:
			author_tag = Reg_vip.objects.get(username = tag)

	if request.method == 'POST':
		author = Reg_vip.objects.get(username = username)
		cf = CommentForm(request.POST)
		if cf.is_valid():
			blog_title = Blog.objects.get(pk = pk)
			add_comment = Blog_comment.objects.create(blog_title = blog_title,comment = author,
				comment_text = cf.cleaned_data['comment_text'])
			response = redirect(now_url+'#blogdetail-comment')
			return response
	else:
		cf = CommentForm()
	return render(request,'tag.html',locals())

def share_index(request):
	global now_url 
	now_url = request.path
	session_username = request.session.get('session_username')
	share_list = Share.objects.all()
	return render(request,'share-index.html',locals())

def register(request):
	if request.method == 'POST':
		uf = UserForm(request.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			email = uf.cleaned_data['email']
			try:
				is_register = Reg_vip.objects.get(username=username)
			except:
				add_register = Reg_vip.objects.create(username=username,password=password,email=email)
				request.session['session_username'] = username
				session_username = request.session.get('session_username')
				return render(request,'success-reg.html',locals())
	else:
		uf = UserForm()
	return render(request,'register.html',locals())

def login(request):
	global now_url
	if request.method == 'POST':
		uf = UserForm(request.POST)
		# print(uf)
		print(uf.is_valid)
		if uf.is_bound:
			a = uf.is_valid()
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			# print(username)
			user = Reg_vip.objects.filter(username= username,password = password)
			if user:
				response = redirect(now_url)
				# print(response)
				request.session['session_username'] = username
				return response
			else:
				is_login = 1
	else:
		uf = UserForm()
		print('else')
	return render(request, 'login.html', locals())

def logout(request):
	global now_url
	del request.session['session_username']
	response = redirect(now_url)
	return response

def userinfo(request):
	return render(request,'userinfo.html')

@csrf_exempt
def ajax_check_username(request):
	# print(request.POST)
	try:
		username = Reg_vip.objects.get(username=request.POST['username'])
	except:
		username = False
	return HttpResponse(username)

@csrf_exempt
def ajax_feedback(request):
	# print(request.POST)
	feedback_content = request.POST['feedback_content']
	feedback_contact = request.POST['feedback_contact']
	# print(feedback_content)
	# print(feedback_contact)
	if (feedback_content):
		feedback = Feedback.objects.create(feedback_content = feedback_content,feedback_contact = feedback_contact)
		send_mail(
				'反馈信息',
				feedback_content,
				'xxx@163.com',		#settings 里设置的发件箱
				['xxx@qq.com'],		#收件箱
				fail_silently=False
			)
	else:
		return HttpResponse(False)

	return HttpResponse(True)


