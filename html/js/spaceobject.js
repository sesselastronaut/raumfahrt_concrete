function createHTMLCategories(cats){
    for(cat in cats){
	var _li = '<li id="'+cat+'" n='+cats[cat]['sort']+'><span>'+cats[cat]['name']+'</span><ul></ul></li>';
	// append in correct order
	$('#nav > ul > li').each(function(){
	    if( parseInt($(this).attr('n')) > cats[cat]['sort']){
		$(this).before(_li);_li='';
	    }
	});
	if(!$('#nav li#'+cat).length){
	    $('#nav > ul').append(_li);
	}
    }
}

function SpaceObjHTML(spObj){
    this.spObj = spObj;
    this.init = function(){
	// add html navigation
	var _li = $('<li class="body" id="'+this.spObj.id+'">'+this.spObj.name+'</div></li>');
	
	if(this.spObj.symbol != undefined)
	    _li.prepend('<div class="symbol"><img src="img/'+this.spObj.symbol+'" widht="12" height="12" /></div>');
	_li.data('spObj',this.spObj).click(function(ev){
	    // deactivate old one
	    if($('#nav li.act').length)
		$('#nav li.act').removeClass('act').data('spObj').hideInfo();
	    $(this).addClass('act');
	    var spObj = $(this).data('spObj');
	    spObj.showInfo();
	    // update infobox 
	    $('.infobox .info .title').empty().append(spObj.name);
	    if(spObj.symbol != undefined)
		$('.infobox .info .title').prepend('<img src="img/'+spObj.symbol+'"/>');
	    $('.infobox .info .pic').empty();
	    if(spObj.pic != undefined)
		$('.infobox .info .pic').append('<img src="img/'+spObj.pic+'"/>');
	    $('.infobox .info .val-dist').empty().append(spObj.dist);
	    $('.infobox .info .val-rot').empty().append(((-180./Math.PI)*spObj.deltaAz).toFixed(2))+";"+spObj.deltaAz;
	    $('.infobox .info .val-size').empty().append(spObj.size);
	    
	    $('.infobox .info').show();
	});
	$('#nav li#'+this.spObj.category+'>ul').append(_li);
    }
}

