document.addEventListener('DOMContentLoaded', function() {
                const images = document.querySelectorAll('.welcome-image img');
                const slideInterval = 2;
                const totalDuration = images.length * slideInterval;
                const percentagePerImage = 100 / images.length;
    
                const keyframes = `
                    @keyframes slideshow {
                        0%, ${percentagePerImage}% { opacity: 1; }
                        ${percentagePerImage + 0.01}%, 100% { opacity: 0; }
                    }
                `;

                const style = document.createElement('style');
                style.textContent = keyframes;
                document.head.appendChild(style);

                images.forEach((img, index) => {
                    img.style.animation = `slideshow ${totalDuration}s infinite`;
                    img.style.animationDelay = `${index * slideInterval}s`;
                });
            });