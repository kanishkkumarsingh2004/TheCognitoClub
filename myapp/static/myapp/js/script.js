document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });
    }
});

function convertUTCToIST(utcDateString) {
    const utcDate = new Date(utcDateString);
    const istOffset = 330; // IST is UTC+5:30
    return new Date(utcDate.getTime() + istOffset * 60000);
}

async function initializeCountdown() {
    try {
        const response = await fetch('/get-registration-deadline/');
        const data = await response.json();
        
        if (data.error) {
            console.error(data.error);
            return;
        }

        const countDownDate = convertUTCToIST(data.deadline).getTime();
        const registrationForm = document.getElementById("registration-form");

        const updateTimer = () => {
            const now = new Date().getTime();
            const distance = countDownDate - now;

            if (distance < 0) {
                clearInterval(timerInterval);
                document.getElementById("countdown-timer").innerHTML = "Registrations Closed!";
                if (registrationForm) {
                    registrationForm.style.display = "none";
                }
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            document.getElementById("days").innerText = String(days).padStart(2, '0');
            document.getElementById("hours").innerText = String(hours).padStart(2, '0');
            document.getElementById("minutes").innerText = String(minutes).padStart(2, '0');
            document.getElementById("seconds").innerText = String(seconds).padStart(2, '0');
        };

        const timerInterval = setInterval(updateTimer, 1000);
        updateTimer(); // Initial call
    } catch (error) {
        console.error('Error fetching registration deadline:', error);
    }
}

document.addEventListener("DOMContentLoaded", initializeCountdown);