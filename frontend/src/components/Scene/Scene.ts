import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"; // Fixed through https://github.com/mrdoob/three.js/issues/29367

export const init = (renders: (THREE.Mesh | THREE.Group)[]) => {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000,
  );

  const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector("#scene") as HTMLCanvasElement,
  });

  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth * 0.8, window.innerHeight * 0.8);

  camera.position.setZ(30);
  camera.position.setY(10);

  renderer.render(scene, camera);

  const grid = new THREE.GridHelper(200, 50);

  scene.add(grid);

  const axesHelper = new THREE.AxesHelper( 5 );
  scene.add( axesHelper );

  const controls = new OrbitControls(camera, renderer.domElement);

  scene.add(...renders);

  const update = () => {
    renderer.render(scene, camera);
  };

  const loop = () => {
    requestAnimationFrame(loop);

    controls.update();

    renderer.render(scene, camera);
  };

  loop();

  return {
    update,
  };
};
