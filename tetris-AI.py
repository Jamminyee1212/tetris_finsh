#초기 설정
import pygame
import random
import time

pygame.init()

font = pygame.font.SysFont("arial",25,True,True)
'''
블럭 고유 번호:
0: 없음
1: ─┘
2: ㄴ
3: └┐
4: ┌┘
5: ㅗ
6: ㅁ
7: ㅣ
'''
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
BLACK = (0,0,0)

#각종 변수
runcode = True #False가 되면 코드 종료
board = [] #테트리스판 상태 저장
nonrealboard = [] #임시 테트리스판
for i in range(0,10): #x좌표
    board.append([])
    nonrealboard.append([])
    for j in range(0,22): #y좌표
        board[i].append(0)
        nonrealboard[i].append(0)

current_falling_block = 1 #현재 떨어지고 있는 블럭
current_rotation = 1 #현재 떨어지고 있는 블럭의 회전 상태
block_coordinate = [4,3] #떨어지고 있는 블럭 위치
fall_period = 50 #50이 될 때마다 y좌표 감소
add_score = [0,100,300,700,1500] #점수 증가량
realblock = [[0,0],[0,0],[0,0],[0,0]] #실제 블럭 위치
block_log = [0,1,0,0,0,0,0,0] #각 블럭 등장 횟수 (블럭 고유 번호를 x라고 할 때 블럭이 나온 횟수는 block_log[x]로 호출하며, block_log[0]는 아무 의미 없는 칸으로 둠)

nonreal_block_coordinate = [4,3]
nonrealblock = [[0,0],[0,0],[0,0],[0,0]] #실제 블럭 위치

#Player 0 Mode에 필요한 것들 (혹시 txt 파일을 생성하고 그 txt 파일에 데이터를 입력하거나 txt 파일에 있는 데이터를 불러오는 기능을 넣어주면 더 좋을듯. 한마디로 프로그램을 꺼놔도 학습 데이터를 자동으로 영구적으로 저장할 수 있는 수단(txt 파일 등)을 마련해두면 좋겠다는 얘기
generation = 1 #거친 세대 수
generation_number = 0 #한 세대 속 조사할 개체 번호
class Gene():
    def __init__(self):
        self.Cleared_Line_Weight = []
        self.Hole_Weight = []
        self.Bump_Weight = []
        self.Height_Weight = []
        for i in range(0,50):
            self.Cleared_Line_Weight.append(random.randint(0,1000))
            self.Hole_Weight.append(random.randint(-1000,0))
            self.Bump_Weight.append(random.randint(-1000,0))
            self.Height_Weight.append(random.randint(-1000,0))
            
    def SetWeight(self,gene_num,a,b,c,d):
        self.Cleared_Line_Weight[gene_num] = a
        self.Hole_Weight[gene_num] = b
        self.Bump_Weight[gene_num] = c
        self.Height_Weight[gene_num] = d
        
rand_gene = Gene()
best_gene = Gene()
rand_gene.SetWeight(0,794,-883,-127,-152)
rand_gene.SetWeight(1,855,-867,-159,-76)
rand_gene.SetWeight(2,867,-503,-93,-75)
rand_gene.SetWeight(3,767,-699,-102,-121)
rand_gene.SetWeight(4,865,-848,-160,-71)

scorelist = []
for i in range(50):
    scorelist.append(0)
sumHeight = 0
maxHeight = 0
averageHeight = 0
holes = 0
wells = 0
clears = 0 
maxtime = 500000
endloop = 0
bestperform = 0

originalscore = []
for i in range(50): originalscore.append(0)

#블럭 클래스 생성
class Block():
    def __init__(self):
        self.blocklist = [[],[],[],[],[],[],[]]
        self.limitx = [[],[],[],[],[],[],[]]
        
    def SetBlock(self,block_num,info,limitx):
        self.blocklist[block_num-1].append(info)
        self.limitx[block_num-1].append(limitx)

#블럭 생성
tetris_block = Block()
tetris_block.SetBlock(1, [[1,-1], [-1,0], [0,0], [1,0]], [1,8])
tetris_block.SetBlock(1, [[-1,-1], [0,1], [0,0], [0,-1]], [1,9])
tetris_block.SetBlock(1, [[-1,1], [1,0], [0,0], [-1,0]], [1,8])
tetris_block.SetBlock(1, [[1,1], [0,-1], [0,0], [0,1]], [0,8])

