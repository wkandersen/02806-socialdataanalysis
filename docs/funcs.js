(function () {
    const root = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    const mediaBlocks = document.querySelectorAll('.media');
    const overlay = document.getElementById('fullscreenOverlay');
    const frame = document.getElementById('fullscreenFrame');
    const closeBtn = document.getElementById('fullscreenClose');

    function applyTheme(theme) {
        root.setAttribute('data-theme', theme);
        const isDark = theme === 'dark';
        themeToggle.textContent = isDark ? 'Light mode' : 'Dark mode';
        themeToggle.setAttribute('aria-pressed', String(isDark));
    }

    let initialTheme = 'light';
    try {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark' || savedTheme === 'light') {
            initialTheme = savedTheme;
        } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            initialTheme = 'dark';
        }
    } catch (error) {
        // Keep light theme if storage is unavailable.
    }
    applyTheme(initialTheme);

    themeToggle.addEventListener('click', () => {
        const nextTheme = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        applyTheme(nextTheme);
        try {
            localStorage.setItem('theme', nextTheme);
        } catch (error) {
            // Ignore storage failures and keep the in-memory preference.
        }
    });

    function closeFullscreen() {
        frame.innerHTML = '';
        overlay.classList.remove('is-open');
        overlay.classList.remove('fullscreen-last');
        overlay.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('fullscreen-open');
    }

    function openFullscreen(element, isLastFigure = false) {
        frame.innerHTML = '';
        const tagName = element.tagName.toLowerCase();
        let fullView;

        if (tagName === 'iframe') {
            fullView = document.createElement('iframe');
            fullView.src = element.src;
            fullView.title = element.title || 'Fullscreen figure';
            fullView.loading = 'eager';
            fullView.setAttribute('allowfullscreen', '');
        } else {
            fullView = document.createElement('img');
            fullView.src = element.currentSrc || element.src;
            fullView.alt = element.alt || 'Fullscreen figure';
        }

        frame.appendChild(fullView);
        overlay.classList.add('is-open');
        overlay.classList.toggle('fullscreen-last', isLastFigure);
        overlay.setAttribute('aria-hidden', 'false');
        document.body.classList.add('fullscreen-open');
        closeBtn.focus();
    }

    mediaBlocks.forEach((block, index) => {
        const figure = block.querySelector('img, iframe');
        if (!figure) {
            return;
        }

        if (index === mediaBlocks.length - 1) {
            block.classList.add('media-last');
        }

        const trigger = document.createElement('button');
        trigger.type = 'button';
        trigger.className = 'fullscreen-toggle';
        trigger.textContent = 'Fullscreen';
        trigger.setAttribute('aria-label', 'Open this figure in fullscreen view');
        trigger.addEventListener('click', () => openFullscreen(figure, index === mediaBlocks.length - 1));
        block.appendChild(trigger);
    });

    closeBtn.addEventListener('click', closeFullscreen);

    overlay.addEventListener('click', (event) => {
        if (event.target === overlay) {
            closeFullscreen();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && overlay.classList.contains('is-open')) {
            closeFullscreen();
        }
    });
})();
