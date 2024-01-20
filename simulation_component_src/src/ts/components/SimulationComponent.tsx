import React, { useEffect, useRef } from 'react';
import {DashComponentProps} from '../props';
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';

type Props = {
    tick_data: object,
} & DashComponentProps;

const SimulationComponent = (props: Props) => {
    const { tick_data } = props;
    const containerRef = useRef(null);

    useEffect(() => {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();

        renderer.setSize(window.innerWidth, window.innerHeight);
        containerRef.current.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableZoom = true;

        const floorGeometry = new THREE.PlaneGeometry(100, 100, 1, 1);
        const floorMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00, side: THREE.DoubleSide });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        scene.add(floor);

        const rocketGeometry = new THREE.ConeGeometry(1, 2, 32);
        const rocketMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
        const rocket = new THREE.Mesh(rocketGeometry, rocketMaterial);
        scene.add(rocket);

        controls.target.set(rocket.position.x, rocket.position.y, rocket.position.z);
        controls.update();

        const animate = function () {
            requestAnimationFrame(animate);
            rocket.position.y += 0.01;
            controls.target.set(rocket.position.x, rocket.position.y, rocket.position.z);
            controls.update();
            renderer.render(scene, camera);
        };

        animate();
    }, []);

    return (
        <div id={"simulation-container"} ref={containerRef}>
        </div>
    )
}

SimulationComponent.defaultProps = {};

export default SimulationComponent;