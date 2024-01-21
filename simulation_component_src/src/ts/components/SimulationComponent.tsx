import React, {useLayoutEffect, useRef} from 'react';
import {DashComponentProps} from '../props';
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {Simulate} from "react-dom/test-utils";
import keyDown = Simulate.keyDown;

type Props = {
    tick_data: object[],
    tick_speed: number,
} & DashComponentProps;

const SimulationComponent = (props: Props) => {
    console.log("SimulationComponent props", props);
    const { tick_data, tick_speed } = props;
    const containerRef = useRef(null);

    useLayoutEffect(() => {
        while (containerRef.current.firstChild) {
            containerRef.current.removeChild(containerRef.current.firstChild);
        }
        // TODO: add a button to jump to liftoff (first tick where "s" is 1)
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x87CEEB);
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5;
        camera.position.y = -15;
        const renderer = new THREE.WebGLRenderer();

        renderer.setSize(window.innerWidth, window.innerHeight);
        containerRef.current.appendChild(renderer.domElement);

        const floorGeometry = new THREE.PlaneGeometry(500, 500, 1, 1);
        const floorMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00, side: THREE.DoubleSide });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        scene.add(floor);

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

        const updateRocketPosition = (currentTick: number, rocket: THREE.Mesh, controls: OrbitControls) => { // TODO: smooth out the animation with moving average
            rocket.position.z = tick_data[currentTick]["h"];
            controls.target.set(rocket.position.x, rocket.position.y, rocket.position.z);
        };

        let startTime = new Date().getTime();
        const animate = function () {
            requestAnimationFrame(animate);

            const currentTime = new Date().getTime();
            const delta = (currentTime - startTime) / 1000;
            let currentTick = Math.floor(delta * tick_speed);

            if (currentTick < tick_data.length) {
                updateRocketPosition(currentTick, rocket, controls); // TODO: add rotation and other axis through acceleration
                // TODO: add a trail behind the rocket
                // TODO: show a parachute when "d" is 1
            } else {
                startTime = new Date().getTime();
            }
            controls.update();

            renderer.render(scene, camera);
        };

        const jumpToLiftoff = (_: Event) => {
            const liftoffTick = tick_data.findIndex(tick => tick["s"] === 1);
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
    <>
      <div id={"simulation-canvas"} ref={containerRef} style={{width: "100%", position: "relative"}}/>
    </>
    )
}

SimulationComponent.defaultProps = {};

export default SimulationComponent;