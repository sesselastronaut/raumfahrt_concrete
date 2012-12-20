
var XYZ2XY = function(p){
//xCart = (p[0]+p[2])*Math.cos(0.46365); 
//yCart = p[1]+(p[0]-p[2])*Math.sin(0.46365);
//    return [xCart,yCart];

//    return [p[0]*.75+p[2]*.65,p[1]];//-p[2]*.5
    return [p[0],p[1]];
}
var AzAlt2XYZ = function(r,az,alt){
    //var _sin = (alt>0)?r*Math.sin(alt):r;
    var _sin = r*Math.cos(alt);
    return [_sin * Math.cos(az), _sin * Math.sin(az), r * Math.sin(alt)];
}
