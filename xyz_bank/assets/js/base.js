// Loader Handling
window.addEventListener('load', () => {
    document.getElementById('loader').style.display = 'none';
    document.getElementById('appCapsule').style.display = 'block';
});


// Show loader before navigating to a new page
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', (event) => {
            const href = link.getAttribute('href');
            
            // Only show loader for internal links (ignore # and external links)
            if (href && !href.startsWith('#') && !href.startsWith('http')) {
                document.getElementById('loader').style.display = 'flex';
            }
        });
    });
});

// Ensure Dark Mode Loads on Every Page (applies immediately)
if (localStorage.getItem('darkMode') === '1') {
    document.body.classList.add('dark-mode');
}

// When DOM is Ready
document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing base.js...");

    // ✅ Dark Mode Handling
    const isDarkMode = localStorage.getItem('darkMode') === '1';
    document.body.classList.toggle('dark-mode', isDarkMode);

    document.querySelectorAll('.dark-mode-switch').forEach(switcher => {
        switcher.checked = isDarkMode;
        switcher.addEventListener('change', (e) => {
            if (e.target.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('darkMode', '1');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', '0');
            }
            console.log("Dark mode toggled:", e.target.checked);
        });
    });

    // ✅ Sidebar Toggle Handling
    document.body.addEventListener('click', (e) => {
        if (e.target.classList.contains('sidebar-toggle')) {
            let sidebar = new bootstrap.Modal(document.getElementById("sidebarPanel"));
            sidebar.show();
        } else if (e.target.classList.contains('sidebar-close')) {
            let sidebar = bootstrap.Modal.getInstance(document.getElementById("sidebarPanel"));
            if (sidebar) sidebar.hide();
        }
    });

    // ✅ Initialize Splide Carousel if Exists
    const carouselEl = document.querySelector('.carousel');
    if (carouselEl) {
        new Splide(carouselEl, {
            perPage: 3,
            rewind: true,
            gap: '16px',
            pagination: false,
            breakpoints: {
                768: { perPage: 2 },
                991: { perPage: 1 }
            }
        }).mount();
    } else {
        console.warn("No element found for '.carousel'");
    }

    // ✅ Ensure data-original is set on page load
    const elements = ['balance-value', 'credit-value', 'debit-value'];
    elements.forEach(id => {
        const element = document.getElementById(id);
        if (element && !element.hasAttribute('data-original')) {
            element.setAttribute('data-original', element.innerHTML);
        }
    });

    // ✅ Toggle visibility function (Hides & Shows Sensitive Data)
    window.toggleAllVisibility = function () {
        const elements = ['balance-value', 'credit-value', 'debit-value'];
        const eyeIcon = document.getElementById('balance-eye');
    
        const isHidden = document.getElementById('balance-value')?.getAttribute("data-hidden") === "true";
    
        elements.forEach(id => {
            const el = document.getElementById(id);
            if (!el) return;
    
            if (isHidden) {
                el.innerHTML = el.getAttribute("data-original");
                el.setAttribute("data-hidden", "false");
            } else {
                el.setAttribute("data-original", el.innerHTML);
                el.innerHTML = "***";
                el.setAttribute("data-hidden", "true");
            }
        });
    
            if (eyeIcon) {
                eyeIcon.setAttribute("name", isHidden ? "eye-outline" : "eye-off-outline");
            }
        };
    
    });
    

document.addEventListener("DOMContentLoaded", function () {
    // Initialize sendActionSheet modal if the element exists
    let sendActionSheet = document.getElementById("sendActionSheet");
    if (sendActionSheet) {
        new bootstrap.Modal(sendActionSheet);
    }
});

document.addEventListener("DOMContentLoaded", function () {
    function loadNotifications() {
        fetch(getNotificationsUrl)
            .then(response => response.json())
            .then(data => {
                const notificationCount = document.getElementById("notification-count");
                const notificationList = document.getElementById("notification-list");

                if (notificationCount && notificationList) {
                    // Update notification count
                    notificationCount.innerText = data.unread_count || 0;

                    // Populate notification list
                    notificationList.innerHTML = data.notifications.length
                        ? data.notifications.map(notif => `<a class="dropdown-item">${notif.message}</a>`).join("")
                        : "<p class='dropdown-item'>No new notifications</p>";
                }
            })
            .catch(error => console.error("Error loading notifications:", error));
    }

    // Initial load and periodic refresh every 10 seconds
    loadNotifications();
    setInterval(loadNotifications, 10000);
});

// Transfer Money Modal Handling

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("transferForm").addEventListener("submit", function (event) {
        event.preventDefault();  // Prevent full page reload

        let formData = new FormData(this);
        let transferMessage = document.getElementById("transferMessage");

        fetch(transferMoneyUrl, {  // Changed to use global variable
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(errorText => { throw new Error(errorText) });
            }
            return response.json();
        })
        .then(data => {
            transferMessage.style.display = "block";
            if (data.success) {
                transferMessage.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
                document.getElementById("transferForm").reset(); // Clear form
                updateBalance(data.new_balance);
                setTimeout(() => {
                    transferMessage.style.display = "none";
                    closeModal();
                }, 2000);
            } else {
                transferMessage.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
            }
        })
        .catch(error => console.error("Error:", error));
    });

    function updateBalance(newBalance) {
        let balanceElement = document.getElementById("userBalance"); // Ensure this ID exists in your dashboard
        if (balanceElement) {
            balanceElement.textContent = `$${newBalance.toFixed(2)}`;
        }
    }

    function closeModal() {
        let modal = document.getElementById("sendActionSheet");
        let bootstrapModal = bootstrap.Modal.getInstance(modal);
        if (bootstrapModal) {
            bootstrapModal.hide();
        }
    }

    // Confirm 'sendActionSheet' exists in your HTML and is a proper Bootstrap modal
});