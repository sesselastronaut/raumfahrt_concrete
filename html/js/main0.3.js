
var dbg = function(log_txt){
    if (window.console != undefined) {
	console.log(log_txt);
    }
}

var showErr = function(msg){
    var div = $('<div class="error">'+msg+'</div>');
    $('#overlay').append(div);
    div.hide().fadeIn().delay(5000).fadeOut();
}


var stage;
var BGLayer,DarksideLayer,LightsideLayer;
var ObjectLegendLayer;
var spaceObjects;

// update data from client
var setData = function(bodyID){
    if(document.location.href.indexOf('file:') != -1){
	showErr('Unable to write file!');
	return;
    }
    $.ajax({
	url: 'set_data.php?goto='+bodyID,
	context: document,
	statusCode: {
	    404: function() {
		showErr('Page Not Found for Data Update');
	    }
	},
	success: function(data){
	    if(data != '1'){
		showErr('Error updating JSON File!');
	    }
	}
    });
}

// frequently update data from server
var loadData = function(){
    if(document.location.href.indexOf('file:') != -1){
	showErr('Offline Mode, no data updates available!');
	return;
    }
    $.ajax({
	url: 'get_data.php',
	context: document,
	statusCode: {
	    404: function() {
		showErr('Page Not Found for Data Update');
	    }
	},
	success: function(data){
	    eval(data);
	    if(arr){
		for(var star in arr){
		    if(spaceObjects[star] != undefined){
			spaceObjects[star].updateData(arr[star]);
		    }
		}
		stage.draw();
	    }
	    window.setTimeout(loadData,30000);
	}
    });
    //window.setTimeout(loadData,3000);
}

// first time loading data
var initData = function(){
    if(document.location.href.indexOf('file:') != -1){
	showErr('Offline Mode, no data updates available!');
	return;
    }
    $.ajax({
	url: 'get_data.php',
	context: document,
	statusCode: {
	    404: function() {
		showErr('Page Not Found for Data Update');
	    }
	},
	success: function(data){
	    eval(data);
	    dbg(cats)
	    if(arr){
		// create categories
		createHTMLCategories(cats);
		for(var star in arr){
		    spaceObjects[star] = new SpaceObj(arr[star],stage.getWidth()*.3);
		    LightsideLayer.add(spaceObjects[star].getGroup('sunny'));
		    LightsideLayer.add(spaceObjects[star].getGroup('info'));
		    LightsideLayer.add(spaceObjects[star].getGroup('act'));
		    DarksideLayer.add(spaceObjects[star].getGroup('shady'));
		    spaceObjects[star].hideInfo();
		}
		window.setTimeout(loadData,300);
	    }
	    else{
		showErr('Unknown Error!');
	    }
	}
    });
    //window.setTimeout(loadData,3000);
}
window.onload = function() {
    stage = new Kinetic.Stage({
        container: "graph",
        width: 1280,
        height: 800
    });
    LightsideLayer = new Kinetic.Layer();
    DarksideLayer = new Kinetic.Layer();
    
    BGLayer = new Kinetic.Layer();
    ObjectLegendLayer = new Kinetic.Layer();
    

    //frame
    BGLayer.add(new Kinetic.Rect({
	strokeWidth:2,
	stroke:'white',
	x:4,y:4,width:stage.getWidth()-8,height:stage.getHeight()-8
    }));
    BGLayer.add(new Kinetic.Rect({
	strokeWidth:1,
	stroke:'white',
	x:8,y:8,width:stage.getWidth()-16,height:stage.getHeight()-16
    }));
    
    //cross
    var line = new Kinetic.Line({strokeWidth:1,stroke:'black',points:[-4,0,4,0]});
    LightsideLayer.add(line);
    line = new Kinetic.Line({strokeWidth:1,stroke:'black',points:[0,-4,0,4]});
    LightsideLayer.add(line);
    
    var _hemi = new Hemisphere(18,64,stage.getWidth()*.3);
    LightsideLayer.add(_hemi.getNorthpole());
    DarksideLayer.add(_hemi.getSoutpole());
    
    //LightsideLayer.add(AxisHelper());
    
    
    spaceObjects = {};
    
    DarksideLayer.setRotationDeg(-90);
    DarksideLayer.move(stage.getWidth()*.55,stage.getHeight()*.53)
    DarksideLayer.setOpacity(.6);
    LightsideLayer.setRotationDeg(-90);
    LightsideLayer.move(stage.getWidth()*.55,stage.getHeight()*.53)

    stage.add(DarksideLayer);
    stage.add(LightsideLayer);
    LightsideLayer.moveToTop();
    DarksideLayer.moveToBottom();
    
    stage.add(BGLayer);
    stage.add(ObjectLegendLayer);

    initData();


    // buttons
    $('.infobox .info').hide();
    $('#go-cancel').click(function(){
	$('.infobox .info').hide();
	$('#nav li.act').removeClass('act').data('spObj').hideInfo();
    });
    
    $('#go-accept').click(function(){
	_spObj = $('#nav li.act').data('spObj');
	setData(_spObj.id);
	$('.infobox.a .title').empty().append(_spObj.name);
	if(_spObj.symbol != undefined){
	    $('.infobox.a .title').prepend('<img src="img/'+_spObj.symbol+'"/>');
	}
    });
    
    
};

