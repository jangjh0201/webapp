document.addEventListener('DOMContentLoaded', function() {
    const images = [
        "/static/images/character_1.png",
        "/static/images/character_2.png",
        "/static/images/character_3.png"
    ];

    let currentIndex = 0;
    const imageElement = document.getElementById('character-image');

    setInterval(() => {
        currentIndex = (currentIndex + 1) % images.length;
        imageElement.src = images[currentIndex];
    }, 1000);
});
