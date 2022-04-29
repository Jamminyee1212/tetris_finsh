#초기 설정
import pygame
import random
import time

pygame.init()

font = pygame.font.SysFont("arial",30,True,True)

#색상설정
GRAY = (128,128,128) #테두리
WHITE = (255,255,255) #0
ORANGE = (255,128,0) #1 (─┘)
BLUE  = (0,0,255) #2 (ㄴ)
GREEN = (0,255,0) #3 (└┐)
RED   = (255,0,0) #4 (┌┘)
PURPLE = (127,0,255) #5 (ㅗ)
YELLOW = (255,255,0) #6 (ㅁ)
SKYBLUE = (102,255,255) #7 (ㅣ)
LIGHTGRAY = (224,224,224)
BLACK = (0,0,0)

#각종 변수
runcode = True #False가 되면 코드 종료
press_a=0 #a가 눌린 횟수
score=0 #점수
board = [] #테트리스판 상태 저장
for i in range(0,10): #x좌표
    board.append([])
    for j in range(0,22): #y좌표
        board[i].append(0)
current_rotation = 1 #현재 떨어지고 있는 블럭의 회전 상태
block_coordinate = [4,3] #떨어지고 있는 블럭 위치
fall_period = 50 #50이 될 때마다 y좌표 감소
hard_drop = False #하드 드랍 유무 (하드드랍은 블럭이 바닥에 닿았을 때 딜레이가 생기지 않고 바로 배치됨)
add_score = [0,100,300,700,1500] #점수 증가량
realblock = [[0,0],[0,0],[0,0],[0,0]] #실제 블럭 위치
block_log = [0,0,0,0,0,0,0,0] #각 블럭 등장 횟수 (블럭 고유 번호를 x라고 할 때 블럭이 나온 횟수는 block_log[x]로 호출하며, block_log[0]는 아무 의미 없는 칸으로 둠)
block_weight = [0,0,0,0,0,0,0,0]
notdropped = [0,0,0,0,0,0,0,0]
sameblock = 0 #동일한 블럭 연속으로 2회 등장 시 3회부터는 그 블럭이 나올 수 없게 하는 변수 
newblock_list = [0,0,0] #떨어질 블럭

'''호출 형식: board[x좌표][y좌표]'''

#블럭 클래스 생성
class Block():
    def __init__(self):
        self.blocklist = [[],[],[],[],[],[],[]]
        self.limitx = [[],[],[],[],[],[],[]]
        self.limity = [[],[],[],[],[],[],[]]
        
    def SetBlock(self,block_num,info,limitx,limity):
        self.blocklist[block_num-1].append(info)
        self.limitx[block_num-1].append(limitx)
        self.limity[block_num-1].append(limity)


#블럭 생성
tetris_block = Block()
tetris_block.SetBlock(1, [[1,-1], [-1,0], [0,0], [1,0]], [1,8], 0)
tetris_block.SetBlock(1, [[-1,-1], [0,1], [0,0], [0,-1]], [1,9], 1)
tetris_block.SetBlock(1, [[-1,1], [1,0], [0,0], [-1,0]], [1,8], 1)
tetris_block.SetBlock(1, [[1,1], [0,-1], [0,0], [0,1]], [0,8], 1)

tetris_block.SetBlock(2, [[-1,-1], [-1,0], [0,0], [1,0]], [1,8], 0)
tetris_block.SetBlock(2, [[-1,1], [0,1], [0,0], [0,-1]], [1,9], 1)
tetris_block.SetBlock(2, [[1,1], [1,0], [0,0], [-1,0]], [1,8], 1)
tetris_block.SetBlock(2, [[1,-1], [0,-1], [0,0], [0,1]], [0,8], 1)

tetris_block.SetBlock(3, [[-1,-1], [-1,0], [0,0], [0,1]], [1,9], 1)
tetris_block.SetBlock(3, [[-1,1], [0,1], [0,0], [1,0]], [1,8], 0)
tetris_block.SetBlock(3, [[-1,-1], [-1,0], [0,0], [0,1]], [1,9], 1)
tetris_block.SetBlock(3, [[-1,1], [0,1], [0,0], [1,0]], [1,8], 0)

tetris_block.SetBlock(4, [[1,-1], [0,0], [1,0], [0,1]], [0,8], 1)
tetris_block.SetBlock(4, [[-1,-1], [0,0], [0,-1], [1,0]], [1,8], 0)
tetris_block.SetBlock(4, [[1,-1], [0,0], [1,0], [0,1]], [0,8], 1)
tetris_block.SetBlock(4, [[-1,-1], [0,0], [0,-1], [1,0]], [1,8], 0)