tetris_block.SetBlock(2, [[-1,-1], [-1,0], [0,0], [1,0]], [1,8])
tetris_block.SetBlock(2, [[-1,1], [0,1], [0,0], [0,-1]], [1,9])
tetris_block.SetBlock(2, [[1,1], [1,0], [0,0], [-1,0]], [1,8])
tetris_block.SetBlock(2, [[1,-1], [0,-1], [0,0], [0,1]], [0,8])

tetris_block.SetBlock(3, [[-1,-1], [-1,0], [0,0], [0,1]], [1,9])
tetris_block.SetBlock(3, [[-1,1], [0,1], [0,0], [1,0]], [1,8])
tetris_block.SetBlock(3, [[-1,-1], [-1,0], [0,0], [0,1]], [1,9])
tetris_block.SetBlock(3, [[-1,1], [0,1], [0,0], [1,0]], [1,8])

tetris_block.SetBlock(4, [[1,-1], [0,0], [1,0], [0,1]], [0,8])
tetris_block.SetBlock(4, [[-1,-1], [0,0], [0,-1], [1,0]], [1,8])
tetris_block.SetBlock(4, [[1,-1], [0,0], [1,0], [0,1]], [0,8])
tetris_block.SetBlock(4, [[-1,-1], [0,0], [0,-1], [1,0]], [1,8])

tetris_block.SetBlock(5, [[0,-1], [-1,0], [0,0], [1,0]], [1,8])
tetris_block.SetBlock(5, [[-1,0], [0,1], [0,0], [0,-1]], [1,9])
tetris_block.SetBlock(5, [[0,1], [1,0], [0,0], [-1,0]], [1,8])
tetris_block.SetBlock(5, [[1,0], [0,-1], [0,0], [0,1]], [0,8])

tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8])
tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8])
tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8])
tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8])

tetris_block.SetBlock(7, [[0,-2], [0,-1], [0,0], [0,1]], [0,9])
tetris_block.SetBlock(7, [[-2,0], [-1,0], [0,0], [1,0]], [2,8])
tetris_block.SetBlock(7, [[0,-2], [0,-1], [0,0], [0,1]], [0,9])
tetris_block.SetBlock(7, [[-2,0], [-1,0], [0,0], [1,0]], [2,8])

#함수 생성
def displayblock(): #블럭 불러오는 코드 (tetris_block.blocklist에서 기본 정보를 불러오고 중심점 (0,0)을 기준으로 블럭 좌표값 대입하여 블럭 위치 확정)
    for i in range(0,4):
        realblock[i][0]=tetris_block.blocklist[current_falling_block-1][current_rotation-1][i][0]
        realblock[i][1]=tetris_block.blocklist[current_falling_block-1][current_rotation-1][i][1]
    for i in range(0,4):
        realblock[i][0]+=block_coordinate[0]
        realblock[i][1]+=block_coordinate[1]

def nonreal_displayblock(a):
    for i in range(0,4):
        nonrealblock[i][0]=tetris_block.blocklist[current_falling_block-1][a][i][0]
        nonrealblock[i][1]=tetris_block.blocklist[current_falling_block-1][a][i][1]
    for i in range(0,4):
        nonrealblock[i][0]+=nonreal_block_coordinate[0]
        nonrealblock[i][1]+=nonreal_block_coordinate[1]

def checkbelow(): #y좌표 감소시키기 전 아래 체크하는 코드
    for i in range(0,4):
        if realblock[i][1]+1>=22:
            return False
        elif board[realblock[i][0]][realblock[i][1]+1]>0:
            return False
    return True    

def draw_square(COLOR,x,y): #(25 X 25) 사각형 그리기
    if y>=2:
        pygame.draw.rect(screen, COLOR, [25*x, 25*y-50, 25, 25],0)

def clean(a): #좌우&회전 이동 시 이동 이전의 블럭 흔적 지우기
    for i in range(0,10):
        if board[i][realblock[a][1]]<=0:
            board[i][realblock[a][1]]=0
        if realblock[a][1]-1>=0 and board[i][realblock[a][1]-1]<=0:
            board[i][realblock[a][1]-1]=0
        if realblock[a][1]+1<=21 and board[i][realblock[a][1]+1]<=0:
            board[i][realblock[a][1]+1]=0

