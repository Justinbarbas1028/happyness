document.addEventListener('DOMContentLoaded', () => {
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  const btn = document.getElementById('helloBtn');
  const msg = document.getElementById('helloMsg');
  if (btn && msg) {
    btn.addEventListener('click', () => {
      msg.textContent = 'Hello from static JS!';
      msg.classList.remove('hidden');
    });
  }
});
