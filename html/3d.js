
var dbg = function (log_txt) {
    if (window.console != undefined) {
	console.log(log_txt);
    }
}

var scene,camera,renderer;
var clock = new THREE.Clock();

/* CUSTOM */
var testLine;
var stagrp,sta;

/* SHOOT */
init();
animate();

function init(){
    
    scene = new THREE.Scene(); 
    
    camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 100);
    camera.up = new THREE.Vector3( 0, 0, 1 );
    //camera.rotation.set(0, -.1, 0);
    camera.position.set(30, 10, 30);
    camera.lookAt(new THREE.Vector3(0, 0, 0));
    
    renderer = new THREE.WebGLRenderer(); 
    renderer.setSize(window.innerWidth, window.innerHeight); 
    
    /* CIRCLE ON GROUND */
    var material = new THREE.LineBasicMaterial({
	color: 0xcccccc,
    });
    geometry = new THREE.Geometry();
    var circlePointsCnt = 64;var circleRad = 15;
    for(var i=0;i<=circlePointsCnt;i++){
	var j = Math.PI*2 / circlePointsCnt * i;
	geometry.vertices.push(new THREE.Vector3(Math.sin(j)*circleRad, Math.cos(j)*circleRad, 0));
    }
    GroundCircle = new THREE.Line(geometry, material);
    scene.add(GroundCircle);
    
    /* TEST LINE */
    var material = new THREE.LineBasicMaterial({
	color: 0xff00ff,
    });
    geometry = new THREE.Geometry();
    geometry.vertices.push(new THREE.Vector3(0, 0, 0));
    geometry.vertices.push(new THREE.Vector3(10, 0, 0));
    testLine = new THREE.Line(geometry, material);
    //testLine.matrix.setRotationFromEuler(new THREE.Vector3(Math.PI / 3,0,0),  'XYZ');
    //testLine.updateMatrix();
    scene.add(testLine);
    
    /* STAR */
    sta = new THREE.Object3D();
    sta.add( new THREE.AxisHelper() );
    sta.translateX(circleRad);
    
    stagrp = new THREE.Object3D();//
    stagrp.add( new THREE.AxisHelper() );
    stagrp.add( sta );
    stagrp.translateX(13);
    //sta.rotation.x = Math.PI/4;
    scene.add(stagrp);
    
    var axes = new THREE.AxisHelper();
    axes.scale.set( 4, 4, 4 );
    scene.add( axes );
    
    document.body.appendChild(renderer.domElement);
}

function animate() {
    requestAnimationFrame(animate);
    render();		
    update();
}
function update(){
    // delta = change in time since last call (in seconds)
    var delta = clock.getDelta(); 
    //sta.rotation.z = -clock.getElapsedTime();
    stagrp.rotation.y = -clock.getElapsedTime();
    dbg(camera.position)
    //sta.lookAt(camera.position)
    testLine.rotation.z = -clock.getElapsedTime();
    //testLine.matrix.setRotationFromEuler(new THREE.Vector3(0,clock.getElapsedTime()),  'XYZ');
    //testLine.updateMatrix();
    //controls.update();
    //stats.update();
}
function render(){
    renderer.render(scene, camera); 
}
