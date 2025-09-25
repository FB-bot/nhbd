// script.js
document.addEventListener('DOMContentLoaded', function() {
  // Check for saved theme preference
  const savedTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  
  // Update theme toggle button icon
  updateThemeIcon(savedTheme);
  
  // Initialize tool filtering
  initToolFilter();
  
  // Add animation to tool cards
  animateToolCards();
  
  // Initialize search functionality
  initSearch();
});

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  
  updateThemeIcon(newTheme);
  showNotification(`Switched to ${newTheme} mode`);
}

function updateThemeIcon(theme) {
  const icon = document.querySelector('.theme-toggle i');
  icon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
}

function toggleMenu() {
  const navbar = document.getElementById('navbar');
  navbar.classList.toggle('active');
  
  const menuBtn = document.querySelector('.menu-btn i');
  if (navbar.classList.contains('active')) {
    menuBtn.className = 'fas fa-times';
  } else {
    menuBtn.className = 'fas fa-bars';
  }
}

function initToolFilter() {
  const filterButtons = document.querySelectorAll('.category-filter button');
  
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Remove active class from all buttons
      filterButtons.forEach(btn => btn.classList.remove('active'));
      
      // Add active class to clicked button
      this.classList.add('active');
      
      const category = this.getAttribute('data-category');
      filterTools(category);
    });
  });
}

function filterTools(category) {
  const toolCards = document.querySelectorAll('.tool-card');
  
  toolCards.forEach(card => {
    if (category === 'all' || card.getAttribute('data-category') === category) {
      card.style.display = 'block';
      setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, 50);
    } else {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      setTimeout(() => {
        card.style.display = 'none';
      }, 300);
    }
  });
}

function animateToolCards() {
  const toolCards = document.querySelectorAll('.tool-card');
  
  toolCards.forEach((card, index) => {
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 100);
  });
}

function initSearch() {
  const searchInput = document.querySelector('.search-box input');
  
  searchInput.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const toolCards = document.querySelectorAll('.tool-card');
    
    toolCards.forEach(card => {
      const title = card.querySelector('h3').textContent.toLowerCase();
      const desc = card.querySelector('p').textContent.toLowerCase();
      
      if (title.includes(searchTerm) || desc.includes(searchTerm)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

function showNotification(message) {
  const notification = document.getElementById('notification');
  notification.textContent = message;
  notification.classList.add('show');
  
  setTimeout(() => {
    notification.classList.remove('show');
  }, 3000);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;
    
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      window.scrollTo({
        top: targetElement.offsetTop - 80,
        behavior: 'smooth'
      });
      
      // Close mobile menu if open
      const navbar = document.getElementById('navbar');
      if (navbar.classList.contains('active')) {
        toggleMenu();
      }
    }
  });
});