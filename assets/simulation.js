var observer = new MutationObserver(function(mutations) {
    var simulationContainer = document.getElementById('simulation_container');
    if (simulationContainer) {
        observer.disconnect();

        var simulationContainer = document.getElementById('simulation_container');

        var scene = new THREE.Scene();
        var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 10000);
        var three_renderer = new THREE.WebGLRenderer();

        // var controls = new OrbitControls(camera, three_renderer.domElement);
        // controls.enableZoom = true;

        three_renderer.setSize(window.innerWidth, window.innerHeight);
        simulationContainer.appendChild(three_renderer.domElement);

        var floor_geometry = new THREE.BoxGeometry(100, 0.1, 100);
        var floor_material = new THREE.MeshBasicMaterial({color: 0x00ff00});
        var floor = new THREE.Mesh(floor_geometry, floor_material);
        scene.add(floor);

        var rocket_geometry = new THREE.BoxGeometry(1, 1, 1);
        var rocket_material = new THREE.MeshBasicMaterial({color: 0x00ff00});
        var rocket = new THREE.Mesh(rocket_geometry, rocket_material);
        scene.add(rocket);

        camera.position.z = 5;

        var render = function () {
            requestAnimationFrame(render);

            rocket.rotation.x += 0.1;
            rocket.rotation.y += 0.1;

            three_renderer.render(scene, camera);
        }

        render();
        }
});
observer.observe(document.body, { childList: true, subtree: true });