from collections import deque

#  N, M 을 공백으로 구분하여 입력 받기
n, m = 15, 15

# 2차원 리스트의 맵 정보 입력 받기
maze_load = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


# 시작 인덱스
startX = 13
startY = 1

# 방문 기록용 2차원 리스트
check = [[0]*m for _ in range(n)]

# 이동칸 기록용 2차원 리스트
count = [[0]*m for _ in range(n)]

# 상하좌우 이동용 방향
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
directions = [0, 1, 2, 3]

# BFS 소스 코드 구현


def solution():
    # 큐(Queue) 구현을 위해 deque 라이브러리 사용
    queue = deque()
    moveQue = deque()

    queue.append((startX, startY))
    maze_load[startX][startY] = 2
    isNotPop = False

    # 큐가 빌 때까지 반복
    while queue:
        if isNotPop == False and len(moveQue) > 0:
            moveQue.pop()
            if len(queue) > 1:
                moveQue.pop()

        x, y = queue.popleft()

        isNotPop = False

        # 현재 위치에서 4가지 방향으로의 위치 확인
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            # 미로 찾기 공간을 벗어난 경우 무시
            if nx < 0 or ny < 0 or nx >= n or ny >= m:
                continue
            # 0인 경우 괴물이므로 무시
            if maze_load[nx][ny] == 0:
                continue
            # 해당 노드를 처음 방문하는 경우에만 최단 거리 기록
            if maze_load[nx][ny] == 1:
                maze_load[nx][ny] = maze_load[x][y] + 1
                queue.append((nx, ny))
                moveQue.append(i)
                isNotPop = True

    return list(moveQue)


print(solution())
