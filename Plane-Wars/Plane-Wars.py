#coding = utf-8
import time
import random
import pygame
from pygame.locals import *

class plane(object):
	def __init__(self,screen,name):
		self.name = name
		#显示内容的窗口
		self.screen = screen
		self.image = pygame.image.load(self.imageName).convert()
		#设置heroPlane存储子弹的列表
		self.bulletList = []

	def display(self):
		#飞机位置的更改
		self.screen.blit(self.image,(self.x,self.y))

		#创建需要删除的对象信息列表
		needDelItemList = []
		for i in self.bulletList:
			if i.judge():
				needDelItemList.append(i)

		for i in needDelItemList:
			self.bulletList.remove(i)

		#更新这架飞机发射出的所有子弹的位置
		for bullet in self.bulletList:
			bullet.display()
			bullet.bulletMove()

	def shoot(self):
		newBullet = publicBullet(self.x,self.y,self.screen,self.name)
		self.bulletList.append(newBullet)

class HeroPlane(plane):
	def __init__(self,screen,name):
		#设置heroPlane默认的坐标
		self.x = 240
		self.y = 600
		self.imageName = "./plane/heroPlane.gif"
		super().__init__(screen,name)

	def moveLeft(self):
		self.x -= 15

	def moveRight(self):
		self.x += 15

class publicBullet(object):
	def __init__(self,x,y,screen,planeName):
		self.screen = screen
		self.planeName = planeName

		if planeName == "hero":
			self.x = x + 40
			self.y = y - 20
			imageName = "./plane/bullet-1.gif"
		elif planeName == "enemy":
			self.x = x + 30
			self.y = y + 30
			imageName = "./plane/bullet-2.gif"

		self.image = pygame.image.load(imageName).convert()
		
	def bulletMove(self):
		if self.planeName == "hero":
			self.y -=3
		elif self.planeName == "enemy":
			self.y += 2

	def display(self):
		self.screen.blit(self.image,(self.x,self.y))

	def judge(self):
		if self.y>890 or self.y<0:
			return True
		else:
			return False

class EnemyPlane(plane):
	def __init__(self,screen,name):
		self.x = 0
		self.y = 0
		self.imageName = "./plane/enemyPlane.gif"
		super().__init__(screen,name)
		#敌机初始方向往右边走
		self.direction = "right"

	def move(self):
		#控制敌机移动的边界
		if self.direction == "right":
			self.x +=2
		elif self.direction == "left":
			self.x -=2
		if self.x >480-50:
			self.direction = "left"
		elif self.x<0:
			self.direction = "right"

	def shootBullet(self):
		num = random.randint(1,100)
		if num == 88:
			super().shoot()

if __name__ =="__main__":
	#创建一个活动窗口，并定义其大小
	screen = pygame.display.set_mode((480,890),0,32)
	
	#创建背景图片
	imageName = "./plane/background.png"
	background = pygame.image.load(imageName).convert()

	heroPlane = HeroPlane(screen,'hero')
	enemyPlane = EnemyPlane(screen,'enemy')
	
	while True:
		#为窗口设置需要显示的背景图
		screen.blit(background,(0,0))#从左上角坐标(0,0)插入

		heroPlane.display()
		enemyPlane.move()
		enemyPlane.shootBullet()
		enemyPlane.display()
	
		for event in pygame.event.get():
			#判断用户是否是点击了退出按钮
			if event.type == QUIT:
				exit()
			#判断用户是否是按下键
			elif event.type == KEYDOWN:
				#检测按键是否是a或者left
				if event.key == K_a or event.key == K_LEFT:
					print('left')
					heroPlane.moveLeft()
				#检测按键是否是d或者right
				elif event.key == K_d or event.key == K_RIGHT:
					print("right")
					#控制飞机让其向右移动
					heroPlane.moveRight()
				#判断按键是否是空格键
				elif event.key == K_SPACE:
					print('Space')
					heroPlane.shoot()
		time.sleep(0.01)
		#更新需要显示的内容
		pygame.display.update()