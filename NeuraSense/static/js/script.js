document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const tryNowBtn = document.getElementById('try-now-btn');
    const chatOverlay = document.getElementById('chat-window-overlay');
    const chatClose = document.getElementById('chat-window-close');
  
    if (tryNowBtn) {
      tryNowBtn.addEventListener('click', () => {
        chatOverlay.style.display = 'flex';
        anime({
          targets: '.chat-window',
          scale: [0.8,1],
          opacity: [0,1],
          easing: 'easeOutBack',
          duration: 500
        });
      });
    }
  
    if (chatClose) {
      chatClose.addEventListener('click', () => {
        anime({
          targets: '.chat-window',
          scale: [1,0.8],
          opacity: [1,0],
          easing: 'easeInBack',
          duration: 400,
          complete: () => {
            chatOverlay.style.display = 'none';
          }
        });
      });
    }
  
    // Dynamically set icons from data-icon attribute in results page
    document.querySelectorAll('.section-with-icon[data-icon]').forEach(sec => {
      const icon = sec.getAttribute('data-icon');
      sec.style.setProperty('--section-icon', `url('../images/${icon}')`);
    });
  
    // Animations on index page
    if (body.classList.contains('page-index')) {
      // Fade in hero elements
      anime({
        targets: ['.intro-title', '.intro-text', '.feature-icons'],
        opacity: [0,1],
        translateY: [20,0],
        easing: 'easeOutQuad',
        duration: 800,
        delay: (el, i) => 200 + i*200
      });
    }
  
    // Scroll reveal on results page
    if (body.classList.contains('page-results')) {
      const controller = new ScrollMagic.Controller();
      document.querySelectorAll('.reveal-section').forEach((section) => {
        const tween = anime.timeline({ autoplay: false })
          .add({
            targets: section,
            opacity: [0,1],
            translateY: [30,0],
            easing: 'easeOutQuad',
            duration: 600
          });
  
        new ScrollMagic.Scene({
          triggerElement: section,
          triggerHook: 0.9
        })
        .on("enter", () => tween.play())
        .addTo(controller);
      });
  
      // Fade in top title on results
      anime({
        targets: '.intro-title',
        opacity: [0,1],
        translateY: [20,0],
        easing: 'easeOutQuad',
        duration: 600,
        delay: 200
      });
    }
  });