// Animate chart bars on load
window.addEventListener('load', () => {
    const bars = document.querySelectorAll('.category-bar');
    bars.forEach((bar, index) => {
        setTimeout(() => {
            bar.style.width = bar.style.width || '0%';
        }, index * 100);
    });
});