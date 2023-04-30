from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .models import Record
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .serializers import RecordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

import secrets
import random
# Create your views here.

def home(request):
	return render(request,'home.html')

def signupuser(request):
	#any time you enter a url in browser that is a GET request
	if request.method== 'GET':
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return render(request,'signupuser.html',{'form':UserCreationForm()})
	else:
		#check if password and confirm password are same
		if request.POST['password1'] == request.POST['password2']:
			try:
				userCreate= User.objects.create_user(request.POST['username'],password=request.POST['password1'])
				userCreate.save()
				login(request,userCreate)
				return redirect('newgame')
				
			
			except IntegrityError:
				return render(request,'signupuser.html',{'form':UserCreationForm(),'error':'Same username already exists!'})
		
		else:
			return render(request,'signupuser.html',{'form':UserCreationForm(),'error':'Passwords not matching'})


@login_required
def logoutuser(request):
	logout(request);
	return redirect('home')



def loginuser(request):
	if request.method== 'GET':
		return render(request,'loginuser.html',{'form':AuthenticationForm()})
	else:
		#check if password and confirm password are same
		userFind=authenticate(request,username=request.POST['username'],password=request.POST['password'])

		#if no user exists then userFind is None
		if userFind is None:
			return render(request,'loginuser.html',{'form':AuthenticationForm(),'error':'Username or Password is incorrect'})
		
		else:
			login(request,userFind)
			return redirect('newgame')
			#inside redirect don't write the html page but write the url endpoint that is name of path
			
			# userTodos=Todo.objects.filter(user = request.user)
			#return redirect(reverse('currentTodos'),userTodos= userTodos,l=c)




class GenerateSudoku:


	def isValid(self,board,po,i,j):
		#print("isValid")
		c=int(po)
		for m in range(0,9):
			if board[i][m]==c:
				return False
		for m in range(0,9):
			if board[m][j]==c:
				return False

		sub_i=3*(int(i/3))
		sub_j=3*(int(j/3))
		for m in range(0,3):
			for n in range(0,3):
				if board[sub_i+m][sub_j+n]==c:
					return False

		return True




	def solve(self,board,i,j):
		#print("solve")
		ni=0 
		nj=0
		if i==9:
			return True
		if j==(9-1):
			ni=i+1 
			nj=0
		else:
			nj=j+1
			ni=i 

		if board[i][j]==0:
			for po in range(1,10):
				if self.isValid(board,po,i,j):
					c=po 
					board[i][j]=c 
					if self.solve(board,ni,nj)==True:
						return True
					board[i][j]=0
		else:
			if self.solve(board,ni,nj)==True:
				return True
		return False


	def isValDia(self,board,n,i,j):
		#print("isValDia")
		for a in range(0,3):
			for b in range(0,3):
				x=a+i 
				y=b+j 
				z=board[x][y]
				if z==n:
					#print("false")
					return False
		#print("true")
		return True


	def gen_dia_code(self,board,i,j):
		#print("gen_dia_code")
		for a in range(0,3):
			for b in range(0,3):
				check=True
				while check==True:
					l = list(range(1, 10))  # the cast to list is optional in Python 2
					random.shuffle(l)
					n=l.pop()
					#print(n)
					ch=self.isValDia(board,n,i,j)
					if ch==True:
						x=a+i 
						y=b+j 
						board[x][y]=n 
						# print(a+i,end=" ")
						# print(b+j,end=" ")
						# print(n,end=" ")
						# print(board[a+i][b+j])
						break


	def gen_dia(self,board):
		#print("gen_dia")
		i=0
		j=0
		self.gen_dia_code(board,i,j)
		#self.display(board)
		i=3
		j=3
		self.gen_dia_code(board,i,j)
		#self.display(board)
		i=6
		j=6
		self.gen_dia_code(board,i,j)
		#print("After dia")
		#self.display(board)


	def solve_check(self,board,i,j,cnt_unique):
		#print("solve_check")
		ni=0 
		nj=0 
		if i==9:
			cnt_unique[0]+=1
		else:
			if j==(9-1):
				ni=i+1
				nj=0
			else:
				nj=j+1
				ni=i 
			if board[i][j]==0:
				for po in range(1,10):
					if self.isValid(board,po,i,j):
						c=po 
						board[i][j]=c 
						self.solve_check(board,ni,nj,cnt_unique)
						board[i][j]=0 

			else:
				self.solve_check(board,ni,nj,cnt_unique)



	def gen_uns_sud(self,board,filled):
		#print("gen_uns_sud")
		try_board=[[0]*9]*9
		emp=81-filled
		i=0
		cnt_unique=[0]*1
		while i<emp:
			l = list(range(0, 9))  # the cast to list is optional in Python 2
			random.shuffle(l)
			ran_r=l.pop()

			l = list(range(0, 9))  # the cast to list is optional in Python 2
			random.shuffle(l)
			ran_c=l.pop()
			
			if board[ran_r][ran_c]==0:
				continue;
			val=board[ran_r][ran_c]
			board[ran_r][ran_c]=0
			cnt_unique[0]=0
			#self.solve_check(board,0,0,cnt_unique)
			cnt_unique[0]=1
			if cnt_unique[0]>1:
				board[ran_r][ran_c]=val 
				continue
			i+=1


	def display(self,board):
		#print("display")
		for m in range(0,9):
			for n in range(0,9):
				print(board[m][n],end = " ")
				if n==2 or n==5:
					print("||",end=" ")
			print("")
			if m==2 or m==5:
				print("=====================")


	def call(self,choice):
		#print("call")
		#board=[[0]*9]*9
		#solution=[[0]*9]*9
		board = [[0]*9 for _ in range(9)]
		solution=M = [[0]*9 for _ in range(9)]
		self.gen_dia(board)
		ni=0
		nj=0

		self.solve(board,ni,nj)
		for i in range(0,9):
			for j in range(0,9):
				solution[i][j]=board[i][j]
		#self.display(board)

		if choice==1:
			self.gen_uns_sud(board,43)
		elif choice==2:
			self.gen_uns_sud(board,38)
		else:
			self.gen_uns_sud(board,31)

		cnt=0
		
		return board,solution

