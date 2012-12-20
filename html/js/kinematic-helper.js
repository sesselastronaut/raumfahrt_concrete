
function AxisHelper(){
    var _points;var _line;var _coords;var _group;
    _group = new Kinetic.Group();
    // x-axis
    _points = [];
    _coords = XYZ2XY([0,0,0]);
    _points[_points.length] = _coords[0];
    _points[_points.length] = _coords[1];
    _coords = XYZ2XY([100,0,0]);
    _points[_points.length] = _coords[0];
    _points[_points.length] = _coords[1];
    _line = new Kinetic.Line({
	points:_points,
        stroke: 'red',
        strokeWidth: .25
    });
    _group.add(_line);
    // y-axis
    _points = [];
    _coords = XYZ2XY([0,0,0]);
    _points[_points.length] = _coords[0];
    _points[_points.length] = _coords[1];
    _coords = XYZ2XY([0,100,0]);
    _points[_points.length] = _coords[0];
    _points[_points.length] = _coords[1];
    _line = new Kinetic.Line({
	points:_points,
        stroke: 'green',
        strokeWidth: .25
    });
    _group.add(_line);
    // z-axis
    _points = [];
    _coords = XYZ2XY([0,0,0]);
    _points[_points.length] = _coords[0];
    _points[_points.length] = _coords[1];
    _coords = XYZ2XY([0,0,100]);
    _points[_points.length] = _coords[0];
    _points[_points.length] = _coords[1];
    _line = new Kinetic.Line({
	points:_points,
        stroke: 'blue',
        strokeWidth: .25
    });
    _group.add(_line);
    return _group;
}


function Hemisphere(_longitudePCnt,_circlePCnt,_circleR,drawSouth){
    this.northpole = new Kinetic.Group();
    this.southpole = new Kinetic.Group();
    
    // ground circle
    var _points = [];var _coords=[0.0,0.0];
    for(var i=0;i<_circlePCnt;i++){
	    _coords = XYZ2XY(AzAlt2XYZ(_circleR*.4,Math.PI*2/_circlePCnt*i,0));
	    _points[_points.length] = _coords[0];
	    _points[_points.length] = _coords[1];
    }
    this.northpole.add(new Kinetic.Polygon({
	points:_points,
        fill: 'rgba(230,230,230,.8)'
    }));
    
    // hemisphere altitudes and longitudes
    for(var i=0;i<_longitudePCnt;i++){
	
	_points = [];//upper longitudes
	for(var j=0;j<=_circlePCnt/4;j++){
	    _coords = XYZ2XY(AzAlt2XYZ(_circleR,Math.PI*2/_longitudePCnt*i,(Math.PI/2/(_circlePCnt/4)*j)));
	    _points[_points.length] = _coords[0];
	    _points[_points.length] = _coords[1];
	}
	this.northpole.add(new Kinetic.Line({
	    points:_points,
            stroke: 'grey',
            strokeWidth: .25,
            lineCap: "round",lineJoin: "round",
	}));

	_points = [];//altitudes
	for(var j=0;j<=_circlePCnt;j++){
	    _coords = XYZ2XY(AzAlt2XYZ(_circleR,(Math.PI*2/_circlePCnt*j),((Math.PI*2/(_longitudePCnt)*i)-Math.PI)/3*2));
	    _points[_points.length] = _coords[0];
	    _points[_points.length] = _coords[1];
	}
	if(i<_longitudePCnt/2){
	    if(drawSouth){
		this.southpole.add(new Kinetic.Line({
		    points:_points,
		    stroke: 'grey',
		    strokeWidth: .25,
		    lineCap: "round",lineJoin: "round",
		}));
	    }
	}
	else{
	    this.northpole.add(new Kinetic.Line({
		points:_points,
		stroke: 'grey',
		strokeWidth: (i==_longitudePCnt/2)?.5:.25,
		lineCap: "round",lineJoin: "round",
	    }));
	}
	
	if(drawSouth){
	    _points = [];//lower longitudes
	    for(var j=0;j<=_circlePCnt/4;j++){
		_coords = XYZ2XY(AzAlt2XYZ(_circleR,Math.PI*2/_longitudePCnt*i,(Math.PI/2/(_circlePCnt/4)*j)-Math.PI/2));
		_points[_points.length] = _coords[0];
		_points[_points.length] = _coords[1];
	    }
	    this.southpole.add(new Kinetic.Line({
		points:_points,
		stroke: 'grey',
		strokeWidth: .25,
		lineCap: "round",lineJoin: "round",
	    }));
	}
    }
    /* METHODS */
    this.getSoutpole = function(){return this.southpole;}
    this.getNorthpole = function(){return this.northpole;}
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
    
    /* METHODS */
    this.getVal = function(){
	return this.val;
    }
    this.setVal = function(val){
	this.val=val;
	this.txtInfo.setText(this.val);
	this.valueChanged();
    }
    this.calcVal = function(x){
	this.setVal( 1. / this.width * (x-this.posX) * (this.maxVal-this.minVal)+this.minVal );
	return this.getVal();
    }
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
