import os
import sys
import random
import pygame
from pygame.locals import *
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM = 50
# 退出
def Stop():
	pygame.quit()
	sys.exit()
# 判断游戏是否结束
def Over(board, size):
	num_cell = size * size
	for i in range(num_cell-1):
		if board[i] != i:
			return False
	return True
# 空白左移
def MoveL(board, blankCell, columns):
	if blankCell % columns == 0:
		return blankCell
	board[blankCell-1], board[blankCell] = board[blankCell], board[blankCell-1]
	return blankCell-1
#空白右移
def MoveR(board, blankCell, columns):
	if (blankCell+1) % columns == 0:
		return blankCell
	board[blankCell+1], board[blankCell] = board[blankCell], board[blankCell+1]
	return blankCell+1
# 空白上移
def MoveU(board, blankCell, columns):
	if blankCell < columns:
		return blankCell
	board[blankCell-columns], board[blankCell] = board[blankCell], board[blankCell-columns]
	return blankCell-columns
# 空白下移
def MoveD(board, blankCell, row, columns):
	if blankCell >= (row-1) * columns:
		return blankCell
	board[blankCell+columns], board[blankCell] = board[blankCell], board[blankCell+columns]
	return blankCell+columns
# 获得打乱的拼图
def CreatePicture(row, columns, Num_Cell):
	board = []
	for i in range(Num_Cell):
		board.append(i)
	# 去掉右下角那块方块
	blankCell = Num_Cell - 1
	board[blankCell] = -1
	for i in range(NUM):
		direction = random.randint(0, 3)
		if direction == 0:
			blankCell = MoveR(board, blankCell, columns)
		elif direction == 1:
			blankCell = MoveL(board, blankCell, columns)
		elif direction == 2:
			blankCell = MoveD(board, blankCell, row, columns)
		elif direction == 3:
			blankCell = MoveU(board, blankCell, columns)
	return board, blankCell
# 随机选取一张图片
def getPath(filepath):
	imgs = os.listdir(filepath)
	return os.path.join(filepath, random.choice(imgs))
# 显示游戏结束界面
def ShowEnd(Demo):
	overback=pygame.image.load("over.jpg").convert()
	Demo.blit(overback,(0,0))
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				Stop()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					Stop()
# 显示游戏开始界面
def ShowStart(Demo):
	background = pygame.image.load("backg.jpg").convert()
	Demo.blit(background,(0,0))
	pygame.display.update()
	while True:
		size = None
		for event in pygame.event.get():
			if event.type == QUIT:
				Stop()
			if event.type == KEYDOWN:
				if event.key == ord('1'):
					size = 3
				elif event.key == ord('2'):
					size = 4
				elif event.key == ord('3'):
					size = 5
		if size:
			break
	return size
# 主函数
def main(filepath):
	# 初始化
	pygame.init()
	# 加载图片
	gameImg = pygame.image.load(getPath(filepath))
	ImgRect = gameImg.get_rect()
	# 设置窗口
	Demo = pygame.display.set_mode((ImgRect.width, ImgRect.height))
	pygame.display.set_caption('拼图游戏')
	# 开始界面
	size = ShowStart(Demo)

	row, columns = size, size
	Num_Cell = size * size
	# 计算Cell大小
	cellWidth = ImgRect.width // columns
	cellHeight = ImgRect.height // row
	# 游戏是否结束
	over = False
	# 避免初始化为原图
	while True:
		gameBoard, blankCell = CreatePicture(row, columns, Num_Cell)
		if not Over(gameBoard, size):
			break
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				Stop()
			if over:
				ShowEnd(Demo)
			# 键盘操作
			if event.type == KEYDOWN:
				if event.key == K_LEFT:
					blankCell = MoveL(gameBoard, blankCell, columns)
				elif event.key == K_RIGHT :
					blankCell = MoveR(gameBoard, blankCell, columns)
				elif event.key == K_UP :
					blankCell = MoveU(gameBoard, blankCell, columns)
				elif event.key == K_DOWN:
					blankCell = MoveD(gameBoard, blankCell, row, columns)
			# 鼠标操作
			if event.type == MOUSEBUTTONDOWN :
				x, y = pygame.mouse.get_pos()
				x_pos = x // cellWidth
				y_pos = y // cellHeight
				idx = x_pos + y_pos * columns
				if idx==blankCell-1 or idx==blankCell+1 or idx==blankCell+columns or idx==blankCell-columns:
					gameBoard[blankCell], gameBoard[idx] = gameBoard[idx], gameBoard[blankCell]
					blankCell = idx
		if Over(gameBoard, size):
			gameBoard[blankCell] = Num_Cell-1
			over = True
		Demo.fill(WHITE)
		for i in range(Num_Cell):
			x_pos = i % columns
			y_pos = i // columns
			rect = pygame.Rect(x_pos*cellWidth, y_pos*cellHeight, cellWidth, cellHeight)
			ImgArea = pygame.Rect((gameBoard[i]%columns)*cellWidth, (gameBoard[i]//columns)*cellHeight, cellWidth, cellHeight)
			Demo.blit(gameImg, rect, ImgArea)
		for i in range(columns+1):
			pygame.draw.line(Demo, BLACK, (i*cellWidth, 0), (i*cellWidth, ImgRect.height))
		for i in range(row+1):
			pygame.draw.line(Demo, BLACK, (0, i*cellHeight), (ImgRect.width, i*cellHeight))
		pygame.display.update()
file = './pictures'
main(file)