function SpaceObj(arraydata,radius){
    this.id = arraydata['id'];
    this.name = arraydata['name'];
    this.category = arraydata['category'];
    this.color = arraydata['color'];
    this.symbol = arraydata['symbol'];
    this.pic = arraydata['pic'];
    this.size = arraydata['size'];
    this.dist = arraydata['dist'];
    this.data = arraydata['data'];
    this.radius = radius;
    this.GroupSunnySide = new Kinetic.Group();
    this.GroupShadySide = new Kinetic.Group();
    this.GroupAct = new Kinetic.Group();
    this.GroupInfo = new Kinetic.Group();
    this.deltaAz = 0;
    
    this.htmlRepresentation = new SpaceObjHTML(this);
    this.htmlRepresentation.init();
    
    /* METHODS */
    this.updateData = function(arraydata){
	this.data = arraydata['data'];
	// calc revolutions
	this.deltaAz = 0;
	var _oldAZ = this.data[0]['az'];var _crosses = 0;
	for(var i in this.data){
	    if(Math.abs(_oldAZ-this.data[i]['az']) > Math.PI){// passed north
		_crosses++;
		this.deltaAz+=(_oldAZ-Math.PI*2)-this.data[i]['az'];
	    }
	    else{
		this.deltaAz+=_oldAZ-this.data[i]['az'];
	    }
	    _oldAZ = this.data[i]['az'];
	}
	// generate new graphs
	this.calcInfoPath();
	this.calcPath();
    }
    this.showInfo = function(){
	this.GroupInfo.transitionTo({opacity:1.0,duration:.1});
	//this.GroupAct.moveToTop();
	//this.GroupAct.transitionTo({opacity:1.0,duration:.1});
	this.GroupSunnySide.transitionTo({opacity:0.0,duration:.1});
	this.GroupShadySide.transitionTo({opacity:0.0,duration:.1});
	return;
    }
    this.hideInfo = function(){
	this.GroupInfo.transitionTo({opacity:0.0,duration:.1});
	//this.GroupAct.transitionTo({opacity:0.0,duration:.1});
	this.GroupSunnySide.transitionTo({opacity:1.0,duration:.1});
	this.GroupShadySide.transitionTo({opacity:1.0,duration:.1});
	return;
    }
    this.createPath = function(points,sunnySide){
	// create new shape objectby point array
	var _shape = new Kinetic.Line({
	    points:points,
            stroke: this.color,
            strokeWidth: 2,
	    dashArray: [4, 4]
	});
	// add to corresponding group
	if(sunnySide==1)
	    this.GroupSunnySide.add(_shape);
	else
	    this.GroupShadySide.add(_shape);
	// act
	this.GroupInfo.add(new Kinetic.Line({
	    points:points,
            stroke: this.color,
            strokeWidth: 8,
	    dashArray: [10, 20],
	    lineCap: "round",lineJoin: "round",
	}));
    }
    this.addCoords = function(points,az,alt,radius){
	_coords = XYZ2XY(AzAlt2XYZ(radius,az,alt));
	points[points.length] = _coords[0];
	points[points.length] = _coords[1];
    }
    this.calcInfoPath = function(){
	// clear groups
	this.GroupInfo.removeChildren();

	var _resolution = Math.PI/32;
	var _points = [];
	var _rad = this.radius*.3;
	// infograph: arch for angles
	// az-angle
	_points[_points.length] = 0;_points[_points.length] = 0;
	this.addCoords(_points,this.data[0]['az'],0,_rad);
	for(var j=_resolution;j<Math.abs(this.deltaAz);j+=_resolution){
	    _arc = (this.deltaAz<0)?this.data[0]['az']+j:this.data[0]['az']-j;
	    this.addCoords(_points,_arc,0,_rad+100/Math.abs(this.deltaAz)*j);
	}
	this.addCoords(_points,this.data[this.data.length-1]['az'],0,_rad+100);
	
	this.GroupInfo.add(new Kinetic.Polygon({
	    points:_points,
	    fill:'red',
	    opacity:.5
	}));
	this.GroupInfo.add(new Kinetic.Line({
	    points:_points,
	    stroke:'white',
	    strokeWidth:1,
	}));

	// 1st alt angle
	_points = [0,0];
	for(var j=0;j<Math.abs(this.data[0]['alt']);j+=_resolution){
	    this.addCoords(_points,this.data[0]['az'],(this.data[0]['alt']<0)?-j:j,_rad);
	}
	this.addCoords(_points,this.data[0]['az'],this.data[0]['alt'],_rad);
	this.GroupInfo.add(new Kinetic.Polygon({
	    points:_points,
	    stroke:'grey',
	    strokeWidth: 1,
	    fill:'rgba(100,100,100,.13)'
	}));
	// last alt angle
	_points = [0,0];
	for(var j=0;j<Math.abs(this.data[this.data.length-1]['alt']);j+=_resolution){
	    this.addCoords(_points,this.data[this.data.length-1]['az'],(this.data[this.data.length-1]['alt']<0)?-j:j,_rad+100);
	}
	this.addCoords(_points,this.data[this.data.length-1]['az'],this.data[this.data.length-1]['alt'],_rad+100);
	this.GroupInfo.add(new Kinetic.Polygon({
	    points:_points,
	    stroke:'grey',
	    strokeWidth: 1,
	    fill:'rgba(100,100,100,.13)'
	}));
	_points = [];
    }
    this.calcPath = function(){
	// clear groups
	this.GroupSunnySide.removeChildren();
	this.GroupShadySide.removeChildren();
	// calc
	var oldSunnyUp = -1;var sunnyUp = 1;var _coords;
	var _points = [];
	for(var i in this.data){
	    // create dotted lines
	    if(this.data[i]['alt'] <= 0)// on dark side
		sunnyUp = 0;
	    else
		sunnyUp = 1;
	    if(oldSunnyUp !=-1 && oldSunnyUp != sunnyUp){// is changing rise
		// add last point exactly on horizon
		this.addCoords(_points,this.data[i]['az'],this.data[i]['alt'],this.radius);
		// finished for this round, create shape
		this.createPath(_points,oldSunnyUp);
		//
		// new one!
		oldSunnyUp = sunnyUp;
		_points = [];
		// add first point exactly on horizon
		this.addCoords(_points,this.data[i]['az'],this.data[i]['alt'],this.radius);
	    }
	    if(oldSunnyUp ==-1){oldSunnyUp=sunnyUp;}
	    this.addCoords(_points,this.data[i]['az'],this.data[i]['alt'],this.radius);
	}
	this.createPath(_points,sunnyUp);

    }
    this.getGroup = function(name){
	switch(name){
	    case 'sunny':
	    return this.GroupSunnySide;
	    case 'shady':
	    return this.GroupShadySide;
	    case 'info':
	    return this.GroupInfo;
	    case 'act':
	    return this.GroupAct;
	}
    }
}
