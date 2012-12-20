
var dbg = function(log_txt){
    if (window.console != undefined) {
	console.log(log_txt);
    }
}
var showInfo = function(evt,log_txt) {
    el = document.getElementById('info');
    el.innerHTML = log_txt;
    el.style.left = evt.pageX;
    el.style.top = evt.pageY;
}

var objColors = {
    'Sun':'yellow',
    'Moon':'orange',
    'Jupiter':'brown',
    'Venus':'blue',
    'Mars':'red',
    'OSCAR7':'green',
    'ISS':'pink',
    'TOOLBAG':'lightblue',
}

var createObjectPaths = function(scale){
    for(star in arr){
	var _path = 'M0,0';
	for(data in arr[star]){
	    _path+= 'L'+Math.sin(arr[star][data]['az']) * arr[star][data]['dist'] * scale;
	    _path+= ','+Math.cos(arr[star][data]['az']) * arr[star][data]['dist'] * scale;
	}
	paper.path(_path);
    }
}

var ObjectPathLayer = new Kinetic.Layer();


var paper;
window.onload = function() {
    paper = Raphael(document.getElementById("stars"), 320, 200);
    paper.text(50, 50, "Space Oserver");
    createObjectPaths(100);
};


/*
var mode = 'bed';
var html = '';
for(star  in arr){
    html+= '<div class="legend '+star+'">'+star+'</div>';
    for(data in arr[star]){
	if(mode == 'gal'){
	    y = arr[star][data]['dec'];
	    x = arr[star][data]['ra'];
	    x = (x*200);
	    y = (y*200+30);
	}
	else if(mode == 'bed'){
	    x = Math.sin(arr[star][data]['az']) * arr[star][data]['dist'] * 400;
	    y = Math.cos(arr[star][data]['az']) * arr[star][data]['dist'] * 400;
	    x+=600;y+=600;
	}
	else{
	    x = Math.sin(arr[star][data]['ra']) * arr[star][data]['dist'] * 40;
	    y = Math.cos(arr[star][data]['ra']) * arr[star][data]['dist'] * 40;
	    x+=600;y+=600;
	}
	html+='<div onmouseover="showInfo(event,\''+star+'\')" class="sta '+star+'" style="left:'+(x)+'px;top:'+(y)+'px;"></div>';
    }
}
el = document.getElementById('stars');
el.innerHTML = html;

*/