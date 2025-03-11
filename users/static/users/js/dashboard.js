/**
 * Dashboard JavaScript functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Add animation to stat numbers if they're visible
    const animateStats = () => {
        const statElements = document.querySelectorAll('.display-4');
        
        statElements.forEach(element => {
            const finalValue = parseInt(element.textContent, 10);
            if (!isNaN(finalValue) && finalValue > 0) {
                let currentValue = 0;
                const duration = 1000; // ms
                const increment = Math.ceil(finalValue / (duration / 16)); // 60fps approx
                
                const counter = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        element.textContent = finalValue;
                        clearInterval(counter);
                    } else {
                        element.textContent = currentValue;
                    }
                }, 16);
            }
        });
    };

    // Use Intersection Observer to trigger animations when elements come into view
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateStats();
                    observer.disconnect(); // Only need to trigger once
                }
            });
        });

        const statsSection = document.querySelector('.row.mb-4');
        if (statsSection) {
            observer.observe(statsSection);
        }
    } else {
        // Fallback for browsers that don't support IntersectionObserver
        setTimeout(animateStats, 500);
    }
});
