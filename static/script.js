document.getElementById('load').addEventListener('click', async () => {
  const response = await fetch('/items');
  const items = await response.json();

  const list = document.getElementById('list');
  list.innerHTML = '';

  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item.name;
    list.appendChild(li);
  });
});