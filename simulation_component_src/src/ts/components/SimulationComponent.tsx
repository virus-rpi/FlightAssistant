import React, { useLayoutEffect, useRef } from 'react';
import {DashComponentProps} from '../props';
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';

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

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
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
        controls.minPolarAngle = undefined;
        controls.maxPolarAngle = undefined;
        controls.update();


        let startTime = new Date().getTime();
        let currentTick = 0;
        let animationId = null;
        const animate = function () {
            // if (!document.getElementById("simulation-canvas")) {
            //     cancelAnimationFrame(animationId);
            //     return;
            // }

            animationId = requestAnimationFrame(animate);

            const currentTime = new Date().getTime();
            const delta = (currentTime - startTime) / 1000;
            currentTick = Math.floor(delta * tick_speed);

            if (currentTick < tick_data.length) {
                rocket.position.z = tick_data[currentTick]["h"];
                controls.target.set(rocket.position.x, rocket.position.y, rocket.position.z);
            } else {
                startTime = new Date().getTime();
                currentTick = 0;
            }
            controls.update();

            renderer.render(scene, camera);
        };

        animate();

        return () => {
            console.log("SimulationComponent unmounted");
            if (animationId) cancelAnimationFrame(animationId);
        }
    }, [tick_data, tick_speed]);

    return (
        <div id={"simulation-canvas"} ref={containerRef} style={{width: "100%", height: "30% !important"}}/>
    )
}

SimulationComponent.defaultProps = {};

export default SimulationComponent;