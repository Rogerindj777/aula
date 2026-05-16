/**
 * TaskFlow — app.js
 * Aplicação de gerenciamento de tarefas sem backend.
 * Persistência via localStorage simulando um db.json
 * com dois arrays: "users" e "todos".
 */

// ============================================================
// CAMADA DE PERSISTÊNCIA (Simula db.json no localStorage)
// ============================================================

/**
 * Lê com segurança um array do localStorage.
 * Retorna array vazio caso a chave não exista ou o JSON seja inválido.
 * @param {string} key - Chave do localStorage
 * @returns {Array}
 */
function readCollection(key) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    // Dado corrompido: retorna array vazio e limpa a chave
    localStorage.removeItem(key);
    return [];
  }
}

/**
 * Salva com segurança um array no localStorage.
 * @param {string} key  - Chave do localStorage
 * @param {Array}  data - Array a ser persistido
 */
function writeCollection(key, data) {
  try {
    localStorage.setItem(key, JSON.stringify(data));
  } catch (err) {
    // QuotaExceededError ou outro erro de armazenamento
    console.error(`[TaskFlow] Erro ao salvar "${key}" no localStorage:`, err);
  }
}

// Atalhos para as coleções
const db = {
  getUsers:    ()      => readCollection("users"),
  saveUsers:   (data)  => writeCollection("users", data),
  getTodos:    ()      => readCollection("todos"),
  saveTodos:   (data)  => writeCollection("todos", data),

  getCurrentUser: () => {
    try {
      const raw = localStorage.getItem("currentUser");
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },
  setCurrentUser:    (user) => localStorage.setItem("currentUser", JSON.stringify(user)),
  clearCurrentUser:  ()     => localStorage.removeItem("currentUser"),
};


// ============================================================
// ROTEAMENTO DE TELAS
// ============================================================

/**
 * Exibe somente a tela com o ID informado e oculta as demais.
 * @param {string} screenId - ID do elemento da tela
 */
function showScreen(screenId) {
  const screens = document.querySelectorAll(".screen");
  screens.forEach((screen) => {
    if (screen.id === screenId) {
      screen.classList.add("active");
    } else {
      screen.classList.remove("active");
    }
  });
}

/**
 * Decide qual tela mostrar com base no estado de autenticação.
 * Mantém o usuário logado ao recarregar a página.
 */
function initRouter() {
  const currentUser = db.getCurrentUser();
  if (currentUser) {
    enterDashboard(currentUser);
  } else {
    showScreen("screen-login");
  }
}


// ============================================================
// UTILITÁRIOS DE UI
// ============================================================

/**
 * Exibe uma mensagem de erro em um elemento de feedback.
 * @param {string} elementId - ID do container de erro
 * @param {string} message   - Texto da mensagem
 */
function showError(elementId, message) {
  const el = document.getElementById(elementId);
  if (!el) return;
  el.classList.remove("hidden");
  const msgSpan = el.querySelector("span") || el;
  msgSpan.textContent = message;
}

/**
 * Oculta um elemento de feedback de erro.
 * @param {string} elementId - ID do container de erro
 */
function hideError(elementId) {
  const el = document.getElementById(elementId);
  if (el) el.classList.add("hidden");
}

/**
 * Exibe mensagem de erro inline abaixo de um campo de formulário.
 * @param {string} fieldErrorId - ID do <p> de erro abaixo do campo
 * @param {string} message      - Mensagem de erro
 */
function showFieldError(fieldErrorId, message) {
  const el = document.getElementById(fieldErrorId);
  if (!el) return;
  el.textContent = message;
  el.classList.remove("hidden");
}

/**
 * Limpa todos os erros inline de um formulário.
 * @param {string[]} fieldErrorIds - Lista de IDs de elementos de erro
 */
function clearFieldErrors(fieldErrorIds) {
  fieldErrorIds.forEach((id) => {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = "";
      el.classList.add("hidden");
    }
  });
}

/**
 * Valida se o e-mail tem formato básico válido.
 * @param {string} email
 * @returns {boolean}
 */
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

/**
 * Formata o primeiro nome do usuário para a saudação.
 * @param {string} fullName
 * @returns {string}
 */
function getFirstName(fullName) {
  return (fullName || "").trim().split(" ")[0] || "Usuário";
}


