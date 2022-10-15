function handleRegisterSubmission() {
  window.event.preventDefault();
  const registerForm = window.event.target;
  const { username, email, password } = registerForm;
  if (!username.value || !email.value || !password.value) {
    const errorText = document.getElementById('errorText');
    errorText.style.display = 'block';
    return;
  }

  fetch('http://localhost:3000/api/register', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: username.value,
      email: email.value,
      password: password.value,
    }),
  })
    .then((res) => {
      console.log(res);
      return (window.location.href = '/');
    })
    .catch((err) => {
      console.log(err);
      return alert(err.message);
    });
}

function handleLogin() {
  window.event.preventDefault();
  const form = window.event.target;
  const username = form.username.value;
  const password = form.password.value;
  const errorText = document.getElementById('errorText');
  if (!username || !password) {
    errorText.style.display = 'block';
    return;
  }

  fetch('http://localhost:3000/api/login', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  })
    .then((res) => {
      res.json().then((data) => {
        if (data.success === false) {
          // Display error text if login was unsuccessful for any reason
          errorText.style.display = 'block';
          errorText.innerText = data.error;
          return;
        }
        if (errorText.style.display === 'block') {
          // Hide error text if successful login after failed attempt
          errorText.style.display = 'none';
        }
        Cookies.set('token', data.token);
        window.location.replace('/');
      });
    })
    .catch((err) => {
      console.log(err);
    });
}
