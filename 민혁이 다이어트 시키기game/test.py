import pygame
import random
import sys

# 파이게임 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("민혁이 다이어트 시키기")

# 색깔 정의
white = (255, 255, 255)
red = (150, 0, 0)
black = (0, 0, 0)

# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 순위표 파일 이름
rank_file = "diet_rank.txt"

# 순위표 읽기
def read_rank():
    try:
        with open(rank_file, "r") as file:
            return [float(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return []

# 순위표 업데이트
def update_rank(diet_value):
    rank = read_rank()
    rank.append(diet_value)
    rank.sort()
    rank = rank[:5]  # 상위 5개만 유지
    with open(rank_file, "w") as file:
        for item in rank:
            file.write(f"{item:.1f}\n")

# 순위표 표시 함수
def show_rank():
    rank = read_rank()
    rank_text = font.render("Rank", True, black)
    screen.blit(rank_text, (650, 15))
    y = 35
    for i, item in enumerate(rank, start=1):
        rank_entry = font.render(f"{i}. {item:.1f}kg", True, black)
        screen.blit(rank_entry, (650, y))
        y += 25

# 민혁 초기 설정
mh_size = 60            # 민혁 캐릭터의 크기 (가로 및 세로 길이)
mh_x = 60               # 민혁 캐릭터의 초기 x 좌표
mh_y = screen_height - mh_size  # 민혁 캐릭터의 초기 y 좌표 (화면 하단)
mh_vel_y = 0            # 민혁 캐릭터의 수직 속도
gravity = 1             # 중력 가속도
jump_strength = -18     # 민혁이 점프 시 수직 방향으로 가해지는 힘
is_jumping = False      # 현재 민혁이 점프 중인지 여부를 나타내는 플래그

# 민혁 이미지 로드 및 크기 조정
mh_image = pygame.image.load("minhyuk.png")
mh_image = pygame.transform.scale(mh_image, (mh_size, mh_size))

# 햄버거 이미지 로드
burger_image = pygame.image.load("burger.png")

# 배경 이미지 로드 및 크기 조정
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# 배경 음악 로드 및 반복 재생 설정
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1)  # -1은 무한 반복 재생

# 점프 소리 로드
jump_sound = pygame.mixer.Sound("jump_sound.wav")

# 햄버거 관련 변수 설정
burgers = []
burger_speed = -6

# 장애물 생성 주기 범위 설정
min_burger_interval = 5
max_burger_interval = 20

# 다음 햄버거 생성까지 카운터 및 주기 초기화
next_burger_counter = random.randint(min_burger_interval, max_burger_interval)

# 다이어트 수치 초기값 및 업데이트 주기 설정
diet_value = 98.2
diet_update_interval = 250  # 0.25초마다 업데이트
last_diet_update_time = pygame.time.get_ticks()

# 햄버거 생성 함수
def create_burger():
    burger_height = random.randint(35, 65)
    burger_width = random.randint(25, 40)
    burger_x = screen_width + random.randint(250, 550)
    burger_y = screen_height - burger_height

    if burgers:
        last_burger = burgers[-1][0]
        burger_x = last_burger.x + random.randint(250, 550)

    burger_rect = pygame.Rect(burger_x, burger_y, burger_width, burger_height)
    burger_img = pygame.transform.scale(burger_image, (burger_width, burger_height))
    burgers.append((burger_rect, burger_img))

# 게임 루프
clock = pygame.time.Clock()
running = True
start_time = pygame.time.get_ticks()

while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_jumping:
            is_jumping = True
            mh_vel_y = jump_strength
            # 점프 소리 재생
            jump_sound.play()

    # 민혁의 수직 이동 (중력 적용)
    mh_vel_y += gravity
    mh_y += mh_vel_y

    if mh_y >= screen_height - mh_size:
        mh_y = screen_height - mh_size
        mh_vel_y = 0
        is_jumping = False

    # 햄버거 이동 및 관리
    for burger in burgers[:]:
        burger[0].x += burger_speed
        if burger[0].right < 0:
            burgers.remove(burger)

    # 다음 햄버거 생성 주기까지 카운터 감소
    next_burger_counter -= 1
    if next_burger_counter <= 0:
        create_burger()
        next_burger_counter = random.randint(min_burger_interval, max_burger_interval)

    # 충돌 체크
    mh_rect = pygame.Rect(mh_x, mh_y, mh_size, mh_size)
    for burger in burgers:
        if mh_rect.colliderect(burger[0]):
            print(f"민혁이 몸무게: {diet_value:.1f}kg")
            update_rank(diet_value)  # 게임 종료 시 순위표 갱신
            running = False

    # 다이어트 수치 업데이트(0.25초마다 0.1씩 감소)
    current_time = pygame.time.get_ticks()
    if (current_time - last_diet_update_time) >= diet_update_interval:
        diet_value -= 0.1 
        last_diet_update_time = current_time
        #현재 시간과 수치 업뎃 시간 사이가 업뎃 주기시간 이상인지 봄

    # 1초마다 햄버거 속도 증가
    if (current_time - start_time) >= 1000:
        burger_speed -= 0.05
        start_time = current_time

    # 화면 그리기
    screen.blit(background_image, (0, 0)) # 사진 넣기
    screen.blit(mh_image, (mh_x, mh_y)) # 캐릭터
    for burger in burgers: #햄버거가 리스트 안에 잇으면 사진 적용
        screen.blit(burger[1], (burger[0].x, burger[0].y))
 
    # 몸무게 넣음
    diet_text = font.render(f"{diet_value:.1f}kg", True, red)
    screen.blit(diet_text, (240, 56))

    # 순위표 표시
    show_rank()

    pygame.display.flip()
    clock.tick(60)#프레임

pygame.quit()
sys.exit()
