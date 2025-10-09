document.getElementById('load').addEventListener('click', async () => {
  // Виклик API
  const response = await fetch('/items');
  const items = await response.json();

  // Відображення даних у списку
  const list = document.getElementById('list');
  list.innerHTML = '';  // очищення списку перед додаванням

  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item.name;
    list.appendChild(li);
  });
});