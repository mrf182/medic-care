// Handle registration form submission
document.getElementById('registrationForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    fetch('/register', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            // Handle HTTP errors
            return response.json().then(data => {
                throw new Error(data.message || 'Registration failed');
            });
        }
        return response.json();
    })
    .then(data => {
        // Handle success or error
        const messageElement = document.getElementById('registrationMessage');
        if (data.success) {
            messageElement.innerHTML = '<div class="alert alert-success">Registration successful!</div>';
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } else {
            messageElement.innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const messageElement = document.getElementById('registrationMessage');
        messageElement.innerHTML = '<div class="alert alert-danger">' + error.message + '</div>';
    });
});


