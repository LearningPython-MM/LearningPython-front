var $module = {
    load_maze: function fx(maze, x, y, path, time, totalScore, noti) {
        buildTime = time
        score = totalScore
        messege = noti
        move(maze, x, y, path)
    }
}

var buildTime = 0.0
var score = 0
var messege = ""

var map = [[]]
var nowX = 0
var nowY = 0
var refreshIntervalId = ""

function move(maze, x, y, path) {
    var result = false
    map = maze
    nowX = x
    nowY = y

    var pathList = Object.values(path)

    var i = 0;

    refreshIntervalId = setInterval(function run() {
        result = move_player(pathList, i++);
    }, 300);
}

function move_player(pathList, i) {
    if (i >= pathList.length) {
        judge_game(false)
        return
    }

    var direction = pathList[i]

    if (direction == 0) {
        map[nowX][nowY] = 1;
        change_image(nowX, nowY, "waterballun")

        nowX -= 1;

        if (map[nowX][nowY] == 0) {
            nowX += 1;
        }
        else if (map[nowX][nowY] == 2) {
            map[nowX][nowY] = 3;
            judge_game(true)
        }

        map[nowX][nowY] = 3;
        change_image(nowX, nowY, "miggyung");
    }
    // up
    else if (direction == 3) {
        map[nowX][nowY] = 1
        change_image(nowX, nowY, "waterballun")

        nowY += 1

        if (map[nowX][nowY] == 0) {
            nowY -= 1
        }
        else if (map[nowX][nowY] == 2) {
            map[nowX][nowY] = 3
            judge_game(true)
        }

        map[nowX][nowY] = 3
        change_image(nowX, nowY, "miggyung")
    }
    // right
    else if (direction == 2) {
        map[nowX][nowY] = 1
        change_image(nowX, nowY, "waterballun")

        nowY -= 1

        if (map[nowX][nowY] == 0) {
            nowY += 1
        }
        else if (map[nowX][nowY] == 2) {
            map[nowX][nowY] = 3
            judge_game(true)
        }

        map[nowX][nowY] = 3
        change_image(nowX, nowY, "miggyung")
    }  // left

    else if (direction == 1) {
        map[nowX][nowY] = 1
        change_image(nowX, nowY, "waterballun")

        nowX += 1

        if (map[nowX][nowY] == 0) {
            nowX -= 1
        }
        else if (map[nowX][nowY] == 2) {
            map[nowX][nowY] = 3
            judge_game(true)
        }

        map[nowX][nowY] = 3
        change_image(nowX, nowY, "miggyung")
    }  // down
}

function change_image(x, y, imageUrl) {
    var id = "x" + String(x) + "y" + String(y);

    if (imageUrl == "ground") {
        document.getElementById(id).style.display = "none"
    }
    else {
        document.getElementById(id).style.display = "inherit"
        document.getElementById(id).src = "./image/" + imageUrl + ".png";
    }
}

function judge_game(result) {
    clearInterval(refreshIntervalId)

    show_result_modal(result, score)
}

function show_result_modal(result, score) {
    if (result) {
        document.getElementById("modal-title").textContent = "미로 탈출 성공 🥳 "
        document.getElementById("maze-score").textContent = "코드 점수: " + score
        if (messege == "") {
            document.getElementById("maze-time").textContent = "소요 시간: " + buildTime + "초"
        } else {
            document.getElementById("maze-time").textContent = "다음엔 점수를 더 올려보는거 어때요?"
        }
    } else {
        document.getElementById("modal-title").textContent = "미로 탈출 실패 😢 "
        document.getElementById("maze-score").textContent = "코드 점수: " + score
        document.getElementById("maze-time").textContent = "다시 도전해 보세용"
    }

    document.getElementById("maze-noti").innerHTML = messege

    elems = document.getElementById("modal1")
    modal = M.Modal.init(elems, {})
    modal.open()
}