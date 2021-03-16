'use strict';

var lineArr;
var timeArr;
var tag_info;
var fastTurns;
var randomIndex;
var map;
var polyline;
var infoWindow;
var randomMarker;

$().ready(function() {
    $("#loader").css("visibility", "hidden");
    $(".input-card").css("visibility", "visible");
    $(".nav-card").css("visibility", "visible");
});

$("#refresh-label").click(refreshMarker);

$("#submit-track-query").click((ev) => {
    var username = $("#username-track-query").val();
    var i_th_track = $("#i-th-track-query").val();
    var url = `/points/${username}/${i_th_track}`;
    console.log(url);
    $.ajax({
        url: url,
        type: "GET",
        dataType: 'json',
        async: true,
        success: function (data) {
            lineArr = data['points'];
            timeArr = data['time'];
            tag_info = data['tag-info'];
            console.log(data);
            fastTurns = data['algo']['fast-turn'];
            console.log(fastTurns);

            // var lineArr = inner_data['points']
            // var lineArr = [[116.478935,39.997761],[116.478939,39.997825],[116.478912,39.998549],[116.478912,39.998549],[116.478998,39.998555],[116.478998,39.998555],[116.479282,39.99856],[116.479658,39.998528],[116.480151,39.998453],[116.48367,39.998968],[116.484648,39.999861]];
            console.log(lineArr)
            map = new AMap.Map("container", {
                resizeEnable: true,
                // center: [1.0, 1.0],
                // center: [120, 30],
                // center: [116.397428, 39.90923],
                center: lineArr[lineArr.length / 2],
                zoom: 17
            });

            // 绘制轨迹
            let cur = 0, i = 0;
            fastTurns.push(1-fastTurns[fastTurns.length-1]) // final opposite sentry
            while (i <= lineArr.length) {
                if (fastTurns[i] != fastTurns[cur]) {
                    let color;
                    if (fastTurns[cur] == 0)
                        color = "#3BE"
                    else
                        color = "#E33"
                    new AMap.Polyline({
                        map: map,
                        path: lineArr.slice(cur, i),
                        showDir:true,
                        strokeColor: color,  //线颜色 light blue
                        // strokeOpacity: 1,     //线透明度
                        strokeWeight: 6,      //线宽
                        // strokeStyle: "solid"  //线样式
                    });

                    cur = i
                }
                i++
            }

            //实例化信息窗体
            var title = '请选择此处驾驶情况';
            var content = [];
            content.push(`
            <input type='button' value='急加速' id='btn-rapid-acc' class='btn'/>
            <input type='button' value='急减速' id='btn-rapid-brake' class='btn'/>
            <input type='button' value='正常' id='btn-normal' class='btn'/>
            <input type='button' value='坏点' id='btn-bad-point' class='btn'/>
            `);

            infoWindow = new AMap.InfoWindow({
                isCustom: true,  //使用自定义窗体
                content: createInfoWindow(title, content.join("<br/>")),
                offset: new AMap.Pixel(16, -45)
            });

            addMarker();

            map.setFitView();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            /*错误信息处理*/
            var json = JSON.parse(jqXHR.responseText);
            var message = json['message']
            if (message === undefined)
                window.alert(`错误码：${jqXHR.status} 请联系管理员`);
            else
                window.alert(`Error occurred: ${message}`);
        }
    });
});

$("div#container").on("click", "#btn-rapid-acc", 
    function(){labelEvent('rapid-acc', '急加速');}
);

$("div#container").on("click", "#btn-rapid-brake",
    function(){labelEvent('rapid-brake', '急减速');}
);

$("div#container").on("click", "#btn-normal",
    function(){labelEvent('normal', '正常');}
);

$("div#container").on("click", "#btn-bad-point", 
    function(){labelEvent('bad-point', '坏点');}
);

// ===============================================
// FUNCTION DEFINITION
// ===============================================

