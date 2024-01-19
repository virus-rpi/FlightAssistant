import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 10000);
const renderer = new THREE.WebGLRenderer();

renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('simulation-container').appendChild(renderer.domElement);

const rocket_geometry = new THREE.BoxGeometry(1, 1, 1);
const rocket_material = new THREE.MeshBasicMaterial({color: 0x00ff00});
const rocket = new THREE.Mesh(rocket_geometry, rocket_material);
scene.add(rocket);

camera.position.z = 5;

const render = function () {
    requestAnimationFrame(render);

    rocket.rotation.x += 0.1;
    rocket.rotation.y += 0.1;

    renderer.render(scene, camera);
}

render();