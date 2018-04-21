from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
# Create your views here.\
def index(request):
	return render(request,'firstapp/index.html')


def login(request):
	if request.method == 'POST':
		user = User.objects.login_validator(request.POST)
		if(type(user) == dict and len(user)!=0):
			for key, error_val in user.items():
				messages.error(request, error_val )
			return redirect('/')
		request.session['user_id'] = user.id
	return redirect('/display')

def register(request):
	if request.method == 'POST':
		errors = User.objects.registration_validator(request.POST)
		if(type(errors) == dict and len(errors)!=0):
			for key, error_val in errors.items():
				messages.error(request, error_val )
			return redirect('/')
		result = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'],
		password = errors, dob = request.POST['dob'])
		request.session['user_id'] = result.id
	return redirect('/display')

def display(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	all_friends = user.friend_of.all()
	context ={
	'user' : user,
	'all_friends': all_friends,
	'num' : len(all_friends),
	'non_friends': User.objects.exclude(friend_of = user)
	}
	return render(request, 'firstapp/list.html', context)

def add(request, id):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	friend = User.objects.get(id=id)
	user.friend_of.add(friend)
	return redirect('/display')

def remove(request,id):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	friend = User.objects.get(id=id)
	user.friend_of.remove(friend)
	return redirect('/display')

def viewpage(request,id):
	if 'user_id' not in request.session:
		return redirect('/')
	user = user = User.objects.get(id=id)
	context={
		"user":user
	}
	return render(request, 'firstapp/view.html', context)

def logout(request):
	if 'user_id' in request.session:
		del request.session['user_id']
	return redirect('/')