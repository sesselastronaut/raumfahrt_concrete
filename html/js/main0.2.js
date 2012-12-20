
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


function Slider(title,posX,posY,minVal,maxVal,width,layer){
    this.title=title;
    this.posX=posX;
    this.posY=posY;
    this.minVal=minVal;
    this.maxVal=maxVal;
    this.width=width;
    this.layer = layer;
    this.val=minVal;
    
    this.valueChanged = function(){}
    
    shade = {color: 'black',blur: 1,offset: [2, 2],alpha: 0.25};
    this.canvas = new Kinetic.Group({x:this.posX,y:this.posY});
    this.bg = new Kinetic.Rect({x:0,y:0,width:this.width+12,height:12,fill: '#cccccc',shadow: shade});
    this.bg.slider = this;
    this.bg.on('click', function(evt){
	var mousePos = stage.getMousePosition();
	var x = mousePos.x-this.slider.posX;
	this.slider.calcVal(x);
	this.slider.handle.setX(x);
	this.slider.layer.draw();
    });
    this.handle = new Kinetic.Rect({
        x: 0,y: 0,width: 12,height: 12,
        fill: '#ff0000',shadow: shade,draggable: true,
	dragBoundFunc: function(pos) {
	    var newX = pos.x < this.slider.posX ? this.slider.posX : pos.x >= this.slider.posX+this.slider.width ? this.slider.posX+this.slider.width : pos.x;
	    this.slider.calcVal(newX);
	    return {
		x: newX,
		y: this.slider.posY
	    };
	}
    });
    this.handle.slider = this;
    this.txtInfo = new Kinetic.Text({x:0,y:0,textFill: 'black',text: this.getVal()});
    this.canvas.add(this.bg);
    this.canvas.add(this.txtInfo);
    this.canvas.add(this.handle);
    this.layer.add(this.canvas);
}
Slider.prototype.calcVal = function(x){
    this.setVal( 1. / this.width * (x-this.posX) * (this.maxVal-this.minVal)+this.minVal );
    return this.getVal();
}
Slider.prototype.getVal = function(){
    return this.val;
}
Slider.prototype.setVal = function(val){
    this.val=val;
    this.txtInfo.setText(this.val);
    this.valueChanged();
}

var drawObjectLegend = function(){
    n = 0;
    for(var star in arr){
	rect = new Kinetic.Rect({
          x: 10,
          y: n*12+10,
          width: 10,
          height: 10,
          fill: objColors[star]
        });
	txt = new Kinetic.Text({
          x: 22,
          y: n*12+11,
          text: star,
	    fontSize: 9,
	    fontFamily: 'Verdana, Courier',
          textFill: 'black'
        });
	ObjectLegendLayer.add(rect);
	ObjectLegendLayer.add(txt);
	n++;
    }
}

function SpaceObj(arraydata){
    this.name = arraydata['name'];
    this.color = objColors[this.name];
    this.size = arraydata['size'];
    this.data = arraydata['data'];
    this.shape = new Kinetic.Line({
	points:[0,0,0,0],
        stroke: this.color,
        strokeWidth: Math.max(3,this.size*.01),
        lineCap: "round",lineJoin: "round"
    });
    this.shape.move(400,300);
}
SpaceObj.prototype.getShape = function(){
    return this.shape;
}
SpaceObj.prototype.calcPath = function(zoom){
    var _points = new Array();
    for(var i in this.data){
	_points[_points.length] = Math.sin(this.data[i]['az']) * this.data[i]['dist'] * zoom;
	_points[_points.length] = Math.cos(this.data[i]['az']) * this.data[i]['dist'] * zoom;
	//_points[_points.length] = Math.sin(arr[star][data]['az']) * (n*4+60);
	//_points[_points.length] = Math.cos(arr[star][data]['az']) * (n*4+60);
    }
    //this.shape.points = _points;
    this.shape.setPoints(_points);
}
var drawObjectPaths = function(scale){
    n=0;
    for(var star in arr){
	var _points = new Array();
	for(var i in arr[star]['data']){
	    _points[_points.length] = Math.sin(arr[star]['data'][i]['az']) * arr[star]['data'][i]['dist'] * scale;
	    _points[_points.length] = Math.cos(arr[star]['data'][i]['az']) * arr[star]['data'][i]['dist'] * scale;
	    //_points[_points.length] = Math.sin(arr[star][data]['az']) * (n*4+60);
	    //_points[_points.length] = Math.cos(arr[star][data]['az']) * (n*4+60);
	}
	path = new Kinetic.Line({
	    points: _points,
            stroke: objColors[star],
            strokeWidth: Math.max(3,arr[star]['size']*.01),
            lineCap: "round",
            lineJoin: "round",
	});
	path.move(400,300);
	dbg(star+";"+arr[star]['size']*.01+";"+arr[star]['data'][0]['dist']);
	ObjectPathLayer.add(path);
	n++;
    }
}
var stage;
var ObjectPathLayer;
var ObjectLegendLayer;
var spaceObjects;
window.onload = function() {
    stage = new Kinetic.Stage({
        container: "stars",
        width: 800,
        height: 600
    });
    ObjectPathLayer = new Kinetic.Layer();
    ObjectLegendLayer = new Kinetic.Layer();
    
    drawObjectLegend();


    line = new Kinetic.Line({strokeWidth:1,stroke:'black',points:[-4,0,4,0]});
    line.move(400,300);
    ObjectPathLayer.add(line);
    line = new Kinetic.Line({strokeWidth:1,stroke:'black',points:[0,-4,0,4]});
    line.move(400,300);
    ObjectPathLayer.add(line);
    
    spaceObjects = new Array();
    for(var star in arr){
	spaceObjects[spaceObjects.length] = new SpaceObj(arr[star]);
	spaceObjects[spaceObjects.length-1].calcPath(50);
	ObjectPathLayer.add(spaceObjects[spaceObjects.length-1].getShape());
    }
//    drawObjectPaths(300);

    slZoom = new Slider('Zoom',10,580,50,100000,760,ObjectLegendLayer);

    slZoom.valueChanged = function(){
	for(var i in spaceObjects){
	    spaceObjects[i].calcPath(this.val);
	    //spaceObjects[i].update();
	}
	ObjectPathLayer.draw();
    }

    stage.add(ObjectPathLayer);
    stage.add(ObjectLegendLayer);
};


/*
var mode = 'bed';
var html = '';
for(var star  in arr){
    html+= '<div class="legend '+star+'">'+star+'</div>';
    for(var data in arr[star]){
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