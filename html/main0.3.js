
var dbg = function(log_txt){
    if (window.console != undefined) {
	console.log(log_txt);
    }
}

var objColors = {
    'Sun':{color:'yellow',darkcolor:'#8f8f00'},
    'Moon':{color:'orange',darkcolor:'#8a4e00'},
    'Jupiter':{color:'brown',darkcolor:'#432a09'},
    'Venus':{color:'blue',darkcolor:'#191595'},
    'Mars':{color:'red',darkcolor:'#191595'},
    'OSCAR7':{color:'green',darkcolor:'#191595'},
    'ISS':{color:'pink',darkcolor:'#191595'}
}


var drawObjectLegend = function(){
    n = 0;
    for(var star in arr){
	rect = new Kinetic.Rect({
          x: 10,
          y: n*12+10,
          width: 10,
          height: 10,
          fill: objColors[star]['color']
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


var stage;
var BGLayer,DarksideLayer,LightsideLayer;
var ObjectLegendLayer;
var spaceObjects;
window.onload = function() {
    stage = new Kinetic.Stage({
        container: "graph",
        width: 1024,
        height: 768
    });
    LightsideLayer = new Kinetic.Layer();
    DarksideLayer = new Kinetic.Layer();
    
    BGLayer = new Kinetic.Layer();
    ObjectLegendLayer = new Kinetic.Layer();
    
    //drawObjectLegend();

    //frame
    BGLayer.add(new Kinetic.Rect({
	strokeWidth:2,
	stroke:'black',
	lineCap:'square',
	lineJoin:'miter',
	x:4,y:4,width:stage.getWidth()-8,height:stage.getHeight()-8
    }));
    BGLayer.add(new Kinetic.Rect({
	strokeWidth:.1,
	stroke:'black',
	lineCap:'square',
	lineJoin:'miter',
	x:8,y:8,width:stage.getWidth()-16,height:stage.getHeight()-16
    }));
    
    //cross
    var line = new Kinetic.Line({strokeWidth:1,stroke:'black',points:[-4,0,4,0]});
    LightsideLayer.add(line);
    line = new Kinetic.Line({strokeWidth:1,stroke:'black',points:[0,-4,0,4]});
    LightsideLayer.add(line);
    
    var _hemi = new Hemisphere(18,64,250);
    LightsideLayer.add(_hemi.getNorthpole());
    DarksideLayer.add(_hemi.getSoutpole());
    
    LightsideLayer.add(AxisHelper());
    
    spaceObjects = new Array();
    for(var star in arr){
	spaceObjects[spaceObjects.length] = new SpaceObj(arr[star],250);
	spaceObjects[spaceObjects.length-1].calcPath();
	spaceObjects[spaceObjects.length-1].calcInfoPath();
	LightsideLayer.add(spaceObjects[spaceObjects.length-1].getGroup('sunny'));
	LightsideLayer.add(spaceObjects[spaceObjects.length-1].getGroup('info'));
	DarksideLayer.add(spaceObjects[spaceObjects.length-1].getGroup('shady'));
	spaceObjects[spaceObjects.length-1].hideInfo();
    }
    spaceObjects[1].showInfo();
    
    DarksideLayer.setRotationDeg(-90);
    DarksideLayer.move(stage.getWidth()*.5,400,stage.getHeight()*.5)
    DarksideLayer.setOpacity(.4);
    LightsideLayer.setRotationDeg(-90);
    LightsideLayer.move(stage.getWidth()*.5,400,stage.getHeight()*.5)

    stage.add(DarksideLayer);
    stage.add(LightsideLayer);
    LightsideLayer.moveToTop();
    DarksideLayer.moveToBottom();
    
    stage.add(BGLayer);
    stage.add(ObjectLegendLayer);

    
};

