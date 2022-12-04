import javascript
from browser import document, html, window, console, bind, websocket
from browser.widgets.dialog import InfoDialog
import stageList

javascript.import_js("maze.js", alias="js_module")

selectStage = int(document.query['stage'])

stage = stageList.mapList[selectStage]

nowX = stage.startX
nowY = stage.startY


class GameResult:
    maxScore = 100

    def __init__(self, src, time, path):
        self.src = src
        self.buildTime = int(time)
        self.codeLoof = src.count('for') + src.count('while')
        self.codeCondition = src.count('if')
        lines = src.split('\n')

        startLines = src.split('def solution():\n')
        defLines = (startLines[1].split('return'))[0]

        self.codeLines = len(defLines.split('\n'))
        self.path = path
        self.noti = ""

    def getScore(self):
        minus = 0

        # queue를 써야하는데 안쓰면 - 10
        if stage.isNeedQueue & (('import deque' in self.src) == False):
            minus += 30
            self.noti += "\n✅ 큐를 이용해보세요!"

        # 반복문 써야하는데 안쓰면 - 10
        if self.codeLoof < stage.minLoofCnt:
            minus += 30
            self.noti += "\n✅ 반복문을 {}개 이상 사용해보세요!".format(stage.minLoofCnt)

        # 분기문 써야하는데 안쓰면 - 10
        if self.codeCondition < stage.minConditionCnt:
            minus += 30
            self.noti += "\n✅ 분기분을 {}개 이상 사용해보세요!".format(
                stage.minConditionCnt)

        # 코드 줄수 + 루프 수 * 2 + (코드 분기문 + 1)
        codeComplex = 0

        if (self.codeLines - stage.minLines) > 0:
            codeComplex += self.codeLines - stage.minLines
        if (self.codeLoof - stage.minLoofCnt) > 0:
            codeComplex += (self.codeLoof - stage.minLoofCnt) * 2
        if (self.codeCondition - stage.minConditionCnt) > 0:
            codeComplex += (self.codeCondition - stage.minConditionCnt)

        minus += codeComplex

        score = int(GameResult.maxScore - minus)

        if score < 0:
            return 0

        return score


def get_maze_text():
    text = "# n x m 넓이의 미로\n"
    text += "n, m = {0}, {1}\n\n".format(stage.n, stage.m)

    text += "# 방향 값 (상,하,좌,우)\n"
    text += "상, 하, 좌, 우 = 0, 1, 2, 3\n\n"

    text += "# 시작 인덱스\n"
    text += "startX = {0}\nstartY = {1}\n\n".format(nowX, nowY)

    text += "# 미로 2차원 배열\n"
    text += "maze_load = [\n"

    for i in range(0, len(stage.map), 1):
        text += "    {0}".format(stage.map[i]) + ",\n"

    text += "]\n\n"

    text += "# 함수 안에 코드를 작성하여 움직일 방향을 리스트로 반환하세요.\n"
    text += "def solution():\n"
    text += "    way = [상, 하, 좌, 우]\n"
    text += "    return way"

    return text


def reset_maze():
    global nowX, nowY, stage

    stage.map[nowX][nowY] = 1
    stage.map[stage.escapeX][stage.escapeY] = 2

    stage.map[stage.startX][stage.startY] = 3

    nowX = stage.startX
    nowY = stage.startY

    erase()
    load_maze()


def draw_board():
    global stage

    tag = ""

    _width_maze = int((document.documentElement.clientWidth / 2) - 150)
    width = _width_maze / stage.m

    for i in range(0, 15, 1):
        tag += "<table bgcolor='black' border='1'><tr>"

        for j in range(0, stage.m, 1):
            tag += "<td id=x{}y{} width='{}' height='{}'".format(
                i, j, width, width)
            tag += "background='./image/other.png' style='background-size: cover;'>"
            tag += "</td>"

        tag += "</tr></table>"

    document["maze-div"].innerHTML += tag


def change_color(x, y, imageUrl):
    id = "x{}y{}".format(x, y)
    document[id].style.backgroundImage = "url('./image/{}.png')".format(
        imageUrl)


def load_maze():
    global stage

    for i in range(0, len(stage.map), 1):
        for j in range(0, len(stage.map[i]), 1):
            if (stage.map[i][j] == 0):
                change_color(i, j, "grace")

            elif (stage.map[i][j] == 2):
                change_color(i, j, "potal")

            elif (stage.map[i][j] == 3):
                change_color(i, j, "miggyung")

            elif (stage.map[i][j] == 1):
                change_color(i, j, "ground")


def erase():
    for i in range(0, stage.n, 1):
        for j in range(0, stage.m, 1):
            change_color(i, j, "ground")


def move(result):
    js_module.load_maze(stage.map, nowX, nowY, result.path,
                        result.buildTime, result.getScore(), result.noti)
