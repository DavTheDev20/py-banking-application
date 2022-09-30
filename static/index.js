function handleRegisterSubmission() {
  window.event.preventDefault();
  const registerForm = window.event.target;
  const { username, email, password } = registerForm;
  if (!username.value || !email.value || !password.value) {
    const errorText = document.getElementById('errorText');
    errorText.style.display = 'block';
    return;
  }

  window.location.href = '/'; //Change this to navigate to valid location
}
