import javascript
from browser import document, html, window, console, bind, websocket
from browser.widgets.dialog import InfoDialog

jq = window.jQuery

javascript.import_js("maze.js", alias="js_module")

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
    text = "# n x m 넓이의 미로\n"
    text += "n, m = {0}, {1}\n\n".format(n, m)

    text += "# 방향 리스트 (상,하,좌,우)\n"
    text += "direction = [0,1,2,3]\n\n"

    text += "# 시작 인덱스\n"
    text += "startX = {0}\nstartY = {1}\n\n".format(nowX, nowY)

    text += "# 미로 2차원 배열\n"
    text += "maze_load = [\n"

    for i in range(0, len(map), 1):
        text += "    {0}".format(map[i]) + ",\n"

    text += "]\n\n"

    text += "# 코드를 함수 안에 넣어 리스트로 반환하세요.\n"
    text += "def solution():\n"
    # text += "    return [0,1,2,3]"
    text += "    return [0, 0, 0, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0, 2]"

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


def move(path):
    js_module.load_maze(map, nowX, nowY, path)


def show_result_modal(result):
    if result:
        document["modal-title"].text = "미로 탈출 성공 🥳"
    else:
        document["modal-title"].text = "미로 탈출 실패 😢"

    elems = document["modal1"]
    modal = window.M.Modal.init(elems, {})
    modal.open()