// ============================================================
// AUTENTICAÇÃO
// ============================================================

/** Registra um novo usuário e redireciona para o login. */
function handleRegister(event) {
  event.preventDefault();

  const name     = document.getElementById("register-name").value.trim();
  const email    = document.getElementById("register-email").value.trim();
  const password = document.getElementById("register-password").value;

  // Limpa erros anteriores
  clearFieldErrors(["register-name-error", "register-email-error", "register-password-error"]);
  hideError("register-error");

  // --- Validação dos campos ---
  let hasError = false;

  if (!name) {
    showFieldError("register-name-error", "Por favor, informe seu nome.");
    hasError = true;
  }

  if (!email) {
    showFieldError("register-email-error", "Por favor, informe seu e-mail.");
    hasError = true;
  } else if (!isValidEmail(email)) {
    showFieldError("register-email-error", "Formato de e-mail inválido.");
    hasError = true;
  }

  if (!password) {
    showFieldError("register-password-error", "Por favor, crie uma senha.");
    hasError = true;
  } else if (password.length < 6) {
    showFieldError("register-password-error", "A senha deve ter pelo menos 6 caracteres.");
    hasError = true;
  }

  if (hasError) return;

  // --- Verifica duplicidade de e-mail ---
  const users = db.getUsers();
  const emailLower = email.toLowerCase();
  const alreadyExists = users.some((u) => u.email.toLowerCase() === emailLower);

  if (alreadyExists) {
    showError("register-error", "Este e-mail já está cadastrado. Faça login.");
    return;
  }

  // --- Persiste novo usuário ---
  const newUser = { name, email: emailLower, password };
  users.push(newUser);
  db.saveUsers(users);

  // Feedback e redirecionamento para login
  document.getElementById("form-register").reset();
  showScreen("screen-login");
  showError("login-error", "Conta criada com sucesso! Faça login.");
  // Muda cor para sucesso
  const loginError = document.getElementById("login-error");
  if (loginError) {
    loginError.classList.remove("bg-red-500/10", "border-red-500/30", "text-red-400");
    loginError.classList.add("bg-emerald-500/10", "border-emerald-500/30", "text-emerald-400");
  }
}

/** Autentica o usuário e redireciona para o dashboard. */
function handleLogin(event) {
  event.preventDefault();

  const email    = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;

  // Limpa erros
  clearFieldErrors(["login-email-error", "login-password-error"]);
  hideError("login-error");

  // Restaura estilo padrão do alerta de login (caso tenha sido verde)
  const loginError = document.getElementById("login-error");
  if (loginError) {
    loginError.classList.add("bg-red-500/10", "border-red-500/30", "text-red-400");
    loginError.classList.remove("bg-emerald-500/10", "border-emerald-500/30", "text-emerald-400");
  }

  // --- Validação de campos vazios ---
  let hasError = false;

  if (!email) {
    showFieldError("login-email-error", "Informe seu e-mail.");
    hasError = true;
  }

  if (!password) {
    showFieldError("login-password-error", "Informe sua senha.");
    hasError = true;
  }

  if (hasError) return;

  // --- Verifica credenciais ---
  const users = db.getUsers();
  const emailLower = email.toLowerCase();
  const user = users.find((u) => u.email.toLowerCase() === emailLower);

  if (!user) {
    showError("login-error", "E-mail não encontrado. Verifique ou crie uma conta.");
    return;
  }

  if (user.password !== password) {
    showError("login-error", "Senha incorreta. Tente novamente.");
    return;
  }

  // --- Login bem-sucedido ---
  db.setCurrentUser(user);
  document.getElementById("form-login").reset();
  enterDashboard(user);
}

/** Efetua logout: remove sessão e volta para o login. */
function handleLogout() {
  db.clearCurrentUser();
  showScreen("screen-login");
}


// ============================================================
// DASHBOARD
// ============================================================

/**
 * Configura e exibe o dashboard para o usuário logado.
 * @param {Object} user - Objeto do usuário logado
 */
function enterDashboard(user) {
  // Saudação com o primeiro nome
  const greeting = document.getElementById("dashboard-greeting");
  if (greeting) greeting.textContent = `Olá, ${getFirstName(user.name)} 👋`;

  showScreen("screen-dashboard");
  renderTaskList(user.email);
}


