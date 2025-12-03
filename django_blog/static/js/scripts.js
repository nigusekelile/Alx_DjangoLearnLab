// Main JavaScript for Django Blog Application

document.addEventListener('DOMContentLoaded', function() {
    console.log('Django Blog application loaded');
    
    // ============================================
    // MOBILE MENU TOGGLE
    // ============================================
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            this.setAttribute('aria-expanded', navLinks.classList.contains('active'));
            
            // Toggle icon between bars and times
            const icon = this.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.nav-menu') && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                mobileMenuToggle.querySelector('i').classList.remove('fa-times');
                mobileMenuToggle.querySelector('i').classList.add('fa-bars');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
            }
        });
        
        // Mobile dropdown toggle
        const mobileDropdowns = document.querySelectorAll('.dropdown > a');
        mobileDropdowns.forEach(dropdown => {
            dropdown.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    const parent = this.parentElement;
                    parent.classList.toggle('active');
                    
                    // Close other dropdowns
                    mobileDropdowns.forEach(other => {
                        if (other !== this) {
                            other.parentElement.classList.remove('active');
                        }
                    });
                }
            });
        });
    }
    
    // ============================================
    // AUTO-HIDE ALERT MESSAGES
    // ============================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Only auto-hide success messages
        if (alert.classList.contains('alert-success')) {
            setTimeout(() => {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            }, 5000); // Hide after 5 seconds
        }
        
        // Add close button functionality
        const closeBtn = alert.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            });
        }
    });
    
    // ============================================
    // FORM VALIDATION ENHANCEMENTS
    // ============================================
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Add loading state to submit buttons
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            form.addEventListener('submit', function() {
                if (this.checkValidity()) {
                    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                    submitButton.disabled = true;
                    
                    // Re-enable button after 10 seconds (in case of error)
                    setTimeout(() => {
                        submitButton.innerHTML = submitButton.dataset.originalText || 'Submit';
                        submitButton.disabled = false;
                    }, 10000);
                }
            });
            
            // Store original button text
            submitButton.dataset.originalText = submitButton.innerHTML;
        }
        
        // Real-time validation feedback
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            // Add validation classes on blur
            input.addEventListener('blur', function() {
                if (this.value.trim() === '' && this.required) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                } else if (this.checkValidity()) {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                } else {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                }
            });
            
            // Remove validation classes on focus
            input.addEventListener('focus', function() {
                this.classList.remove('is-invalid', 'is-valid');
            });
        });
    });
    
    // ============================================
    // DELETE CONFIRMATION DIALOGS
    // ============================================
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        if (button.closest('form')) {
            // Form already has confirmation
            return;
        }
        
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    });
    
    // ============================================
    // ANIMATIONS AND EFFECTS
    // ============================================
    
    // Fade in elements on scroll
    const fadeElements = document.querySelectorAll('.post-card, .feature-card, .related-post-card');
    
    const fadeInOnScroll = function() {
        fadeElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.style.opacity = "1";
                element.style.transform = "translateY(0)";
            }
        });
    };
    
    // Set initial state for fade elements
    fadeElements.forEach(element => {
        element.style.opacity = "0";
        element.style.transform = "translateY(20px)";
        element.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    });
    
    // Run on load and scroll
    window.addEventListener('load', fadeInOnScroll);
    window.addEventListener('scroll', fadeInOnScroll);
    
    // ============================================
    // ACTIVE NAVIGATION HIGHLIGHTING
    // ============================================
    function setActiveNav() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-links a');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPath || 
                (currentPath.includes(href) && href !== '/')) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
    
    setActiveNav();
    
    // ============================================
    // BACK TO TOP BUTTON
    // ============================================
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
    backToTopButton.className = 'back-to-top';
    backToTopButton.setAttribute('aria-label', 'Back to top');
    document.body.appendChild(backToTopButton);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.opacity = '1';
            backToTopButton.style.visibility = 'visible';
            backToTopButton.style.transform = 'translateY(0)';
        } else {
            backToTopButton.style.opacity = '0';
            backToTopButton.style.visibility = 'hidden';
            backToTopButton.style.transform = 'translateY(20px)';
        }
    });
    
    // Scroll to top when clicked
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // ============================================
    // COPY CODE BLOCKS (if any)
    // ============================================
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const copyButton = document.createElement('button');
        copyButton.innerHTML = '<i class="far fa-copy"></i>';
        copyButton.className = 'copy-code-btn';
        copyButton.setAttribute('aria-label', 'Copy code');
        
        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(copyButton);
        
        copyButton.addEventListener('click', function() {
            const textToCopy = block.textContent;
            navigator.clipboard.writeText(textToCopy).then(() => {
                copyButton.innerHTML = '<i class="fas fa-check"></i>';
                copyButton.style.color = '#2ecc71';
                
                setTimeout(() => {
                    copyButton.innerHTML = '<i class="far fa-copy"></i>';
                    copyButton.style.color = '';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                copyButton.innerHTML = '<i class="fas fa-times"></i>';
                copyButton.style.color = '#e74c3c';
                
                setTimeout(() => {
                    copyButton.innerHTML = '<i class="far fa-copy"></i>';
                    copyButton.style.color = '';
                }, 2000);
            });
        });
    });
    
    // ============================================
    // IMAGE LAZY LOADING
    // ============================================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // ============================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const targetElement = document.querySelector(href);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// ============================================
// ADDITIONAL CSS VIA JAVASCRIPT
// ============================================
const additionalStyles = `
    /* Back to top button */
    .back-to-top {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: #3498db;
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        opacity: 0;
        visibility: hidden;
        transform: translateY(20px);
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .back-to-top:hover {
        background: #2980b9;
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(52, 152, 219, 0.4);
    }
    
    /* Form validation states */
    .is-valid {
        border-color: #2ecc71 !important;
        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 8 8'%3e%3cpath fill='%232ecc71' d='M2.3 6.73L.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1z'/%3e%3c/svg%3e");
        background-repeat: no-repeat;
        background-position: right calc(0.375em + 0.1875rem) center;
        background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
    }
    
    .is-invalid {
        border-color: #e74c3c !important;
        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%23e74c3c' viewBox='0 0 12 12'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23e74c3c' stroke='none'/%3e%3c/svg%3e");
        background-repeat: no-repeat;
        background-position: right calc(0.375em + 0.1875rem) center;
        background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
    }
    
    .invalid-feedback {
        display: block;
        width: 100%;
        margin-top: 0.25rem;
        font-size: 0.875rem;
        color: #e74c3c;
    }
    
    /* Copy code button */
    .copy-code-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(255, 255, 255, 0.1);
        color: #95a5a6;
        border: none;
        padding: 5px 10px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .copy-code-btn:hover {
        background: rgba(255, 255, 255, 0.2);
        color: #3498db;
    }
    
    /* Loading spinner */
    .fa-spin {
        animation: fa-spin 1s linear infinite;
    }
    
    @keyframes fa-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Active navigation link */
    .nav-links a.active {
        background-color: #3498db !important;
        color: white !important;
    }
    
    /* Lazy loaded images */
    img[data-src] {
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    img.loaded {
        opacity: 1;
    }
    
    /* Print styles */
    @media print {
        .back-to-top,
        .copy-code-btn,
        .mobile-menu-toggle {
            display: none !important;
        }
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// ============================================
// ERROR HANDLING AND LOGGING
// ============================================
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.message, 'at', e.filename