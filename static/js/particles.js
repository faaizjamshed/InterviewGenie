// js/particles.js
function createParticles() {
    const particleCount = 40; 
    for (let i = 0; i < particleCount; i++) {
        const p = document.createElement('div');
        const size = Math.random() * 3 + 2 + 'px'; 
        const delay = Math.random() * 5;
        const speed = Math.random() * 10 + 5;
        p.style.cssText = `
            position: fixed;
            width: ${size};
            height: ${size};
            background: rgba(75, 144, 255, ${Math.random() * 0.4 + 0.1});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            z-index: -1;
            pointer-events: none;
            animation: moveUp ${speed}s linear ${delay}s infinite;
            box-shadow: 0 0 ${size} rgba(75,144,255,0.5);
        `;
        document.body.appendChild(p);
    }
}

// Sirf Animation rakhein, Background yahan se khatam!
const styleEl = document.createElement('style');
styleEl.innerHTML = `
    @keyframes moveUp {
        0% { transform: translateY(0) translateX(0); opacity: 0; }
        50% { opacity: 0.5; }
        100% { transform: translateY(-300px) translateX(30px); opacity: 0; }
    }
`;
document.head.appendChild(styleEl);

createParticles();