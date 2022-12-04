# n x m 넓이의 미로
n, m = 3, 10

# 방향 리스트 (상,하,좌,우)
상, 하, 좌, 우 = 0, 1, 2, 3

# 시작 인덱스
startX = 1
startY = 1

# 미로 2차원 배열
maze_load = [
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 3, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# 함수 안에 코드를 작성하여 움직일 방향을 리스트로 반환하세요.


def solution():
    way = []

    for j in range(1, m, 1):
        if maze_load[1][j] == 0:
            way.append(상)
        else:
            way.append(우)

    return way
