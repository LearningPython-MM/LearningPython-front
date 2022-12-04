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
        if stage.isNeedQueue and (('import deque' in self.src) == False):
            minus += 30
            self.noti += "<p>✅ 큐를 이용해보세요!</p>"

        # 반복문 써야하는데 안쓰면 - 10
        if self.codeLoof < stage.minLoofCnt:
            minus += 30
            self.noti += "<p>✅ 반복문을 {}개 이상 사용해보세요!</p>".format(
                stage.minLoofCnt)

        # 분기문 써야하는데 안쓰면 - 10
        if self.codeCondition < stage.minConditionCnt:
            minus += 30
            self.noti += "<p>✅ 분기문을 {}개 이상 사용해보세요!</p>".format(
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

    _width_maze = int((document.documentElement.clientWidth / 2) - 80)
    width = _width_maze / stage.m

    tag += "<table>"

    for i in range(0, stage.m, 1):
        tag += "<tr>"

        for j in range(0, stage.m, 1):
            tag += "<td width='{}' height='{}'".format(width, width)
            tag += "background='./image/ground.png' style='background-size: cover; padding: 0; margin: 0;'>"
            tag += "    <img id=x{}y{} src='./image/other.png' style='max-width: 100%; display:block;'/>".format(
                i, j)
            tag += "</td>"

        tag += "</tr>"

    tag += "</table>"

    document["maze-div"].innerHTML += tag


def change_image(x, y, imageUrl):
    id = "x{}y{}".format(x, y)
    if imageUrl == "ground":
        document[id].style.display = "none"
    else:
        document[id].style.display = "inherit"
        document[id].src = "./image/{}.png".format(imageUrl)


def load_maze():
    global stage

    for i in range(0, len(stage.map), 1):
        for j in range(0, len(stage.map[i]), 1):
            if (stage.map[i][j] == 0):
                change_image(i, j, "grace")

            elif (i == stage.escapeX and j == stage.escapeY):
                change_image(i, j, "potal")

            elif (i == stage.startX and j == stage.startY):
                change_image(i, j, "miggyung")

            elif (stage.map[i][j] == 1):
                change_image(i, j, "ground")


def erase():
    for i in range(0, stage.n, 1):
        for j in range(0, stage.m, 1):
            change_image(i, j, "ground")


def move(result):
    js_module.load_maze(stage.map, nowX, nowY, result.path,
                        result.buildTime, result.getScore(), result.noti)
