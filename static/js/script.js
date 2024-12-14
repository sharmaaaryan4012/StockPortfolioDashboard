let timeoutSeconds = Math.floor(sessionTimeoutMs / 1000);

function updateTimer() {
    const minutes = Math.floor(timeoutSeconds / 60);
    const seconds = timeoutSeconds % 60;
    const timerElement = document.getElementById('timeout-timer');
    if (timerElement) {
        timerElement.textContent = `Timeout: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    if (timeoutSeconds > 0) {
        timeoutSeconds--;
    } else {
        clearInterval(timerInterval);
        alert("Your session has expired. You will be logged out.");
        window.location.href = "/logout"; // Redirect to logout
    }
}

const timerInterval = setInterval(updateTimer, 1000);