import React, {useLayoutEffect, useRef} from 'react';
import {DashComponentProps} from '../props';
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';

type Props = {
    tick_data: object[],
    tick_speed: number,
    accelerations: object[],
} & DashComponentProps;

const SimulationComponent = (props: Props) => {
    console.log("SimulationComponent props", props);
    const { tick_data, tick_speed , accelerations} = props;
    const containerRef = useRef(null);
    const liftoffTick = tick_data.findIndex(tick => tick["s"] === 1);

    useLayoutEffect(() => {
        while (containerRef.current.firstChild) {
            containerRef.current.removeChild(containerRef.current.firstChild);
        }
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x87CEEB);
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 10;
        camera.position.y = -50;
        const renderer = new THREE.WebGLRenderer();

        renderer.setSize(window.innerWidth, window.innerHeight);
        containerRef.current.appendChild(renderer.domElement);

        const floorGeometry = new THREE.PlaneGeometry(10000, 10000, 1, 1);
        const floorMaterialTop = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        floorMaterialTop.onBeforeCompile = (shader) => {
          shader.fragmentShader = shader.fragmentShader.replace(
            'vec4 diffuseColor = vec4( diffuse, opacity );',
            'vec4 diffuseColor = vec4( diffuse, opacity ); if (gl_FrontFacing) diffuseColor.rgb = diffuseColor.rgb; else diffuseColor.rgb = vec3(0.545, 0.271, 0.075);'
          );
        };
        const floor = new THREE.Mesh(floorGeometry, floorMaterialTop);
        scene.add(floor);

        const gridHelper = new THREE.GridHelper(10000, 100);
        gridHelper.rotation.x = Math.PI / 2;
        scene.add(gridHelper);

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
        scene.add(ambientLight);

        const rocketGeometry = new THREE.ConeGeometry(1, 5, 32);
        const rocketMaterial = new THREE.MeshBasicMaterial({ color: 0x1100ff });
        const rocket = new THREE.Mesh(rocketGeometry, rocketMaterial);
        rocket.rotation.x = Math.PI / 2;
        rocket.position.z = 2.5;
        scene.add(rocket);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableZoom = true;
        controls.target.set(rocket.position.x, rocket.position.y, rocket.position.z);
        controls.update();

        let lastHeight = [];
        const maxHeightHistory = 10;
        let lastRotation = [];
        const maxRotationHistory = 5;

        const updateRocketPosition = (currentTick: number, rocket: THREE.Mesh, controls: OrbitControls) => {
            const newHeight = tick_data[currentTick]["h"];
            lastHeight.push(newHeight);
            if (lastHeight.length > maxHeightHistory) {
                lastHeight.shift();
            }

            rocket.position.z = lastHeight.reduce((a, b) => a + b, 0) / lastHeight.length;

            if (currentTick > liftoffTick) {
                const accelerationX = accelerations["az"][currentTick] / tick_speed;
                const accelerationY = accelerations["ay"][currentTick] / tick_speed;

                rocket.position.x += accelerationX;
                rocket.position.y += accelerationY;
            }

            controls.target.set(rocket.position.x, rocket.position.y, rocket.position.z);
        };

        const updateRocketRotation = (currentTick: number, rocket: THREE.Mesh) => {
            const newRotationX = (tick_data[currentTick]["gx"] * (Math.PI / 180)) + Math.PI / 2;
            const newRotationY = tick_data[currentTick]["gy"] * (Math.PI / 180);
            const newRotationZ = tick_data[currentTick]["gz"] * (Math.PI / 180);
            lastRotation.push([newRotationX, newRotationY, newRotationZ]);
            if (lastRotation.length > maxRotationHistory) {
                lastRotation.shift();
            }
            const averageRotation = lastRotation.reduce((a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]], [0, 0, 0]).map((v: number) => v / lastRotation.length);
            rocket.rotation.x = averageRotation[0];
            rocket.rotation.y = averageRotation[1];
            rocket.rotation.z = averageRotation[2];
        }

        let startTime = new Date().getTime();
        const animate = function () {
            requestAnimationFrame(animate);

            const currentTime = new Date().getTime();
            const delta = (currentTime - startTime) / 1000;
            let currentTick = Math.floor(delta * tick_speed);

            if (currentTick < tick_data.length) {
                updateRocketPosition(currentTick, rocket, controls);
                updateRocketRotation(currentTick, rocket);
                // TODO: add a trail behind the rocket
                // TODO: show a parachute when "d" is 1
                // TODO: add a line to show the current altitude
                // TODO: add google maps 3d view of starting location
                // TODO: better rocket model
                // TODO: text that shows the current tick and seconds elapsed
                // TODO: on hover, show all sensor data for that tick
            } else {
                startTime = new Date().getTime();
            }
            controls.update();
            camera.rotation.z = 0;

            renderer.render(scene, camera);
        };

        const jumpToLiftoff = (_: Event) => {
            rocket.position.x = 0;
            rocket.position.y = 0;
            startTime = new Date().getTime() - (liftoffTick / tick_speed * 1000);
        }

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === "L" || event.key === "l") {
                jumpToLiftoff(event);
            }
        }

        document.addEventListener("keyup", handleKeyDown);

        animate();

        return () => {
            console.log("SimulationComponent unmounted");
            document.removeEventListener("keyup", handleKeyDown);
            // if (animationId) cancelAnimationFrame(animationId);
        }
    }, [tick_data, tick_speed]);

    return (
      <div id={"simulation-canvas"} ref={containerRef} style={{width: "100%", position: "relative"}}/>
    )
}

SimulationComponent.defaultProps = {};

export default SimulationComponent;