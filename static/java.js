
document.addEventListener("DOMContentLoaded", () => {
    
    // --- Video Player Logic ---
    const video = document.getElementById("hoverVideo");
    if (video) {
        video.addEventListener("click", () => {
            video.muted = false;
            video.play();
        });
        video.addEventListener("mouseleave", () => {
            video.muted = true;
        });
    }

    // --- Image Slider Logic ---
    const track = document.querySelector('.slider-track');
    if (track) {
        let scrollAmount = 0;
        
        function autoSlide() {
            // Ballaca hal sawir + farqiga (gap)
            const scrollWidth = track.querySelector('img').clientWidth + 10; 
            scrollAmount += scrollWidth;
            
            if (scrollAmount >= track.scrollWidth - track.clientWidth) {
                scrollAmount = 0; // Ku noqo bilowga
            }
            track.scrollTo({
                left: scrollAmount,
                behavior: 'smooth'
            });
        }
        // Ku dar setInterval si uu si otomaatig ah u shaqeeyo (3 ilbiriqsi kasta)
        setInterval(autoSlide, 3000);
    }

    // --- Scroll Animation Logic (Intersection Observer) ---
    const sectionsToAnimate = document.querySelectorAll('#product, .secand-product-section, #features-section, #contect');
    if (sectionsToAnimate.length > 0) {
        const scrollObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                } else {
                    entry.target.classList.remove('visible');
                }
            });
        }, {
            threshold: 0.1
        });
        sectionsToAnimate.forEach(section => {
            section.classList.add('scroll-reveal');
            scrollObserver.observe(section);
        });
    }

  const cursor = document.getElementById('custom-cursor');

    // Hubi in cursor-ku jiro iyo inaanan ku jirin shaashad taabasho leh (mobile)
    if (cursor && !window.matchMedia("(pointer: coarse)").matches) {
        
        let mouseX = 0, mouseY = 0;
        let cursorX = 0, cursorY = 0;
        const speed = 0.1;

        function animateCursor() {
            const deltaX = mouseX - cursorX;
            const deltaY = mouseY - cursorY;
            
            cursorX += deltaX * speed;
            cursorY += deltaY * speed;
            
            cursor.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0)`;
            requestAnimationFrame(animateCursor);
        }

        animateCursor();

        window.addEventListener('mousemove', e => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        // Soo ururi dhamaan walxaha la rabo in cursor-ku uu isqariyo marka la dul istaago
        const interactiveElements = document.querySelectorAll(
            'a, button, .cards, .feature-card, #hoverVideo, .slider-track img, .social-media a, .down1 a.'
        );

        // KAN WAA CAQLIGA LA BADALAY:
        // Hadda cursor-ka gaarka ah wuu qarsoomayaa halkii uu weynaan lahaa.
        interactiveElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursor.classList.add('hidden'); // Qari cursor-ka gaarka ah
            });
            el.addEventListener('mouseleave', () => {
                cursor.classList.remove('hidden'); // Soo celi cursor-ka gaarka ah
            });
        });

        // Qari cursor-ka marka uu mouse-ku ka baxo daaqada
        document.addEventListener('mouseleave', () => {
            cursor.classList.add('hidden');
        });

        // Soo bandhig cursor-ka marka uu mouse-ku soo galo daaqada
        document.addEventListener('mouseenter', () => {
            cursor.classList.remove('hidden');
        });
    }
    // =========================================================
    // === DHAMAADKA Koodhka Cusub ee CURSOR-KA ===
    // =========================================================
});

    // --- Mobile Menu Toggle Logic ---
    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.querySelector(".nav-menu");
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener("click", () => {
            navMenu.classList.toggle("active");
        });
    }

    // --- Scroll to Top Logic ---
    const scrollToTopBtn = document.getElementById("scrollToTopBtn");
    
    if (scrollToTopBtn) {
        scrollToTopBtn.addEventListener("click", () => {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }
  