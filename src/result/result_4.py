# n x m 넓이의 미로
n, m = 5, 10

# 방향 값 (상,하,좌,우)
상, 하, 좌, 우 = 0, 1, 2, 3

# 시작 인덱스
startX = 1
startY = 1

# 미로 2차원 배열
maze_load = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# 함수 안에 코드를 작성하여 움직일 방향을 리스트로 반환하세요.


def solution():
    way = []

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    x, y = startX, startY
    maze_load[x][y] += 10

    while True:
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 0 or ny < 0 or nx >= n or ny >= m:
                continue

            if maze_load[nx][ny] == 0:
                continue

            if maze_load[nx][ny] == 1:
                way.append(i)
                x = nx
                y = ny
                maze_load[x][y] += 10

            if maze_load[nx][ny] == 2:
                way.append(i)
                return way