tetris_block.SetBlock(5, [[0,-1], [-1,0], [0,0], [1,0]], [1,8], 0)
tetris_block.SetBlock(5, [[-1,0], [0,1], [0,0], [0,-1]], [1,9], 1)
tetris_block.SetBlock(5, [[0,1], [1,0], [0,0], [-1,0]], [1,8], 1)
tetris_block.SetBlock(5, [[1,0], [0,-1], [0,0], [0,1]], [0,8], 1)

tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8], 0)
tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8], 0)
tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8], 0)
tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8], 0)

tetris_block.SetBlock(7, [[0,-2], [0,-1], [0,0], [0,1]], [0,9], 1)
tetris_block.SetBlock(7, [[-2,0], [-1,0], [0,0], [1,0]], [2,8], 0)
tetris_block.SetBlock(7, [[0,-2], [0,-1], [0,0], [0,1]], [0,9], 1)
tetris_block.SetBlock(7, [[-2,0], [-1,0], [0,0], [1,0]], [2,8], 0)

#함수 생성
def displayblock(): #블럭 불러오는 코드 (tetris_block.blocklist에서 기본 정보를 불러오고 중심점 (0,0)을 기준으로 블럭 좌표값 대입하여 블럭 위치 확정)
    for i in range(0,4):
        realblock[i][0]=tetris_block.blocklist[newblock_list[0]-1][current_rotation-1][i][0]
        realblock[i][1]=tetris_block.blocklist[newblock_list[0]-1][current_rotation-1][i][1]
    for i in range(0,4):
        realblock[i][0]+=block_coordinate[0]
        realblock[i][1]+=block_coordinate[1]

def checkbelow(): #y좌표 감소시키기 전 아래 체크하는 코드
    for i in range(0,4):
        '''print(realblock[i][0],",",realblock[i][1]+1)
        print("")'''
        if realblock[i][1]+1>=22:
            return False
        elif board[realblock[i][0]][realblock[i][1]+1]>0:
            return False
    return True

def checkleft(): #왼쪽 체크
    for i in range(0,4):
        if realblock[i][0]-1<0:
            return False
        elif board[realblock[i][0]-1][realblock[i][1]]>0:
            return False
    return True

def checkright(): #오른쪽 체크
    for i in range(0,4):
        if realblock[i][0]+1>9:
            return False
        elif board[realblock[i][0]+1][realblock[i][1]]>0:
            return False
    return True

def checkrotate(): #-90° 돌기 전 블럭이 있는지 없는지 체크
    for i in range(0,4):
        if realblock[i][0]+1>9:
            return False
        elif board[realblock[i][0]+1][realblock[i][1]]>0:
            return False
    return True
        
def downblock(fall): #1초에 한번씩 y좌표 1씩 줄이는 코드
    time.sleep(0.01)
    displayblock()
    if fall>=50:
        if checkbelow():
            for i in range(0,4):
                board[realblock[i][0]][realblock[i][1]]=0
            block_coordinate[1]+=1
            for i in range(0,4):
                board[realblock[i][0]][realblock[i][1]+1]=newblock_list[0]*(-1)
            '''print(newblock_list[0]*(-1))'''
            return True
        else:
            return False
    return True
    

def draw_square(COLOR,x,y): #(25 X 25) 사각형 그리기
    if y>=2:
        pygame.draw.rect(screen, COLOR, [25*x, 25*y-50, 25, 25],0)

def draw_square1(COLOR,S): #(8 X 8) 사각형
    for i in range(0,4): pygame.draw.rect(screen, COLOR, [341+(110*(S-1))+(8*tetris_block.blocklist[newblock_list[seq]-1][0][i][0]),361+(8*tetris_block.blocklist[newblock_list[seq]-1][0][i][1]),8,8])

def clean(a): #좌우&회전 이동 시 이동 이전의 블럭 흔적 지우기
    for i in range(0,10):
        if board[i][realblock[a][1]]<=0:
            board[i][realblock[a][1]]=0
        if realblock[a][1]-1>=0 and board[i][realblock[a][1]-1]<=0:
            board[i][realblock[a][1]-1]=0
        if realblock[a][1]+1<=21 and board[i][realblock[a][1]+1]<=0:
            board[i][realblock[a][1]+1]=0

