let scene, camera, renderer, particles;

function initThreeJS() {
    // Create scene
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);

    // Ensure the container is positioned correctly
    const container = document.getElementById('threejs-container');
    container.style.position = 'absolute';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '100%';
    container.style.height = '100%';
    container.style.zIndex = '1';

    container.appendChild(renderer.domElement);

    // Create particles
    const geometry = new THREE.BufferGeometry();
    const vertices = [];
    for (let i = 0; i < 1000; i++) {
        vertices.push(
            Math.random() * 600 - 300,
            Math.random() * 600 - 300,
            Math.random() * 600 - 300
        );
    }
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    const material = new THREE.PointsMaterial({ color: 0xffffff, size: 0.5, opacity: 0.5 });
    particles = new THREE.Points(geometry, material);
    scene.add(particles);

    camera.position.z = 300;

    // Ensure renderer's canvas doesn't capture mouse events
    renderer.domElement.style.pointerEvents = 'none';
}

function animate() {
    requestAnimationFrame(animate);

    if (particles) {
        particles.rotation.x += 0.0005;
        particles.rotation.y += 0.0005;
    }

    renderer.render(scene, camera);
}

function handleResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initThreeJS();
    animate();

    // Add resize listener
    window.addEventListener('resize', handleResize);
});