// ============================================================
// TAREFAS — CRUD
// ============================================================

/**
 * Adiciona uma nova tarefa ao localStorage.
 * Somente tarefas com título não-vazio são aceitas.
 */
function handleAddTask(event) {
  event.preventDefault();

  const titleInput = document.getElementById("task-title");
  const typeSelect = document.getElementById("task-type");
  const descArea   = document.getElementById("task-description");

  const title       = titleInput.value.trim();
  const type        = typeSelect.value;
  const description = descArea.value.trim();

  // Limpa erros anteriores
  hideError("task-form-error");

  // --- Validação: título obrigatório ---
  if (!title) {
    showError("task-form-error", "O título da tarefa é obrigatório.");
    titleInput.focus();
    return;
  }

  const currentUser = db.getCurrentUser();
  if (!currentUser) {
    handleLogout(); // Sessão expirada — redireciona para login
    return;
  }

  // --- Cria objeto da tarefa ---
  const newTodo = {
    id:          Date.now(),    // identificador único baseado em timestamp
    userId:      currentUser.email,
    title,
    type,
    description,
    done:        false,
  };

  // --- Persiste e atualiza UI ---
  const todos = db.getTodos();
  todos.push(newTodo);
  db.saveTodos(todos);

  // Limpa o formulário após adição bem-sucedida
  document.getElementById("form-task").reset();

  renderTaskList(currentUser.email);
}

/**
 * Marca uma tarefa como concluída no localStorage e atualiza a UI.
 * @param {number} taskId - ID (timestamp) da tarefa
 */
function completeTask(taskId) {
  const todos = db.getTodos();
  const taskIndex = todos.findIndex((t) => t.id === taskId);

  if (taskIndex === -1) return; // Tarefa não encontrada

  todos[taskIndex].done = true;
  db.saveTodos(todos);

  const currentUser = db.getCurrentUser();
  if (currentUser) renderTaskList(currentUser.email);
}


// ============================================================
// RENDERIZAÇÃO DA LISTA DE TAREFAS
// ============================================================

/**
 * Configurações visuais dos tipos de tarefa (badge).
 */
const TASK_TYPE_CONFIG = {
  trabalho: {
    label:   "💼 Trabalho",
    classes: "bg-blue-500/15 text-blue-300 border-blue-500/25",
  },
  pessoal: {
    label:   "🌿 Pessoal",
    classes: "bg-violet-500/15 text-violet-300 border-violet-500/25",
  },
  estudos: {
    label:   "📚 Estudos",
    classes: "bg-emerald-500/15 text-emerald-300 border-emerald-500/25",
  },
};

/**
 * Cria o elemento HTML de um card de tarefa.
 * @param {Object} task - Objeto da tarefa
 * @returns {HTMLElement}
 */
function createTaskCard(task) {
  const typeConfig = TASK_TYPE_CONFIG[task.type] || TASK_TYPE_CONFIG.trabalho;

  const card = document.createElement("div");
  card.id = `task-${task.id}`;
  card.className = [
    "task-card glass-card rounded-2xl p-5 mb-3",
    task.done ? "task-done" : "",
  ].join(" ");

  // Conteúdo interno do card
  card.innerHTML = `
    <div class="flex items-start justify-between gap-4">
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 flex-wrap mb-2">
          <span class="task-title font-semibold text-white text-sm leading-snug">${escapeHtml(task.title)}</span>
          <span class="text-xs font-medium px-2 py-0.5 rounded-full border ${typeConfig.classes}">
            ${typeConfig.label}
          </span>
        </div>
        ${
          task.description
            ? `<p class="text-slate-400 text-xs leading-relaxed mt-1">${escapeHtml(task.description)}</p>`
            : ""
        }
      </div>

      <div class="flex-shrink-0">
        ${
          task.done
            ? `<span class="btn-complete-done inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                </svg>
                Concluída
               </span>`
            : `<button
                 class="btn-complete inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-600/50 text-slate-400 text-xs font-medium"
                 onclick="completeTask(${task.id})"
                 aria-label="Marcar tarefa como concluída"
               >
                 <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                   <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                 </svg>
                 Concluir
               </button>`
        }
      </div>
    </div>
  `;

  return card;
}

/**
 * Escapa caracteres especiais HTML para evitar XSS.
 * @param {string} text
 * @returns {string}
 */
