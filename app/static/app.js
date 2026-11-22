'use strict';

const $ = (id) => document.getElementById(id);
let allTasks = [];
let toastTimer;

function showToast(message) {
  const toast = $('toast');
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3500);
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const data = await response.json();
      if (typeof data.detail === 'string') detail = data.detail;
    } catch (_) { /* response may not be JSON */ }
    throw new Error(detail);
  }
  return response.json();
}

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function formatDueDate(value) {
  if (!value) return '';
  const day = new Date(`${value}T12:00:00`);
  if (Number.isNaN(day.getTime())) return value;
  return `◷ ${day.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}`;
}

function renderTasks() {
  const search = $('search-tasks').value.toLowerCase().trim();
  const filter = $('filter-tasks').value;
  const visible = allTasks.filter((task) => {
    const matchesSearch = `${task.title} ${task.description || ''}`.toLowerCase().includes(search);
    const matchesStatus = filter === 'all' || (filter === 'completed' ? task.completed : !task.completed);
    return matchesSearch && matchesStatus;
  });
  const list = $('task-list');
  list.replaceChildren();

  if (!visible.length) {
    const empty = element('div', 'empty-state');
    empty.append(element('span', 'empty-graphic', '☑'));
    empty.append(element('strong', '', allTasks.length ? 'Nothing matches your filters' : 'A fresh start!'));
    empty.append(element('span', '', allTasks.length ? 'Try another search or filter.' : 'Add your first task to get started.'));
    list.append(empty);
  }

  for (const task of visible) {
    const row = element('article', `task-item${task.completed ? ' is-done' : ''}`);
    const checkbox = element('button', `task-check${task.completed ? ' checked' : ''}`, task.completed ? '✓' : '');
    checkbox.type = 'button';
    checkbox.setAttribute('aria-label', `${task.completed ? 'Mark not completed' : 'Mark completed'}: ${task.title}`);
    checkbox.addEventListener('click', () => updateTask(task.id, { completed: !task.completed }));

    const copy = element('div', 'task-copy');
    copy.append(element('div', 'task-name', task.title));
    if (task.description) copy.append(element('div', 'task-description', task.description));
    const meta = element('div', 'task-meta');
    meta.append(element('span', `priority-tag priority-${task.priority}`, `${task.priority} priority`));
    if (task.due_date) meta.append(element('span', 'date-tag', formatDueDate(task.due_date)));
    copy.append(meta);

    const actions = element('div', 'task-actions');
    const edit = element('button', 'task-action', '✎');
    edit.type = 'button';
    edit.title = 'Edit task name';
    edit.setAttribute('aria-label', `Edit ${task.title}`);
    edit.addEventListener('click', async () => {
      const title = prompt('Edit task name:', task.title);
      if (title !== null && title.trim() && title.trim() !== task.title) {
        await updateTask(task.id, { title: title.trim() });
      }
    });
    const remove = element('button', 'task-action delete', '×');
    remove.type = 'button';
    remove.title = 'Delete task';
    remove.setAttribute('aria-label', `Delete ${task.title}`);
    remove.addEventListener('click', async () => {
      if (confirm(`Delete "${task.title}"?`)) await deleteTask(task.id);
    });
    actions.append(edit, remove);
    row.append(checkbox, copy, actions);
    list.append(row);
  }

  const completed = allTasks.filter((task) => task.completed).length;
  const total = allTasks.length;
  const percent = total ? Math.round((completed / total) * 100) : 0;
  $('total-tasks').textContent = String(total);
  $('completed-tasks').textContent = String(completed);
  $('remaining-tasks').textContent = String(total - completed);
  $('sidebar-count').textContent = String(total);
  $('task-count').textContent = String(total);
  $('visible-count').textContent = `${visible.length} task${visible.length === 1 ? '' : 's'} shown`;
  $('progress-percent').textContent = `${percent}%`;
  $('progress-ring-label').textContent = `${percent}%`;
  $('progress-ring').style.background = `conic-gradient(#7866ec ${percent}%, #eceaf7 ${percent}%)`;
}

async function loadTasks() {
  try {
    allTasks = await request('/tasks');
    renderTasks();
  } catch (error) {
    $('task-list').replaceChildren(element('div', 'empty-state', 'Unable to load tasks. Please try refreshing.'));
    showToast(error.message);
  }
}

async function updateTask(id, changes) {
  try {
    await request(`/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(changes) });
    await loadTasks();
    showToast('Task updated');
  } catch (error) { showToast(error.message); }
}

async function deleteTask(id) {
  try {
    await request(`/tasks/${id}`, { method: 'DELETE' });
    await loadTasks();
    showToast('Task deleted');
  } catch (error) { showToast(error.message); }
}

async function checkServer() {
  try {
    const [health, version] = await Promise.all([request('/health'), request('/version')]);
    $('server-status').textContent = health.status === 'ok' ? 'All systems operational' : 'Server unavailable';
    $('server-dot').classList.toggle('offline', health.status !== 'ok');
    $('version-label').textContent = `v${version.version}`;
  } catch (_) {
    $('server-status').textContent = 'Connection unavailable';
    $('server-dot').classList.add('offline');
  }
}

$('create-task-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const title = $('task-title').value.trim();
  if (!title) return;
  const payload = {
    title,
    description: $('task-description').value,
    priority: $('task-priority').value,
    due_date: $('task-due-date').value || null,
  };
  const button = $('submit-task');
  button.disabled = true;
  try {
    await request('/tasks', { method: 'POST', body: JSON.stringify(payload) });
    $('create-task-form').reset();
    $('form-message').textContent = '';
    await loadTasks();
    showToast('New task created!');
    $('task-title').focus();
  } catch (error) {
    $('form-message').textContent = error.message;
    showToast(error.message);
  } finally { button.disabled = false; }
});

$('search-tasks').addEventListener('input', renderTasks);
$('filter-tasks').addEventListener('change', renderTasks);
$('refresh-button').addEventListener('click', loadTasks);
$('today-label').textContent = new Date().toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
checkServer();
loadTasks();
