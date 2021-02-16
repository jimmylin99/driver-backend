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
var inner_data
$.ajax({
    url: "points/chendy/0_th_recent",
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

marker = new AMap.Marker({
    map: map,
    // position: [116.478935,39.997761],
    // position: [120, 30],
    position: lineArr[0],
    icon: "http://webapi.amap.com/images/car.png",
    offset: new AMap.Pixel(-26, -13),
    autoRotation: true,
    angle:-90,
});

// 绘制轨迹
var polyline = new AMap.Polyline({
    map: map,
    path: lineArr,
    showDir:true,
    strokeColor: "#28F",  //线颜色
    // strokeOpacity: 1,     //线透明度
    strokeWeight: 6,      //线宽
    // strokeStyle: "solid"  //线样式
});

var passedPolyline = new AMap.Polyline({
    map: map,
    // path: lineArr,
    strokeColor: "#AF5",  //线颜色
    // strokeOpacity: 1,     //线透明度
    strokeWeight: 6,      //线宽
    // strokeStyle: "solid"  //线样式
});


marker.on('moving', function (e) {
    passedPolyline.setPath(e.passedPath);
});

map.setFitView();
function startAnimation () {
    marker.moveAlong(lineArr, 2000);
}

function pauseAnimation () {
    marker.pauseMove();
}

function resumeAnimation () {
    marker.resumeMove();
}

function stopAnimation () {
    marker.stopMove();
}