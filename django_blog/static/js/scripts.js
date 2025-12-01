// Basic example script to demonstrate dynamic behavior
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog page loaded');
    
    // Add fade-in animation to all post cards
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add confirmation for delete buttons
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Add active state to navigation links
    const currentUrl = window.location.pathname;
    const navLinks = document.querySelectorAll('header nav ul li a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
            link.style.backgroundColor = '#3498db';
            link.style.color = 'white';
        }
    });
});