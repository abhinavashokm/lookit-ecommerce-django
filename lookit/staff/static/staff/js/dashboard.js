// Animate chart bars on load
window.addEventListener('load', () => {
    const bars = document.querySelectorAll('.category-bar');
    bars.forEach((bar, index) => {
        setTimeout(() => {
            bar.style.width = bar.style.width || '0%';
        }, index * 100);
    });
});

// Toggle KPI cards on mobile
function toggleKPICards() {
    const hiddenCards = document.querySelectorAll('.kpi-card.hidden-mobile');
    const toggleBtn = document.getElementById('kpiToggle');
    const toggleText = document.getElementById('toggleText');
    
    hiddenCards.forEach(card => {
        card.classList.toggle('show');
    });
    
    // Update button text and active state
    if (hiddenCards[0].classList.contains('show')) {
        toggleText.textContent = 'Show Less';
        toggleBtn.classList.add('active');
    } else {
        toggleText.textContent = 'Show More';
        toggleBtn.classList.remove('active');
    }
}