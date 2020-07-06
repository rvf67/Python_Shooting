#2020810059 
#이태주
import pygame
import sys
import random
from time import sleep
#창크기 셋팅
WINDOW_ROW = 800
WINDOW_COL= 600


BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
#화면상에 그림을 그려넣는 코드 생성
def drawObject(obj, x, y):
  global gamePad
  gamePad.blit(obj,(x,y))
#개수표시
def writeCrush(x):
  global gamePad
  font=pygame.font.Font('NanumGothic.ttf',30)
  text=font.render('파괴한 장애물:'+str(x),True,WHITE)
  gamePad.blit(text,(10,0))

def helpCounter(x):
  global gamePad
  font=pygame.font.Font('NanumGothic.ttf',30)
  text=font.render('아이템 갯수:'+str(x),True,WHITE)
  gamePad.blit(text,(500,40))  

def writeFault(x):
  global gamePad
  font=pygame.font.Font('NanumGothic.ttf',30)
  text=font.render('실수:'+str(x),True,WHITE)
  gamePad.blit(text,(500,0))

def gameOver(x):
  global gamePad,gameOverSound
  overFont=pygame.font.Font('NanumGothic.ttf',80)
  text=overFont.render(x,True,RED)
  gamePad.blit(text,(400,300))
  pygame.display.update()
  pygame.mixer.music.stop()
  gameOverSound.play()
  sleep(3)
  pygame.mixer.music.play(-1)
  runGame()

def crash():
  global gamePad
  gameOver('파괴됨')

def fault():
  global gamePad
  gameOver('게임 오버')
#시작 전 이미지와 음성 세팅
def pyGame():
  global gamePad, clock, player , shooter, obstacle,boom,ally,gameOverSound,screamSound,gunSound,crushSound,itemSound
  pygame.init()
  pygame.mixer.init()
  gamePad = pygame.display.set_mode((WINDOW_ROW,WINDOW_COL))
  pygame.display.set_caption('슈팅게임')
  player=pygame.image.load('character.png')
  ally=pygame.image.load('character.png')
  shooter=pygame.image.load('bullet.png')
  obstacle=pygame.image.load('obstacle.png')
  boom=pygame.image.load('boom.png')
  gameOverSound=pygame.mixer.Sound('gameover.wav')
  crushSound=pygame.mixer.Sound('explosion.wav')
  gunSound=pygame.mixer.Sound('gun.wav')
  itemSound=pygame.mixer.Sound('item.wav')
  screamSound=pygame.mixer.Sound('scream.wav')
  pygame.mixer.music.load('bgm.mp3')
  pygame.mixer.music.play(-1)
  clock = pygame.time.Clock()

