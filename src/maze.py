from browser import document, html, window, console, bind, websocket

n, m = 15, 15

startX = 13
startY = 1

escapeX = 1
escapeY = 14

nowX = 13
nowY = 1

map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 2],
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
    [0, 3, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def get_maze_text():
    text = "map = [\n"

    for i in range(0, len(map), 1):
        text = text + "    {0}".format(map[i]) + ",\n"

    text = text + "]"
    return text


def reset_maze():
    global map, nowX, nowY

    map[nowX][nowY] = 1
    map[escapeX][escapeY] = 2

    map[startX][startY] = 3

    nowX = startX
    nowY = startY

    erase()
    load_maze()


def draw_board():
    global map

    tag = ""

    for i in range(0, len(map), 1):
        tag += "<table bgcolor='black' border='1'><tr>"
        for j in range(0, len(map[i]), 1):
            tag += "<td id=x{}y{} width='15' height='15'></td>".format(i, j)
        tag += "</tr></table>"

    document["maze-div"].innerHTML += tag


def change_color(x, y, color):
    id = "x{}y{}".format(x, y)
    document[id].style.backgroundColor = color


def load_maze():
    global map

    for i in range(0, len(map), 1):
        for j in range(0, len(map[i]), 1):
            if (map[i][j] == 0):
                change_color(i, j, "#980000")

            elif (map[i][j] == 2):
                change_color(i, j, "#FFFF48")
                # 출구

            elif (map[i][j] == 3):
                change_color(i, j, "#90E4FF")
                # document.getElementById("x"+i+"y"+j).innerHTML = "<img src='Kkobuk.jpg' width='30' height='25'>"

            elif (map[i][j] == 1):
                change_color(i, j, "white")
                # document.getElementById("x"+i+"y"+j).innerHTML = "<img src=''>"


def erase():
    for i in range(0, n, 1):
        for j in range(0, m, 1):
            change_color(i, j, "white")


def move_player(direction):
    global nowX
    global nowY
    global map

    if direction == 0:  # up
        map[nowX][nowY] = 1
        nowX -= 1
        if (map[nowX][nowY] == 0):
            nowX += 1
        elif (map[nowX][nowY] == 2):
            map[nowX][nowY] = 3
            # alert("축하합니다! 클리어하셨습니다.")
        map[nowX][nowY] = 3
        change_color(nowX, nowY, "#FFFF48")

    elif direction == 3:  # right
        map[nowX][nowY] = 1
        nowY += 1
        if (map[nowX][nowY] == 0):
            nowY -= 1
        elif (map[nowX][nowY] == 2):
            map[nowX][nowY] = 3
            # alert("축하합니다! 클리어하셨습니다.")
        map[nowX][nowY] = 3
        change_color(nowX, nowY, "#FFFF48")

    elif direction == 2:  # left
        map[nowX][nowY] = 1
        nowY -= 1
        if (map[nowX][nowY] == 0):
            nowY += 1
        elif (map[nowX][nowY] == 2):
            map[nowX][nowY] = 3
            # alert("축하합니다! 클리어하셨습니다.")
        map[nowX][nowY] = 3
        change_color(nowX, nowY, "#FFFF48")

    elif direction == 1:  # down
        map[nowX][nowY] = 1
        nowX += 1
        if (map[nowX][nowY] == 0):
            nowX -= 1
        elif (map[nowX][nowY] == 2):
            map[nowX][nowY] = 3
            # alert("축하합니다! 클리어하셨습니다.")
        map[nowX][nowY] = 3
        change_color(nowX, nowY, "#FFFF48")


def move(path):
    for p in path:
        move_player(p)
        # 여기에 딜레이,,,