function addMarker() {
    randomIndex = randomNum(0, lineArr.length-1);
    randomMarker = new AMap.Marker({
        map: map,
        position: lineArr[randomIndex]
    });
    AMap.event.addListener(randomMarker, 'click', function() {
        infoWindow.open(map, randomMarker.getPosition());
    });
}

//构建自定义信息窗体
function createInfoWindow(title, content) {
    var info = document.createElement("div");
    info.className = "custom-info input-card content-window-card";

    //可以通过下面的方式修改自定义窗体的宽高
    //info.style.width = "400px";
    // 定义顶部标题
    var top = document.createElement("div");
    var titleD = document.createElement("div");
    titleD.id = 'info-title';
    var closeXDiv = document.createElement("div");
    var closeX = document.createElement("img");
    top.className = "info-top";
    titleD.innerHTML = title;
    closeXDiv.className = "float-right";
    closeX.src = "https://webapi.amap.com/images/close2.gif";
    closeX.onclick = closeInfoWindow;

    top.appendChild(titleD);
    closeXDiv.appendChild(closeX);
    top.appendChild(closeXDiv);
    info.appendChild(top);

    // 定义中部内容
    var middle = document.createElement("div");
    middle.className = "info-middle";
    middle.style.backgroundColor = 'white';
    middle.innerHTML = content;
    info.appendChild(middle);

    // 定义底部内容
    var bottom = document.createElement("div");
    bottom.className = "info-bottom";
    bottom.style.position = 'relative';
    bottom.style.top = '0px';
    bottom.style.margin = '0 auto';
    var sharp = document.createElement("img");
    sharp.src = "https://webapi.amap.com/images/sharp.png";
    bottom.appendChild(sharp);
    info.appendChild(bottom);
    return info;
}

//关闭信息窗体
function closeInfoWindow() {
    map.clearInfoWindow();
}

function refreshMarker() {
    if (randomMarker) {
        randomMarker.setMap(null);
        randomMarker = null;

        closeInfoWindow();
    }
    addMarker();
    map.setFitView();
}

function labelEvent(label_name, chinese_name) {
    // console.log("bind succeed btn-rapid-acc");
    // console.log(lineArr[randomIndex])
    if (window.confirm(`这个点将会被标记为：${chinese_name}`)) {
        $.ajax({
            url: "/label/update", 
            type: 'POST',
            data: `{
                "status": "OK",
                "tag_info": ${JSON.stringify(tag_info)},
                "time": ${JSON.stringify(timeArr[randomIndex])},
                "updated_fields": {
                    "${label_name}": 1
                }
            }`,
            dataType: 'json',
            beforeSend: (request) => {
                // console.log("before send rapid-acc");
            },
            success: function(result) {
                console.log(result);
                console.log(`success ${label_name}`);
                window.alert("数据库已成功更新标记，新标记将产生");
                refreshMarker();
            },
            error: function(result) {
                console.log(result);
                console.log(`error occured ${label_name}`);
                console.log(this.data);
                window.alert("数据回传或更新失败，请联系管理员");
            }
        })
    } else {
        $('#info-title').html("上一次选择已取消，请重新选择")
                        .css("color", "red");
    }
    
}

// UTILS
function equar(a, b) {
    if (a.length !== b.length) {
        return -1
    } else {
        for (let i = 0; i < a.length; i++) {
            if (a[i][0] !== b[i][1] || a[i][1] !== b[i][0]) {
                console.log(typeof a[i][0])
                console.log(typeof b[i][0])
                return i
            }
        }
        return -100;
    }
}
//生成从minNum到maxNum的随机数
function randomNum(minNum,maxNum){ 
    switch(arguments.length){ 
        case 1: 
            return parseInt(Math.random()*minNum+1,10);  
        case 2: 
            return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10); 
            default: 
                return 0; 
    } 
} 
// END OF UTILS

// ===========================================
// END OF FUNCTION DEFINITION
// ===========================================