def block_create(): #블럭 생성
    p = 0
    for j in range(0,block_log[1]+1):
        p += random.randint(2,10)*(-1) #random.randint(a,b): a<=x<=b 인 정수인 난수 x 리턴
    same_P = []
    same_P.append(1)
    new_P = p
    new = 1
        
    for i in range(2,8):
        P = 0
        for j in range(0,block_log[i]+1):
            P += random.randint(2,10)*(-1)
        #print(P,", ",end='')
        if new_P < P:
            same_P = []
            same_P.append(i)
            new_P = P
            new = i
        elif new_P==P:
            same_P.append(i)
    if len(same_P) <= 1:
        block_log[new]+=1
        return new
    else:
        i=random.randrange(0,len(same_P))
        block_log[same_P[i]]+=1
        return same_P[i]

def NewGeneration():
    for i in range(0,5):
        rand_gene.SetWeight(i,best_gene.Cleared_Line_Weight[i],best_gene.Hole_Weight[i],best_gene.Bump_Weight[i],best_gene.Height_Weight[i])
    for i in range(5,50):
        mom = random.randint(0,4)
        dad = random.randint(0,4)
        while mom==dad: dad = random.randint(0,4)
        parents = [mom,dad]
        mutation = random.randint(0,100)
        tend = random.randint(0,2)
        if tend==0: proportion = [random.randint(0,33),random.randint(0,33),random.randint(0,33),random.randint(0,33)]
        elif tend==1: proportion = [random.randint(34,76),random.randint(34,76),random.randint(34,76),random.randint(34,76)]
        elif tend==2: proportion = [random.randint(77,100),random.randint(77,100),random.randint(77,100),random.randint(77,100)]
        if mutation>=5:
            a = best_gene.Cleared_Line_Weight[mom]*proportion[0]+best_gene.Cleared_Line_Weight[dad]*(100-proportion[0])
            a/=100
            new_line = int(a)
            b = best_gene.Hole_Weight[mom]*proportion[1]+best_gene.Hole_Weight[dad]*(100-proportion[1])
            b/=100
            new_hole = int(b)
            c = best_gene.Bump_Weight[mom]*proportion[2]+best_gene.Bump_Weight[dad]*(100-proportion[2])
            c/=100
            new_bump = int(c)
            d = best_gene.Height_Weight[mom]*proportion[3]+best_gene.Height_Weight[dad]*(100-proportion[3])
            d/=100
            new_height = int(d)
        else:
            new_line = random.randint(0,1000)
            new_hole = random.randint(-1000,0)
            new_bump = random.randint(-1000,0)
            new_height = random.randint(-1000,0)
        rand_gene.SetWeight(i,new_line,new_hole,new_bump,new_height)
def CalculateWeight(clear,hole,bump,height):
    if clear>=3:
        a=1
        for i in range(1,clear+1): a*=i
        clear = a
    else:
        return ((rand_gene.Cleared_Line_Weight[generation_number]*clear)+(rand_gene.Hole_Weight[generation_number]*hole)+(rand_gene.Bump_Weight[generation_number]*bump)+(rand_gene.Height_Weight[generation_number]*height))

def Selection():
    for i in range(0,50):
        originalscore[i]=scorelist[i]
    scorelist.sort(reverse=True)
    print("generation ", generation, ": ")
    for i in range(0,5):
        a=0
        while not scorelist[i]==originalscore[a]:
            a+=1
        best_gene.SetWeight(i,rand_gene.Cleared_Line_Weight[a],rand_gene.Hole_Weight[a],rand_gene.Bump_Weight[a],rand_gene.Height_Weight[a])
        print(i,": ",best_gene.Cleared_Line_Weight[i],best_gene.Hole_Weight[i],best_gene.Bump_Weight[i],best_gene.Height_Weight[i], end = ' ')
        print("")
#초기설정
size = [10*25+25+10*25,20*25]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris N")
clock = pygame.time.Clock()

