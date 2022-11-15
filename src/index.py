import sys
import time
import binascii

import tb as traceback
import javascript

from browser import document, html, window, console, bind, websocket
import browser.widgets.dialog as dialog

import maze

javascript.import_js("maze.js", alias="js_module")

defaultCode = maze.get_maze_text()


def reset_src():
    if "code" in document.query:
        code = document.query.getlist("code")[0]
        editor.setValue(code)
    else:
        if storage is not None and "py_src" in storage:
            editor.setValue(storage["py_src"])
        else:
            editor.setValue(defaultCode)
        if "py_test" in storage and "files" in document:
            document["files"].selectedIndex = int(storage["py_test"])
    editor.scrollToRow(0)
    editor.gotoLine(0)


def reset_src_area():
    if storage and "py_src" in storage:
        editor.value = storage["py_src"]
    else:
        editor.value = defaultCode


def reset_editor():
    maze.reset_maze()

    if has_ace:
        reset_src()
    else:
        reset_src_area()


maze.draw_board()

maze.load_maze()


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

    result_soultion = solution()
    maze.move(result_soultion)

    print(f"<completed in {((time.perf_counter() - t0) * 1000.0):6.2f} ms>")

    return state

    # Clear output and restart turtle


def btn_clear_click(*args):
    document["console"].value = ""

    maze.reset_maze()
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
_height_editor = int(document.documentElement.clientHeight)
_height_console = int(document.documentElement.clientHeight - 467)
_height_maze = int(document.documentElement.clientHeight - 300)
document["editor"].style.height = f"{_height_editor}px"
document["console"].style.height = f"{_height_console}px"
document["maze-div"].style.height = f"{_height_maze}px"

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
