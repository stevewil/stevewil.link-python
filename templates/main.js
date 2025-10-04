document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.getElementById('hamburger-button');
    const navLinks = document.getElementById('navbar-links');

    if (hamburger && navLinks) {
        const closeMenu = () => {
            navLinks.classList.remove('is-active');
            hamburger.classList.remove('is-active');
            document.body.classList.remove('body-no-scroll');
        };

        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('is-active');
            hamburger.classList.toggle('is-active');
            document.body.classList.toggle('body-no-scroll');
        });

        navLinks.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    }
});