#본 코드
while runcode:
    clock.tick(10000) #1000fps
    #이벤트 감지 코드
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runcode = False

    #AI 스스로 판단
    Will_Placed=[0,0]
    BestWeight=-99999999
    for rotate_type in range(0,4):
        for move in range(tetris_block.limitx[current_falling_block-1][rotate_type][0],tetris_block.limitx[current_falling_block-1][rotate_type][1]+1):
            nonreal_block_coordinate[0]=move
            nonreal_block_coordinate[1]=2
            for x in range(0,10):
                for y in range(0,22): nonrealboard[x][y] = board[x][y]
            endloop_aaaaaa=False
            nonreal_displayblock(rotate_type)
            while True:
                for i in range(0,4):
                    if nonrealblock[i][1]>=22 or nonrealblock[i][0]<0 or nonrealblock[i][0]>9:
                        print("block: ", nonrealblock[i][0], nonrealblock[i][1]+1)
                        print("type: ", current_falling_block)
                    if nonrealblock[i][1]+1>=22 or board[nonrealblock[i][0]][nonrealblock[i][1]+1]>0:
                        endloop_aaaaaa=True
                        break
                if endloop_aaaaaa:
                    break
                nonreal_block_coordinate[1]+=1
                nonreal_displayblock(rotate_type)        
            for i in range(0,4):
                nonrealboard[nonrealblock[i][0]][nonrealblock[i][1]]=current_falling_block
            #제거된 줄 수 세기
            temp_cleared_line=0
            for y in range(6,22):
                filled=True
                while filled:
                    for x in range(0,10):
                        if board[x][y]<=0: filled=False
                    if not filled: break
                    for down in range(y-1,4,-1):
                        for xx in range(0,10): nonrealboard[xx][down+1]=nonrealboard[xx][down]
                    for xx in range(0,10): nonrealboard[xx][4]=0
                    temp_cleared_lines+=1
            #구멍 수 세기
            hole_num=0
            highest = []
            summit = 22
            for x in range(0,10):
                highest.append(22)
                for y in range(5,22):
                    if nonrealboard[x][y]==0:
                        if nonrealboard[x][y-1]>0:
                            totalhole=0
                            for yy in range(y,22):
                                if nonrealboard[x][yy]==0: totalhole+=1
                            hole_num+=totalhole
                            break
                    if nonrealboard[x][y]>0 and y<highest[x]: highest[x]=y
                if highest[x]<summit: summit=highest[x]
            #울퉁불퉁함(bumpiness) 계산
            bumpy=0
            for x in range(0,9):
                a=highest[x]-highest[x+1]
                if a<0: a*=(-1)
                bumpy+=a
            #칸 높이 계산
            summit*=(-1)
            summit+=22
            #가중치 계산
            temp_weight = CalculateWeight(temp_cleared_line,hole_num,bumpy,summit)
            if temp_weight > BestWeight:
                Will_Placed[0] = rotate_type
                Will_Placed[1] = move
                BestWeight=temp_weight
    #가장 좋다고 판단되는 위치에 놓기
    block_coordinate[0] = Will_Placed[1]
    block_coordinate[1] = 2
    current_rotation = Will_Placed[0]+1
    displayblock()
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
        board[realblock[i][0]][realblock[i][1]]=current_falling_block
    scorelist[generation_number]+=10
    endloop+=1
        
    #초기 설정
    screen.fill(WHITE)

    #새 블럭 생성
    for i in range(0,4):
        board[realblock[i][0]][realblock[i][1]]=current_falling_block
    current_falling_block=block_create()
    block_coordinate[0] = 4
    block_coordinate[1] = 3
    current_rotation = 1

    #한 줄 차면 제거
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
    scorelist[generation_number] += add_score[cleared_lines]
    
    #새 개체 트레이닝 or 세대교체
    end=False
    for h in range(0,5):
        for x in range(0,10):
            if board[x][h]>0 or endloop>=maxtime:
                if scorelist[generation_number]>bestperform:
                    bestperform = scorelist[generation_number]
                generation_number+=1
                endloop=0
                if generation_number==50:
                    Selection()
                    NewGeneration()
                    generation+=1
                    generation_number=0
                    for i in range(0,50): scorelist[i]=0
                for xx in range(0,10):
                    for yy in range(0,22): board[xx][yy]=0
                end=True
                print(generation, generation_number, ": ", rand_gene.Cleared_Line_Weight[generation_number], rand_gene.Hole_Weight[generation_number], rand_gene.Bump_Weight[generation_number], rand_gene.Height_Weight[generation_number],end = ' ')
                print("")
                print("")
                break
        if end: break
    
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
    
    #스코어 및 정보 표시
    score_text = font.render("Score : " + str(scorelist[generation_number]), True, BLACK)
    screen.blit(score_text,(300,75))
    gen_text = font.render("Generation : " + str(generation) + "(" + str(generation_number) + ")", True, BLACK)
    screen.blit(gen_text,(300,170))
    best_text = font.render("Best Gene : " + str(bestperform), True, BLACK)
    screen.blit(best_text,(300,265))
    
    pygame.display.flip()
#종료

pygame.quit()
