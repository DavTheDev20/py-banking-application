function handleRegisterSubmission() {
  window.event.preventDefault();
  const registerForm = window.event.target;
  const { username, email, password } = registerForm;
  if (!username.value || !email.value || !password.value) {
    const errorText = document.getElementById('errorText');
    errorText.style.display = 'block';
    return;
  }

  fetch('http://localhost:5000/api/register', {
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