#블럭 생성
def block_create():
    global block_weight
    #print("[",end='')
    block_weight[1] += random.randint(2,10)*(-1) #random.randint(a,b): a<=x<=b 인 정수인 난수 x 리턴
    #print(p,", ",end='')
    same_P = []
    same_P.append(1)
    new_P = block_weight[1]
    new = 1
        
    for i in range(2,8):
        block_weight[i] += random.randint(2,10)*(-1)
        #print(P,", ",end='')
        if new_P < block_weight[i]:
            #print(new," ",i,"\n",new_P," < ",block_weight[i],"\n")
            same_P = []
            same_P.append(i)
            new_P = block_weight[i]
            new = i
        elif new_P==block_weight[i]:
            same_P.append(i)
    #print("]")
    #print("[",end='')
    for i in range(1,8):
        pass
        #print(block_weight[i],", ",end='')
    #print("]")
    for i in range(1,8): notdropped[i]+=1
    if len(same_P) <= 1:
        block_log[new]+=1
        if newblock_list[1]==newblock_list[2]: block_weight[new]-=8
        else: block_weight[new]-=5
        notdropped[new]=0
        for a in range(1,8):
            if notdropped[a]>10: block_weight[a]+=10
        return new
    else:
        i=random.randrange(0,len(same_P))
        block_log[same_P[i]]+=1
        if newblock_list[1]==newblock_list[2]: block_weight[same_P[i]]-=8
        else: block_weight[same_P[i]]-=5
        notdropped[same_P[i]]=0
        for a in range(1,8):
            if notdropped[a]>10: block_weight[a]+=10
        return same_P[i]
            

#초기설정
size = [10*25+25+10*25,20*25]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris 1")
clock = pygame.time.Clock()

newblock_list[0] = random.randint(1,7)
block_log[newblock_list[0]]+=1
for i in range(1,3):
    newblock_list[i] = block_create()

