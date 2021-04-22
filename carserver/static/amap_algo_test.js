'use strict';

var lineArr;
var timeArr;
var tag_info;
var ROIs;
var randomIndex;
var map;
var polyline;
var infoWindow;
var randomMarker;

$().ready(function() {
    $("#loader").css("visibility", "hidden");
    $(".nav-card").css("visibility", "visible");
});

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
            ROIs = data['algo']['ROI'];
            console.log(ROIs);

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
            ROIs.push(1-ROIs[ROIs.length-1]) // final opposite sentry
            while (i <= lineArr.length) {
                if (ROIs[i] != ROIs[cur]) {
                    let color;
                    if (ROIs[cur] == 0)
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

// ===============================================
// FUNCTION DEFINITION
// ===============================================

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

