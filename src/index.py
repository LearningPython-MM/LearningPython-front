import sys
import time
import binascii

import tb as traceback
import javascript

from browser import document, html, window, console, bind, websocket
import browser.widgets.dialog as dialog
from browser import timer

nowX = 13
nowY = 1
map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 3, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


def reset_src():
    if "code" in document.query:
        code = document.query.getlist("code")[0]
        editor.setValue(code)
    else:
        if storage is not None and "py_src" in storage:
            editor.setValue(storage["py_src"])
        else:
            editor.setValue("def solution():\n    return [0,1,2,3]")
        if "py_test" in storage and "files" in document:
            document["files"].selectedIndex = int(storage["py_test"])
    editor.scrollToRow(0)
    editor.gotoLine(0)


def reset_src_area():
    if storage and "py_src" in storage:
        editor.value = storage["py_src"]
    else:
        editor.value = "def solution():\n    return [0,1,2,3]"


def reset_editor():
    if has_ace:
        reset_src()
    else:
        reset_src_area()


def draw_board():
    global map

    tag = ""

    for i in range(0, len(map), 1):
        tag += "<table bgcolor='black' border='1'><tr>"
        for j in range(0, len(map[i]), 1):
            tag += "<td id=x{}y{} width='15' height='15'></td>".format(i, j)
        tag += "</tr></table>"

    document["maze-div"].innerHTML += tag


draw_board()


def change_color(x, y, color):
    id = "x{}y{}".format(x, y)
    document[id].style.backgroundColor = color


def load_maze():
    global map

    for i in range(0, len(map), 1):
        for j in range(0, len(map[i]), 1):
            if (map[i][j] == 1):
                change_color(i, j, "#980000")
                # 벽돌

            elif (map[i][j] == 2):
                change_color(i, j, "#FFFF48")
                # 출구

            elif (map[i][j] == 3):
                change_color(i, j, "#90E4FF")
                # document.getElementById("x"+i+"y"+j).innerHTML = "<img src='Kkobuk.jpg' width='30' height='25'>"

            elif (map[i][j] == 0):
                change_color(i, j, "white")
                # document.getElementById("x"+i+"y"+j).innerHTML = "<img src=''>"


def erase():
    for i in range(0, 15, 1):
        for j in range(0, 15, 1):
            change_color(i, j, "white")


load_maze()


def move_player(direction):
    global nowX
    global nowY
    global map

    if direction == 0:  # up
        map[nowX][nowY] = 0
        nowX -= 1
        if (map[nowX][nowY] == 1):
            nowX += 1
        elif (map[nowX][nowY] == 2):
            alert("축하합니다! 클리어하셨습니다.")
        map[nowX][nowY] = 3

    elif direction == 2:  # right
        map[nowX][nowY] = 0
        nowY += 1
        if (map[nowX][nowY] == 1):
            nowY -= 1
        elif (map[nowX][nowY] == 2):
            alert("축하합니다! 클리어하셨습니다.")
        map[nowX][nowY] = 3

    elif direction == 3:  # left
        map[nowX][nowY] = 0
        nowY -= 1
        if (map[nowX][nowY] == 1):
            nowY += 1
        elif (map[nowX][nowY] == 2):
            alert("축하합니다! 클리어하셨습니다.")
        map[nowX][nowY] = 3

    elif direction == 1:  # down
        map[nowX][nowY] = 0
        nowX += 1
        if (map[nowX][nowY] == 1):
            nowX -= 1
        elif (map[nowX][nowY] == 2):
            alert("축하합니다! 클리어하셨습니다.")
        map[nowX][nowY] = 3

    erase()
    load_maze()


def move(path):
    for p in path:
        move_player(p)
        # 여기서 딜레이를 줘야함,,,


def btn_run_click(*args):
    document["console"].value = ""
    src = editor.getValue()
    if storage is not None:
        storage["py_src"] = src

    t0 = time.perf_counter()

    try:
        ns = {"__name__": "__main__"}
        exec(src, ns, globals())
        state = 1
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        state = 0

    sys.stdout.flush()

    result_soultion = solution_test()
    move(result_soultion)

    print(f"<completed in {((time.perf_counter() - t0) * 1000.0):6.2f} ms>")

    return state

    # Clear output and restart turtle


def btn_clear_click(*args):
    document["console"].value = ""

    # Switch between Light and Dark mode


def btn_brightness_click(*args):
    if document["btn_brightness"].lastChild.text == "brightness_4":
        document["btn_brightness"].lastChild.text = "brightness_5"
        editor.setTheme("ace/theme/chrome")
    else:
        document["btn_brightness"].lastChild.text = "brightness_4"
        editor.setTheme("ace/theme/dracula")


class cOutput:
    encoding = "utf-8"

    def __init__(self):
        self.cons = document["console"]
        self.buf = ""

    def write(self, data):
        self.buf += str(data)

    def flush(self):
        self.cons.value += self.buf
        self.buf = ""

    def __len__(self):
        return len(self.buf)


# console.log(window.M)

# from interpreter import Interpreter
# Interpreter(globals=globals())

# Set height of editor_container to fit the screen
_height = int(document.documentElement.clientHeight - 205)
document["editor"].style.height = f"{_height}px"
document["console"].style.height = f"{_height}px"
document["maze-div"].style.height = f"{_height}px"

try:
    editor = window.ace.edit("editor")
    editor.setTheme("ace/theme/dracula")
    editor.session.setMode("ace/mode/python")
    editor.focus()
    editor.setOptions(
        {
            "enableLiveAutocompletion": True,
            "highlightActiveLine": True,
            "highlightSelectedWord": True,
        }
    )

    has_ace = True
except:
    editor = html.TEXTAREA(rows=20, cols=70)
    document["editor"] <= editor

    def get_value():
        return editor.value

    def set_value(x):
        editor.value = x

    editor.getValue = get_value
    editor.setValue = set_value

    has_ace = False

    # Expose editor to glabal environment, so it can be tuned on the fly
window.editor = editor

if hasattr(window, "localStorage"):
    from browser.local_storage import storage
else:
    storage = None

if "set_debug" in document:
    __BRYTHON__.debug = int(document["set_debug"].checked)

if "console" in document:
    cOut = cOutput()
    sys.stdout = cOut
    sys.stderr = cOut

reset_editor()

document["btn_run"].bind("click", lambda *args: btn_run_click())
document["btn_clear"].bind("click", lambda *args: btn_clear_click())
document["btn_brightness"].bind("click", lambda *args: btn_brightness_click())

# Must do window.M.AutoInit() after all html being loaded!
window.M.AutoInit()