#본 코드
while runcode:
    clock.tick(100) #100fps
    #이벤트 감지 코드
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runcode = False
            
        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT and not hard_drop: # 왼쪽 키 입력
                if checkleft():
                    for i in range(0,4):
                        clean(i)
                    block_coordinate[0]-=1
                    '''print("left move:",block_coordinate)'''
                    displayblock()
                    for i in range(0,4):
                        board[realblock[i][0]][realblock[i][1]]=newblock_list[0]*(-1)
                
            elif event.key == pygame.K_RIGHT and not hard_drop: # 오른쪽 키 입력
                '''print("limit right: ",tetris_block.limitx[newblock_list[0]-1][current_rotation-1][1])'''
                if checkright():
                    for i in range(0,4):
                        clean(i)
                    block_coordinate[0]+=1
                    '''print("right move:",block_coordinate)'''
                    displayblock()
                    for i in range(0,4):
                        board[realblock[i][0]][realblock[i][1]]=newblock_list[0]*(-1)
              
            elif event.key == pygame.K_SPACE: # 하드드롭
                for i in range(0,4):
                    clean(i)
                endloop_aaaaa=False
                while True:
                    for i in range(0,4):
                        if realblock[i][1]+1>=22 or board[realblock[i][0]][realblock[i][1]+1]>0:
                            endloop_aaaaa=True
                            break
                    if endloop_aaaaa:
                        break
                    block_coordinate[1]+=1
                    displayblock()
                for i in range(0,4):
                    board[realblock[i][0]][realblock[i][1]]=newblock_list[0]
                score+=10
                hard_drop=True
            
            elif event.key == pygame.K_UP: # 회전
                if 1: #완성되면 checkrotate() 넣기
                    current_rotation+=1
                if current_rotation==5:
                    current_rotation=1
                for i in range(0,4):
                    clean(i)
                before=current_rotation-1
                if before==0:
                    before=4
                if block_coordinate[0]==tetris_block.limitx[newblock_list[0]-1][before-1][0]:
                    if(tetris_block.limitx[newblock_list[0]-1][before-1][0]<tetris_block.limitx[newblock_list[0]-1][current_rotation-1][0]):
                        block_coordinate[0]+=tetris_block.limitx[newblock_list[0]-1][current_rotation-1][0]-tetris_block.limitx[newblock_list[0]-1][before-1][0]

                if block_coordinate[0]==tetris_block.limitx[newblock_list[0]-1][before-1][1]:
                    if(tetris_block.limitx[newblock_list[0]-1][before-1][1]>tetris_block.limitx[newblock_list[0]-1][current_rotation-1][1]):
                        block_coordinate[0]+=tetris_block.limitx[newblock_list[0]-1][current_rotation-1][1]-tetris_block.limitx[newblock_list[0]-1][before-1][1]

                displayblock()
                for i in range(0,4):
                    board[realblock[i][0]][realblock[i][1]]=newblock_list[0]*(-1)

    #초기 설정
    screen.fill(WHITE)
            

    #블럭 드롭 or 생성
    if downblock(fall_period) and not hard_drop: #블럭 정착
      if fall_period>=50:
          fall_period=0
      fall_period+=1

    else: #새 블럭 생성
      for i in range(0,4):
          board[realblock[i][0]][realblock[i][1]]=newblock_list[0]
      for i in range(0,2): newblock_list[i] = newblock_list[i+1]
      newblock_list[2]=block_create()
      '''print("new_block: ",newblock_list[0])'''
      block_coordinate[0] = 4
      block_coordinate[1] = 3
      if newblock_list[0] == 3 or newblock_list[0] == 4 or newblock_list[0] == 7:
          block_coordinate[1]=2
      current_rotation = 1
      hard_drop=False
      fall_period=50

    #한 줄 차면 제거 & 게임오버 표시
    for x in range(0,10):
        if board[x][4]>0:
            runcode = False
    cleared_lines=0
    for y in range(5,22):
        filled=True
        while filled:
            for x in range(0,10):
                if board[x][y]<=0:
                    filled=False
            if not filled:
                break
            for down in range(y-1,4,-1):
                for xx in range(0,10): 
                    board[xx][down+1]=board[xx][down]
            for xx in range(0,10): 
                board[xx][4]=0
            cleared_lines+=1
    score += add_score[cleared_lines]
    #칸 정보 표시 (+디자인)
    for y in range(0,20):
        for x in range(0,10):
            if board[x][y+2] == 0:
                draw_square(WHITE,x,y)

    pygame.draw.rect(screen, GRAY, [0, 450, 250, 50],0)
    pygame.draw.rect(screen, GRAY, [0, 0, 250, 25],0)
    
    for y in range(0,20):
        for x in range(0,10):
            if board[x][y+2] == 1 or board[x][y+2] == -1: #1번 블럭
                draw_square(ORANGE,x,y)
            elif board[x][y+2] == 2 or board[x][y+2] == -2: #2번 블럭
                draw_square(BLUE,x,y)
            elif board[x][y+2] == 3 or board[x][y+2] == -3: #3번 블럭
                draw_square(GREEN,x,y)
            elif board[x][y+2] == 4 or board[x][y+2] == -4: #4번 블럭
                draw_square(RED,x,y)
            elif board[x][y+2] == 5 or board[x][y+2] == -5: #5번 블럭
                draw_square(PURPLE,x,y)
            elif board[x][y+2] == 6 or board[x][y+2] == -6: #6번 블럭
                draw_square(YELLOW,x,y)
            elif board[x][y+2] == 7 or board[x][y+2] == -7: #7번 블럭
                draw_square(SKYBLUE,x,y)

    pygame.draw.rect(screen, GRAY, [0, 0, 1, 500],0)
    pygame.draw.rect(screen, GRAY, [249, 0, 1, 500],0)
    for x in range(1,10):
        pygame.draw.rect(screen, GRAY, [25*x-1, 0, 2, 500],0)
    for y in range(1,20):
        pygame.draw.rect(screen, GRAY, [0, 25*y-1, 250, 2],0)
    pygame.draw.rect(screen, BLACK, [250, 0, 25, 500])

    #다음 블럭 표시
    score_text = font.render("Next Block: ", True, BLACK)
    screen.blit(score_text,(300,270))
    pygame.draw.rect(screen, GRAY, [315, 335, 60, 60])
    pygame.draw.rect(screen, LIGHTGRAY, [325, 345, 40, 40])
    pygame.draw.rect(screen, GRAY, [425, 335, 60, 60])
    pygame.draw.rect(screen, LIGHTGRAY, [435, 345, 40, 40])

    for seq in range(1,3):
        if newblock_list[seq] == 1:
            draw_square1(ORANGE,seq)
        elif newblock_list[seq] == 2:
            draw_square1(BLUE,seq)
        elif newblock_list[seq] == 3:
            draw_square1(GREEN,seq)
        elif newblock_list[seq] == 4:
            draw_square1(RED,seq)
        elif newblock_list[seq] == 5:
            draw_square1(PURPLE,seq)
        elif newblock_list[seq] == 6:
            draw_square1(YELLOW,seq)
        elif newblock_list[seq] == 7:
            pygame.draw.rect(screen, SKYBLUE, [341+(110*(seq-1)),353,8,24])
    #스코어 시스템
    score_text = font.render("Score : " + str(score), True, BLACK)
    screen.blit(score_text,(300,75))

    pygame.display.flip()

#종료
pygame.quit()
