const apiUrl = 'your api url';
console.log('Token has been deleted');

async function loginUser() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    try {
        const response = await fetch(`${apiUrl}/login`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log('User registered successfully');
        const data = await response.json();
        token = data.access_token;
        id = data.access_id;
        console.log('Logged in successfully');
        localStorage.setItem('token', token);
        localStorage.setItem('userid', id);
        localStorage.setItem('username', username);
        window.location.href = 'index.html';
    } catch (error) {
        console.error('Error logging in user:', error);
        alert(error.message);
    }
}


