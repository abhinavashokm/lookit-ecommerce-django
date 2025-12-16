
// Initialize date pickers
flatpickr(".date-picker", {
    dateFormat: "Y-m-d",
    allowInput: true
});

// Date range button functionality
const dateRangeBtns = document.querySelectorAll('.date-range-btn');
dateRangeBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        dateRangeBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        // Here you would typically update the date range based on selection
        const range = this.textContent.trim();
        console.log('Selected date range:', range);
        
        // Example: Update date inputs based on selection
        const today = new Date();
        const fromDate = document.getElementById('fromDate');
        const toDate = document.getElementById('toDate');
        
        if (range === 'Today') {
            fromDate._flatpickr.setDate(today, true);
            toDate._flatpickr.setDate(today, true);
        } else if (range === 'This Week') {
            const firstDay = new Date(today.setDate(today.getDate() - today.getDay()));
            fromDate._flatpickr.setDate(firstDay, true);
            toDate._flatpickr.setDate(new Date(), true);
        } else if (range === 'This Month') {
            const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
            fromDate._flatpickr.setDate(firstDay, true);
            toDate._flatpickr.setDate(new Date(), true);
        } else if (range === 'This Year') {
            const firstDay = new Date(today.getFullYear(), 0, 1);
            fromDate._flatpickr.setDate(firstDay, true);
            toDate._flatpickr.setDate(new Date(), true);
        }
    });
});

// Set default date range to today
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const fromDate = document.getElementById('fromDate');
    const toDate = document.getElementById('toDate');
    
    if (fromDate && toDate) {
        fromDate._flatpickr.setDate(today, true);
        toDate._flatpickr.setDate(today, true);
    }
});
