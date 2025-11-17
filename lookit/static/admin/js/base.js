
// Sidebar toggle functionality
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');
let isCollapsed = false;

menuToggle.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
        // Mobile: toggle show/hide
        sidebar.classList.toggle('show');
    } else {
        // Desktop: toggle collapse/expand
        isCollapsed = !isCollapsed;
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
        } else {
            sidebar.classList.remove('collapsed');
        }
    }
});


// Close sidebar on mobile when clicking outside
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768) {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
            sidebar.classList.remove('show');
        }
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        sidebar.classList.remove('show');
        if (!isCollapsed) {
            sidebar.classList.remove('collapsed');
        }
    }
});

// Navigation menu active state
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', function (e) {

        // Close sidebar on mobile after clicking
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('show');
        }
    });
});

// User dropdown toggle
function toggleUserDropdown(event) {
    event.stopPropagation();
    const dropdown = document.getElementById('userDropdown');
    dropdown.classList.toggle('show');
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('userDropdown');
    const userElement = document.getElementById('navbarUser');
    if (!userElement.contains(e.target)) {
        dropdown.classList.remove('show');
    }
});

// User dropdown functions
function viewProfile() {
    alert('View Profile');
    document.getElementById('userDropdown').classList.remove('show');
}

function openSettings() {
    alert('Open Settings');
    document.getElementById('userDropdown').classList.remove('show');
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        alert('Logging out...');
        // Add actual logout logic here
    }
    document.getElementById('userDropdown').classList.remove('show');
}
