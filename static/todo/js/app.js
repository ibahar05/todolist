/* ============================================================
   TASKFLOW — app.js (Pure Frontend Interactions Only)
   ============================================================ */

const Config = {
  TOAST_DURATION: 3000,
};

/* ============================================================
   2. TOAST NOTIFICATIONS
   ============================================================ */
const Toast = (() => {
  function getContainer() {
    return document.getElementById('toastContainer');
  }

  function show(message, type = 'info') {
    const container = getContainer();
    if (!container) return;

    const icons = { info: 'ℹ️', success: '✅', error: '❌', warning: '⚠️' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <span class="toast-icon">${icons[type] || icons.info}</span>
      <span class="toast-text">${message}</span>
      <div class="toast-progress"></div>
    `;

    container.appendChild(toast);
    const timer = setTimeout(() => dismiss(toast), Config.TOAST_DURATION);

    toast.addEventListener('click', () => {
      clearTimeout(timer);
      dismiss(toast);
    });
  }

  function dismiss(toast) {
    toast.classList.add('removing');
    toast.addEventListener('animationend', () => toast.remove(), { once: true });
  }

  return { show };
})();

/* ============================================================
   3. DASHBOARD CONTROLLER (Pure Interaction & Filter)
   ============================================================ */
const Dashboard = (() => {
  let state = {
    filter:  'all',
    search:  '',
  };

  let el = {};

  function init() {
    el = {
      taskList:      document.getElementById('taskList'),
      emptyState:    document.getElementById('emptyState'),
      addTaskForm:   document.getElementById('addTaskForm'),
      addTaskBtn:    document.getElementById('addTaskBtn'),
      saveNewTask:   document.getElementById('saveNewTask'),
      cancelNewTask: document.getElementById('cancelNewTask'),
      newTaskInput:  document.getElementById('newTaskInput'),
      searchInput:   document.getElementById('searchInput'),
      filterTabs:    document.querySelectorAll('.filter-tab'),
      sidebar:       document.getElementById('sidebar'),
      sidebarOverlay:document.getElementById('sidebarOverlay'),
      menuToggle:    document.getElementById('menuToggle'),
    };

    bindEvents();
    setupDjangoInteractions();
    checkEmptyStateOnLoad();
  }

 function bindEvents() {
    // --- باز کردن فرم برای تسک جدید (با تنظیم اکشن روی Create) ---
    if (el.addTaskBtn) {
      el.addTaskBtn.addEventListener('click', () => {
        openAddForm();
        if (el.addTaskForm) el.addTaskForm.action = "/task/create/"; // آدرس ساخت تسک جدید
        const formLabel = document.getElementById('formLabel');
        if (formLabel) formLabel.textContent = "Task name";
      });
    }

    if (el.cancelNewTask) el.cancelNewTask.addEventListener('click', closeAddForm);

    // --- ثبت فرم (چه برای ساخت و چه برای آپدیت) ---
    if (el.saveNewTask) el.saveNewTask.addEventListener('click', submitNewTask);

    if (el.newTaskInput) {
      el.newTaskInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeAddForm();
      });
    }

    // --- مدیریت کلیک روی دکمه‌های ادیتِ تسک‌ها (Event Delegation) ---
    if (el.taskList) {
      el.taskList.addEventListener('click', (e) => {
        const editBtn = e.target.closest('.edit-task-btn');
        if (editBtn) {
          const updateUrl = editBtn.dataset.url;
          const currentTitle = editBtn.dataset.title;

          openAddForm();
          
          // تغییر پویای اکشن فرم به آدرس آپدیت جنگو و پر کردن مقدار اینپوت
          if (el.addTaskForm) el.addTaskForm.action = updateUrl; 
          if (el.newTaskInput) el.newTaskInput.value = currentTitle;
          
          const formLabel = document.getElementById('formLabel');
          if (formLabel) formLabel.textContent = "Edit Task";
        }
      });
    }

    // --- Search Input ---
    if (el.searchInput) {
      el.searchInput.addEventListener('input', () => {
        state.search = el.searchInput.value.trim().toLowerCase();
        setFilter(state.filter);
      });
    }

    // --- Filter Tabs ---
    el.filterTabs.forEach(tab => {
      tab.addEventListener('click', () => setFilter(tab.dataset.filter));
    });

    // --- Mobile Menu Toggle ---
    if (el.menuToggle) {
      el.menuToggle.addEventListener('click', () => {
        if (el.sidebar) el.sidebar.classList.toggle('open');
        if (el.sidebarOverlay) el.sidebarOverlay.classList.toggle('visible');
      });
    }
    if (el.sidebarOverlay) {
      el.sidebarOverlay.addEventListener('click', () => {
        if (el.sidebar) el.sidebar.classList.remove('open');
        if (el.sidebarOverlay) el.sidebarOverlay.classList.remove('visible');
      });
    }
  }

  // مدیریت فرانت‌آندی چک‌باکس‌ها (برای فعال کردن اینپوت‌ها و نمایش انیمیشن خط خوردن)
  function setupDjangoInteractions() {
    if (!el.taskList) return;

    const checkboxes = el.taskList.querySelectorAll('.task-checkbox');
    checkboxes.forEach(cb => {
      cb.removeAttribute('disabled');
      cb.addEventListener('change', (e) => {
        const card = cb.closest('.task-card');
        if (card) {
          card.classList.toggle('completed', cb.checked);
          Toast.show(cb.checked ? 'Task marked as completed! ✓' : 'Task marked as active.', cb.checked ? 'success' : 'info');
          
          // برای اینکه آمار به صورت واقعی در دیتابیس بروزرسانی شود، فرم یا درخواستی باید ارسال شود
          const toggleForm = card.querySelector('.toggle-task-form');
          if (toggleForm) {
            toggleForm.submit();
          }
        }
      });
    });
  }

  function openAddForm() {
    if (el.addTaskForm) el.addTaskForm.classList.remove('hidden');
    if (el.newTaskInput) el.newTaskInput.focus();
    if (el.addTaskBtn) el.addTaskBtn.classList.add('hidden');
    if (el.emptyState) el.emptyState.classList.add('hidden');
  }

  function closeAddForm() {
    if (el.addTaskForm) el.addTaskForm.classList.add('hidden');
    if (el.newTaskInput) el.newTaskInput.value = '';
    if (el.addTaskBtn) el.addTaskBtn.classList.remove('hidden');
    checkEmptyStateOnLoad();
  }

  function submitNewTask(e) {
    if (e) e.preventDefault();

    const title = el.newTaskInput.value.trim();
    if (!title) {
      el.newTaskInput.focus();
      Toast.show('Please enter a task name.', 'warning');
      return;
    }

    const formElement = el.newTaskInput.closest('form');
    if (formElement) {
      Toast.show('Saving to server...', 'success');
      formElement.submit();
    }
  }

  function setFilter(filter) {
    state.filter = filter;
    el.filterTabs.forEach(tab => tab.classList.toggle('active', tab.dataset.filter === filter));
    
    if (!el.taskList) return;
    const taskCards = el.taskList.querySelectorAll('.task-card');
    let visibleCount = 0;

    taskCards.forEach(card => {
      const isCompleted = card.classList.contains('completed');
      const titleEl = card.querySelector('.task-title');
      const taskTitle = titleEl ? titleEl.textContent.toLowerCase() : '';
      
      const matchesFilter = filter === 'all' || 
                            (filter === 'active' && !isCompleted) || 
                            (filter === 'completed' && isCompleted);
                            
      const matchesSearch = taskTitle.includes(state.search);

      if (matchesFilter && matchesSearch) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    if (el.emptyState) {
      if (visibleCount === 0) el.emptyState.classList.remove('hidden');
      else el.emptyState.classList.add('hidden');
    }
  }

  function checkEmptyStateOnLoad() {
    if (!el.taskList || !el.emptyState) return;
    const total = el.taskList.querySelectorAll('.task-card').length;
    if (total === 0) el.emptyState.classList.remove('hidden');
    else el.emptyState.classList.add('hidden');
  }

  return { init };
})();

document.addEventListener('DOMContentLoaded', () => {
  Dashboard.init();
});