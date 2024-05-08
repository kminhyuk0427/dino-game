import pygame
import random
import sys

# 파이게임 초기화
pygame.init()

# 화면 설정
screen_width = 800 # 화면 가로
screen_height = 300 # 화면 세로
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino Game")

# 색깔 정의
white = (255, 255, 255)
black = (0, 0, 0)

# 공룡 초기 설정
dino_size = 50  # 공룡의 가로세로 크기
dino_x = 50  # 공룡의 초기 x 위치
dino_y = screen_height - dino_size  # 공룡의 초기 y 위치 (바닥에 닿도록 설정)
dino_vel_y = 0  # 공룡의 수직 속도 (점프 및 중력 적용)
gravity = 1  # 중력 가속도 (아래로 떨어지는 속도)
jump_strength = -17   # 점프 세기 (음수 값으로 위쪽으로 이동)
is_jumping = False  # 공룡의 점프 상태 여부를 나타내는 플래그

# 장애물 관련 변수 설정
obstacles = []  # 장애물을 관리하는 리스트
obstacle_speed = -6  # 장애물의 이동 속도 (화면 왼쪽으로 이동)

# 장애물 생성 주기 범위 설정
min_obstacle_interval = 5
max_obstacle_interval = 20

# 다음 장애물 생성까지 카운터 및 주기 초기화
next_obstacle_counter = random.randint(min_obstacle_interval, max_obstacle_interval)

# 장애물 생성 함수
def create_obstacle():
    global next_obstacle_counter

    # 다음 장애물 생성 주기를 랜덤으로 설정
    next_obstacle_counter = random.randint(min_obstacle_interval, max_obstacle_interval)

    # 장애물의 높이와 너비를 랜덤으로 설정
    obstacle_height = random.randint(30, 70)
    obstacle_width = random.randint(20, 40)

    # 장애물의 초기 위치 (화면 오른쪽 밖에서 시작)
    if obstacles:
        last_obstacle = obstacles[-1]
        obstacle_x = last_obstacle.x + random.randint(100, 500)  # 이전 장애물에서 일정 거리 이후에 생성
    else:
        obstacle_x = screen_width + random.randint(100, 500)

    obstacle_y = screen_height - obstacle_height

    # 장애물을 pygame.Rect 객체로 생성하여 리스트에 추가
    obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))

# 게임 루프
clock = pygame.time.Clock()
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_jumping:
            # 스페이스 바를 누르면 공룡이 점프
            is_jumping = True
            dino_vel_y = jump_strength

    # 공룡의 수직 이동 (중력 적용)
    dino_vel_y += gravity
    dino_y += dino_vel_y

    # 공룡이 화면 아래로 떨어지지 않도록 제한
    if dino_y >= screen_height - dino_size:
        dino_y = screen_height - dino_size
        dino_vel_y = 0
        is_jumping = False

    # 장애물 이동 및 관리
    for obstacle in obstacles[:]:
        obstacle.x += obstacle_speed
        # 화면 왼쪽을 벗어나면 장애물 제거
        if obstacle.right < 0:
            obstacles.remove(obstacle)

    # 다음 장애물 생성 주기까지 카운터 감소
    next_obstacle_counter -= 1
    if next_obstacle_counter <= 0:
        create_obstacle()

    # 충돌 체크
    dino_rect = pygame.Rect(dino_x, dino_y, dino_size, dino_size)
    for obstacle in obstacles:
        if dino_rect.colliderect(obstacle):
            running = False  # 게임 종료

    # 화면 그리기
    screen.fill(white)  # 화면을 흰색으로 채우기
    pygame.draw.rect(screen, black, (dino_x, dino_y, dino_size, dino_size))  # 공룡 그리기
    for obstacle in obstacles:
        pygame.draw.rect(screen, black, obstacle)  # 장애물 그리기

    pygame.display.flip()  # 화면 업데이트
    clock.tick(60)  # 프레임 속도 설정 (초당 60프레임)

pygame.quit()  # 파이게임 종료
sys.exit()  # 시스템 종료
