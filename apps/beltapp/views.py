from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quote
from django.contrib import messages

def index(request):
  return render(request, 'beltapp/index.html')

def flash_errors(errors, request):
	for error in errors:
		messages.error(request, error)

def user_session(request):
	return User.objects.get(id = request.session['user_id'])

def registration(request):
	if request.method == 'POST':
		errors = User.objects.reggie_validation(request.POST)
		if not errors:
			user = User.objects.create_user(request.POST)
			request.session['user_id'] = user.id
			return redirect('/successreg')
		flash_errors(errors, request)
	return redirect('/')

def login(request):
	if request.method == 'POST':
		check = User.objects.login_validation(request.POST)
		if 'user' in check:
			print check
			request.session['user_id']=check['user'].id
			return redirect('/successlog')
		flash_errors(check['errors'],request)
	return redirect('/')

def current_user(request):
	return User.objects.get(id=request.session['user_id'])

def successlog(request):
	context={
		'user': current_user(request),
	}
	request.session['msg'] = 'Welcome Back, '
	return render(request, 'beltapp/main.html', context)

def successreg(request):
	context={
		'user': current_user(request),
	}
	request.session['msg'] = 'Thanks for signing up, '
	return render(request, 'beltapp/main.html', context)

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')
	return redirect('/')


def fave(request, id):
	user = current_user(request)
	if request.method == 'POST':
		quote = Quote.objects.get(id=id)
		quote.favorite.add(user)
	return redirect('/main')


def remove(request, id):
	user = current_user(request)
	if request.method == 'POST':
		quote = Quote.objects.get(id=id)
		quote.favorite.remove(user)
	return redirect('/main')

def users(request, id):
	user = User.objects.get(id=id)
	quote = Quote.objects.filter(user=user)
	count = quote.count()

	context = {
		'quote' : quote,
		'user' : user,
		'count' : count,
	}
	return render(request, 'beltapp/third.html', context)

def new(request):
	user = current_user(request)
	if request.method == 'POST':
		errors = Quote.objects.quote_validation(request.POST)
		if not errors:	
			quote = Quote.objects.create(author = request.POST['author'], user=user,
		quote = request.POST['quote'])	
			
			return redirect('/main')
		flash_errors(errors, request)
	return redirect('/main')

def main(request):
	user = current_user(request)
	allquote = Quote.objects.all()
	faves = user.faves.all()

	# user = User.objects.get(id=request.session['user_id'])
	# quote = new(request)
	# quote = Quote.objects.get(id=quote.user.id)
	# faves = Quote.objects.get(id=quote.user.favorite)

	context={
		'user': current_user(request),
		'quote': allquote,
		'faves': faves,
	}
	request.session['msg'] = 'Welcome Back, '
	return render(request, 'beltapp/main.html', context)