function escapeHtml(text) {
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
  return String(text).replace(/[&<>"']/g, (char) => map[char]);
}

/**
 * Renderiza a lista completa de tarefas do usuário logado.
 * Tarefas pendentes aparecem antes das concluídas.
 * Atualiza também o contador de progresso.
 * @param {string} userEmail - E-mail do usuário logado
 */
function renderTaskList(userEmail) {
  const container = document.getElementById("task-list");
  if (!container) return;

  // Filtra apenas as tarefas do usuário logado
  const allTodos  = db.getTodos();
  const userTodos = allTodos.filter((t) => t.userId === userEmail);

  // Ordena: pendentes primeiro, concluídas no final
  const pending   = userTodos.filter((t) => !t.done);
  const done      = userTodos.filter((t) => t.done);
  const sorted    = [...pending, ...done];

  // Atualiza o contador de progresso
  updateProgressCounter(userTodos.length, done.length);

  // Limpa o container antes de re-renderizar
  container.innerHTML = "";

  // Exibe mensagem vazia quando não há tarefas
  if (sorted.length === 0) {
    container.innerHTML = `
      <div class="text-center py-16 text-slate-500">
        <svg class="w-12 h-12 mx-auto mb-4 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
        </svg>
        <p class="text-sm font-medium">Nenhuma tarefa cadastrada ainda.</p>
        <p class="text-xs mt-1 opacity-60">Adicione sua primeira tarefa acima.</p>
      </div>
    `;
    return;
  }

  // Cria e adiciona os cards com delay de animação escalonado
  sorted.forEach((task, index) => {
    const card = createTaskCard(task);
    card.style.animationDelay = `${index * 60}ms`;
    container.appendChild(card);
  });
}

/**
 * Atualiza o contador de tarefas e a barra de progresso no topo do dashboard.
 * @param {number} total - Total de tarefas do usuário
 * @param {number} doneCount - Quantidade de tarefas concluídas
 */
function updateProgressCounter(total, doneCount) {
  const totalEl    = document.getElementById("counter-total");
  const doneEl     = document.getElementById("counter-done");
  const progressBar = document.getElementById("progress-bar");

  if (totalEl) {
    totalEl.textContent = total === 1 ? "1 tarefa no total" : `${total} tarefas no total`;
  }

  if (doneEl) {
    doneEl.textContent = doneCount === 1 ? "1 concluída" : `${doneCount} concluídas`;
  }

  if (progressBar) {
    const pct = total > 0 ? Math.round((doneCount / total) * 100) : 0;
    progressBar.style.width = `${pct}%`;
  }
}


// ============================================================
// INICIALIZAÇÃO — EVENT LISTENERS
// ============================================================

/**
 * Registra todos os listeners de eventos e inicializa o roteador.
 * Chamado quando o DOM estiver completamente carregado.
 */
function init() {
  // --- Formulário de Login ---
  const formLogin = document.getElementById("form-login");
  if (formLogin) formLogin.addEventListener("submit", handleLogin);

  // --- Formulário de Cadastro ---
  const formRegister = document.getElementById("form-register");
  if (formRegister) formRegister.addEventListener("submit", handleRegister);

  // --- Formulário de Nova Tarefa ---
  const formTask = document.getElementById("form-task");
  if (formTask) formTask.addEventListener("submit", handleAddTask);

  // --- Botão de Logout ---
  const btnLogout = document.getElementById("btn-logout");
  if (btnLogout) btnLogout.addEventListener("click", handleLogout);

  // --- Navegação entre telas de auth ---
  const gotoRegister = document.getElementById("goto-register");
  if (gotoRegister) {
    gotoRegister.addEventListener("click", () => {
      hideError("register-error");
      clearFieldErrors(["register-name-error", "register-email-error", "register-password-error"]);
      showScreen("screen-register");
    });
  }

  const gotoLogin = document.getElementById("goto-login");
  if (gotoLogin) {
    gotoLogin.addEventListener("click", () => {
      hideError("login-error");
      clearFieldErrors(["login-email-error", "login-password-error"]);
      showScreen("screen-login");
    });
  }

  // --- Decide qual tela exibir com base na sessão ---
  initRouter();
}

// Aguarda o DOM estar pronto antes de inicializar
document.addEventListener("DOMContentLoaded", init);