@login_required
def newGame(request):
	return render(request,'newgame.html')




@login_required
def showSudoku(request):
	if request.method=='GET':
		redirect('newgame')

	elif request.method=='POST':
		difficulty='easy'
		choice=1
		points=0
		board=[]
		solution=[]
		minutes=12
		if request.POST.get('easy'):
			difficulty='easy'
			choice=1
			points=5
			filled=43
			minutes=10
		elif request.POST.get('medium'):
			difficulty='medium'
			choice=2
			points=10
			filled=38
			minutes=15
		elif request.POST.get('hard'):
			difficulty='hard'
			choice=3
			points=15
			filled=31
			minutes=20
		
		p=GenerateSudoku()
		board,solution= p.call(choice)
		li=[]

		for i in range(0,9):
			for j in range(0,9):
				if board[i][j]==0:
					board[i][j]='-'
		

		#p.display(board)
		for i in range(0,9):
			y= ''.join(str(v) for v in board[i])
			li.append(y)
		lis=" ".join(li)
		

		lo=[]
		for i in range(0,9):
			#y="".join(board[i])
			y= ''.join(str(v) for v in solution[i])
			lo.append(y)
		sol=" ".join(lo)
		#print(sol)

		#lis="387491625 241568379 569327418 758619234 123784596 496253187 934176852 675832941 812945763"
		
		
		return render(request,"sudoku.html",{'board':lis , 'minutes':minutes, 'solution':sol, 'life':5, 'filled':filled,'difficulty':difficulty, 'points':points})


@login_required
@api_view(['POST'])
def result(request):
	if request.method=='POST':
		difficulty=request.POST['difficulty']
		remainingTime=request.POST['timer']
		message=request.POST['message']
		lifeLeft=request.POST['life']
		points=request.POST['points']
		user=request.user
		# print(type(lifeLeft))
		# print(lifeLeft)
		# print(points)
		if lifeLeft=='0':
			points=0
		elif difficulty=='easy':
			points=5
		elif difficulty=='medium':
			points=10
		else:
			points=15
		
		
		serializer= RecordSerializer(data=request.data)

		if serializer.is_valid():
			print("valid")
			
			serializer.save(points=points,difficulty=difficulty,timer=remainingTime,life=lifeLeft,user=user)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		return render(request,"result.html",{'difficulty':difficulty, 'remainingTime':remainingTime, 'points':points, 'message':message, 'lifeLeft':lifeLeft})

@login_required
@api_view(['GET'])
def records(request):
	if request.method=='GET':
		history=Record.objects.filter(user = request.user)
		serializer=RecordSerializer(history,many=True)
		return render(request,'records.html',{'records': serializer.data})





def developercontacts(request):
	return render(request,'developercontacts.html')


def howtoplay(request):
	return render(request,'howtoplaysudoku.html')

