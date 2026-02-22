function validateEmail(email) {
    if (!email.includes('@') || !email.includes('.')) {
        alert('Некорректный email. Должен содержать @ и .');
        return false;
    }
    return true;
}

function validatePassword(password) {
    if (password.length < 6) {
        alert('Пароль должен быть минимум 6 символов');
        return false;
    }
    return true;
}

function validateUsername(username) {
    if (username.length < 3) {
        alert('Имя должно быть минимум 3 символа');
        return false;
    }
    return true;
}

async function realRegister() {
    let email = prompt('Email:');
    let username = prompt('Имя пользователя:');
    let password = prompt('Пароль:');

    if (!validateEmail(email)) return;
    if (!validateUsername(username)) return;
    if (!validatePassword(password)) return;

    try {
        let response = await fetch('/auth/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, username, password})
        });
        let data = await response.json();
        if (response.ok) {
            localStorage.setItem('token', data.data.token);
            localStorage.setItem('user', JSON.stringify(data.data.user));
            alert('Регистрация успешна!');
            location.reload();
        } else {
            alert('Ошибка: ' + (data.error));
        }
    } catch (error) {
        alert('Упс...');
    }
}

async function realLogin() {
    let email = prompt('Email:');
    let password = prompt('Пароль:');

    if (!validateEmail(email)) return;
    if (!validatePassword(password)) return;

    try {
        let response = await fetch('/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, password})
        });
        let data = await response.json();
        if (response.ok) {
            localStorage.setItem('token', data.data.token);
            localStorage.setItem('user', JSON.stringify(data.data.user));
            alert('Вход выполнен!');
            location.reload();
        } else {
            alert('Ошибка: ' + (data.error));
        }
    } catch (error) {
        alert('Упс...');
    }
}