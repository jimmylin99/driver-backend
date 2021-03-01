'use strict';
// utils start
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
        break; 
        case 2: 
            return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10); 
        break; 
            default: 
                return 0; 
            break; 
    } 
} 
// utils end
var inner_data
var randomIndex;
$.ajax({
    url: "/points/chendy/0_th_recent",
    type: "GET",
    dataType: 'json',
    async: false,
    success: function (data) {
        console.log(data)
        console.log(data['points'])
        inner_data = data['points']
        // inner_data = [
        //     [121.43486897291308,31.030860772000423], 
        //     [121.43486897291308,31.030860772000423], 
        //     [121.43486897291308,31.030860772000423], 
        //     [121.43486897291308,31.030860772000423],
        //     [121.43489763090122,31.03104879079986], 
        //     [121.43489763090122,31.03104879079986],
        //     [121.43489763090122,31.03104879079986]
        // ]
        // console.log(equar(data['points'], inner_data))

        // $('#debug-log').text(data.data)

    }
})

// var lineArr = inner_data['points']
var lineArr = inner_data
// var lineArr = [[116.478935,39.997761],[116.478939,39.997825],[116.478912,39.998549],[116.478912,39.998549],[116.478998,39.998555],[116.478998,39.998555],[116.479282,39.99856],[116.479658,39.998528],[116.480151,39.998453],[116.48367,39.998968],[116.484648,39.999861]];
console.log(lineArr)
var map = new AMap.Map("container", {
    resizeEnable: true,
    // center: [1.0, 1.0],
    // center: [120, 30],
    // center: [116.397428, 39.90923],
    center: lineArr[lineArr.length / 2],
    zoom: 17
});

// 绘制轨迹
var polyline = new AMap.Polyline({
    map: map,
    path: lineArr,
    showDir:true,
    strokeColor: "#F8F",  //线颜色
    // strokeOpacity: 1,     //线透明度
    strokeWeight: 6,      //线宽
    // strokeStyle: "solid"  //线样式
});

//实例化信息窗体
var title = '请选择此处驾驶情况';
var content = [];
content.push(`
<input type='button' value='急加速' id='btn-rapid-acc' class='btn'/>
<input type='button' value='急减速' id='btn-rapid-brake' class='btn'/>
<input type='button' value='正常' id='btn-normal' class='btn'/>
`);

var infoWindow = new AMap.InfoWindow({
    isCustom: true,  //使用自定义窗体
    content: createInfoWindow(title, content.join("<br/>")),
    offset: new AMap.Pixel(16, 0)
})

addMarker()

map.setFitView();

$("div#container").on("click", "#btn-rapid-acc", function() {
    console.log("bind succeed btn-rapid-acc");
    $.ajax({
        url: "/label/rapid-acc", 
        type: 'POST',
        data: `{
            "status": "OK",
            "lng": ${lineArr[randomIndex][0]},
            "lat": ${lineArr[randomIndex][1]},
            "user": "chendy",
            "i-th-track": 0 
        }`,
        dataType: 'json',
        beforeSend: (request) => {
            console.log("before send rapid-acc");
        },
        success: function(result) {
            console.log(result);
            console.log("success rapid-acc");
        },
        error: function(result) {
            console.log(result);
            console.log("error occured rapid-acc");
            console.log(data);
        }
    })
})


function addMarker() {
    randomIndex = randomNum(0, lineArr.length-1);
    var randomMarker = new AMap.Marker({
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
