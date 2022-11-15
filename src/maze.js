var $module = {
    load_maze: function fx(maze, x, y, path) {
        move(maze, x, y, path)
    }
}

function load_maze(text){
    alert("hi")
}

var map = [[]]
var nowX = 0
var nowY = 0
var refreshIntervalId = ""

function move(maze, x, y, path){
    var result = false
    map = maze
    nowX = x
    nowY = y

    var pathList = Object.values(path)
    
    var i = 0;
    
    refreshIntervalId = setInterval(function run() {
        result = move_player(pathList, i++);
    }, 200);
}

function move_player(pathList, i){
    if (i >= pathList.length){
        show_result_modal(false)
        return
    }

    var direction = pathList[i]

    if (direction == 0) {
        map[nowX][nowY] = 1;
        nowX -= 1;

        if (map[nowX][nowY] == 0){
            nowX += 1;
        }
        else if (map[nowX][nowY] == 2){
            map[nowX][nowY] = 3;
            show_result_modal(true)
        }

        map[nowX][nowY] = 3;
        change_color(nowX, nowY, "#FFFF48");
    }  
    // up
    else if (direction == 3){
        map[nowX][nowY] = 1
        nowY += 1

        if (map[nowX][nowY] == 0){
            nowY -= 1
        }
        else if (map[nowX][nowY] == 2){
            map[nowX][nowY] = 3
            show_result_modal(true)
        }

        map[nowX][nowY] = 3
        change_color(nowX, nowY, "#FFFF48")
    }  
    // right
    else if (direction == 2){
        map[nowX][nowY] = 1
        nowY -= 1

        if (map[nowX][nowY] == 0){
            nowY += 1
        }
        else if (map[nowX][nowY] == 2){
            map[nowX][nowY] = 3
            show_result_modal(true)
        }

        map[nowX][nowY] = 3
        change_color(nowX, nowY, "#FFFF48")
    }  // left

    else if (direction == 1){
        map[nowX][nowY] = 1
        nowX += 1

        if (map[nowX][nowY] == 0){
            nowX -= 1
        }
        else if (map[nowX][nowY] == 2){
            map[nowX][nowY] = 3
            show_result_modal(true)
        }

        map[nowX][nowY] = 3
        change_color(nowX, nowY, "#FFFF48")
    }  // down
}

function change_color(x, y, color){
    var id = "x"+ String(x) +"y" + String(y);
    document.getElementById(id).style.backgroundColor = color;
}

function show_result_modal(result) {
    clearInterval(refreshIntervalId)

    if (result) {
        document.getElementById("modal-title").textContent = "미로 탈출 성공 🥳"
    } else {
        document.getElementById("modal-title").textContent = "미로 탈출 실패 😢"
    }

    elems = document.getElementById("modal1")
    modal = M.Modal.init(elems, {})
    modal.open()
}



// def load_maze():
//     global map

//     for i in range(0, len(map), 1):
//         for j in range(0, len(map[i]), 1):
//             if (map[i][j] == 0):
//                 change_color(i, j, "#980000")

//             elif (map[i][j] == 2):
//                 change_color(i, j, "#FFFF48")
//                 # 출구

//             elif (map[i][j] == 3):
//                 change_color(i, j, "#90E4FF")
//                 # document.getElementById("x"+i+"y"+j).innerHTML = "<img src='Kkobuk.jpg' width='30' height='25'>"

//             elif (map[i][j] == 1):
//                 change_color(i, j, "white")
//                 # document.getElementById("x"+i+"y"+j).innerHTML = "<img src=''>"


// function erase(){
//     for i in range(0, n, 1):
//         for j in range(0, m, 1):
//             change_color(i, j, "white")
// }