def runGame():
  global gamePad , clock, player, shooter,obstacle,boom,ally,gunSound,itemSound,screamSound,crushSound,gameOverSound
  #각종 개채들 설정
  obstacleSize=obstacle.get_rect().size
  obstacleRow=obstacleSize[0]
  obstacleCol=obstacleSize[1]
  obstacleX=random.randrange(0,WINDOW_ROW-obstacleRow)
  obstacleY=0
  obstacleColSpeed=1
  obstacleRowSpeed=random.randrange(-3,3)
  allySize=ally.get_rect().size
  allyRow=obstacleSize[0]
  allyCol=obstacleSize[1]
  allyX=random.randrange(0,WINDOW_ROW-allyRow)
  allyY=-80
  allyColSpeed=1
  playerSize=player.get_rect().size
  playerRow=playerSize[0]
  playerCol=playerSize[1]

  x=WINDOW_ROW*0.3
  y=WINDOW_COL*0.9
  playerX=0
  #총 발사 전용 리스트(좌표지정)
  shootXY=[]
  crush=False
  crush1=False
  crushCount=0
  passCount=0
  totalCount=0
  helpCount=2
  setKey = False
  #키설정
  while not setKey:
    for event in pygame.event.get():
      if event.type in [pygame.QUIT]:
        pygame.quit
        sys.exit

      if event.type in [pygame.KEYDOWN]:
        if event.key == pygame.K_LEFT:
          playerX -= 5 

        elif event.key == pygame.K_RIGHT:
          playerX += 5  

        elif event.key == pygame.K_SPACE:
          gunSound.play()
          shootX=x+playerRow/2
          shootY=y-playerCol
          shootXY.append([shootX,shootY])
        #위기의 상황에서 장애물을 없애주는 기능
        elif event.key == pygame.K_c:
          if helpCount>0:
            itemSound.play()
            sleep(2)
            helpCount -= 1
            crush= True
            crushCount += 1

      if event.type in [pygame.KEYUP]:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
          playerX = 0
      
          
    gamePad.fill(BLACK)
    #플레이어가 화면 밖으로 나가지 않도록 조정
    x += playerX
    if x<0:
      x=0
    elif x>WINDOW_ROW-playerRow:
      x=WINDOW_ROW-playerRow

    #플레이어와와 장애물의 충돌  
    if y < obstacleY+obstacleCol:
        if (obstacleX >x and x+playerRow >obstacleX) or(obstacleX+obstacleRow > x and obstacleX + obstacleRow<x+playerRow):
          crash()  
    drawObject(player,x,y)
    #총알이 위로 올라가는 것을 표현
    if len (shootXY) != 0 :
      for sxy in shootXY:
        sxy[1] -= 5
        if sxy[1]<=0:
          try:
            shootXY.remove(sxy)
          except ValueError:
            continue
      #장애물이 총알에 맞았을 때
      if sxy[1] < obstacleY and sxy[1] < obstacleY+obstacleCol:
        if sxy[0]>obstacleX-3 and sxy[0]<obstacleX+obstacleRow:
          try:
            shootXY.remove(sxy)
            crush=True
            crushCount += 1
            totalCount += 1
          except:
            pass
      #부수면 안되는 객체가 총에 맞았을 때
      if sxy[1] < allyY and sxy[1] < allyY+allyCol:
        if sxy[0]>allyX-3 and sxy[0]<allyX+allyRow:
          try:
            shootXY.remove(sxy)
            passCount += 1
            totalCount += 1
            crush1=True
            if passCount == 3:
              fault()  
          except:
            pass        

    if len(shootXY) !=0:
      for sx , sy in shootXY:
        drawObject(shooter, sx,sy)
    #장애물이 사선으로 튀도록 조정
    obstacleX += obstacleRowSpeed
    obstacleY += obstacleColSpeed
    #장애물이 벽을 튕김
    if obstacleX <0 or obstacleX > WINDOW_ROW -obstacleRow:
      obstacleRowSpeed=-obstacleRowSpeed
    #장애물이 바닥을 통과 했을 때
    if obstacleY > WINDOW_COL:
      obstacleX=random.randrange(0,WINDOW_ROW-obstacleRow)
      obstacleY=0
      obstacleRowSpeed=random.randrange(-3,3)
      passCount += 1
      totalCount += 1
      if passCount == 3:
        fault()

    if allyY > WINDOW_COL-55:
      allyY=-20000000000 
 
    #장애물을 부쉈을 때
    if crush:
      drawObject(boom,obstacleX,obstacleY)
      crushSound.play()
      obstacleSize=obstacle.get_rect().size
      obstacleRow=obstacleSize[0]
      obstacleCol=obstacleSize[1]
      obstacleX=random.randrange(0,WINDOW_ROW-obstacleRow)
      obstacleY=0  
      #장애물 파괴시 속도 증가
      obstacleColSpeed += 0.1
      if obstacleColSpeed>10:
        obstacleColSpeed=10
      obstacleRowSpeed=random.randrange(-3,3)
      crush=False
    if crush1:
      drawObject(boom,obstacleX,obstacleY)
      screamSound.play()
      allySize=ally.get_rect().size
      allyRow=allySize[0]
      allyCol=allySize[1]
      allyX=random.randrange(0,WINDOW_ROW-allyRow)
      allyY=-80  
      crush1=False

    writeFault(passCount)  
    writeCrush(crushCount) 
    helpCounter(helpCount) 
    drawObject(obstacle,obstacleX,obstacleY)
    #부수면 안 되는 객체 추가:
    allyY += allyColSpeed
    if crushCount % 10 ==0 and totalCount != 0:
      allyX=random.randrange(0,WINDOW_ROW-allyRow)
      allyY=-80
    drawObject(ally,allyX,allyY)  



    pygame.display.update()

    clock.tick(60)

  pygame.quit         

pyGame()
runGame()
