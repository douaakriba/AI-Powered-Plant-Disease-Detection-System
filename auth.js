/**
 * auth.js — PhytoSentinel
 * Module d'authentification centralisé
 *
 * - Stockage : localStorage (token + user)
 * - Backend  : /api/auth/login | /api/auth/verify
 * - Rôles    : admin → pages admin uniquement | farmer/expert/technician → pages utilisateur uniquement
 *
 * ── PROTECTION DES PAGES ──────────────────────────────────────────────────────
 *  • Pages ADMIN   : index.html, alertes.html, carte.html, database.html,
 *                    maladies.html, rapports.html
 *    → Accessibles UNIQUEMENT au rôle "admin"
 *    → Tout autre rôle connecté est redirigé vers agriculteur.html
 *
 *  • Pages FARMER  : agriculteur.html, detection.html, parametres.html
 *    → Accessibles aux rôles farmer / expert / technician
 *    → Un admin qui tente d'y accéder est redirigé vers index.html
 *
 *  • login.html    : si déjà connecté, redirection automatique selon le rôle
 */

const API_BASE = "http://localhost:5000";

const STORAGE_TOKEN = "phyto_token";
const STORAGE_USER  = "phyto_user";

// ── Définition des zones de pages ─────────────────────────────────────────────

/** Pages réservées à l'admin */
const ADMIN_PAGES = [
  "index.html",
  "alertes.html",
  "carte.html",
  "database.html",
  "maladies.html",
  "rapports.html",
  "detection.html",
];

/** Pages réservées aux utilisateurs (non-admin) */
const USER_PAGES = [
  "agriculteur.html",
  "detection.html",
  "parametres.html",
];

/** Page d'accueil selon le rôle */
const ROLE_HOME = {
  admin:      "index.html",
  farmer:     "agriculteur.html",
  expert:     "agriculteur.html",
  technician: "agriculteur.html",
};

// ── Lecture du stockage ────────────────────────────────────────────────────────

function getToken() {
  return localStorage.getItem(STORAGE_TOKEN) || null;
}

function getUser() {
  try {
    const raw = localStorage.getItem(STORAGE_USER);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function isAuthenticated() {
  return !!getToken();
}

// ── Écriture / suppression ────────────────────────────────────────────────────

function saveSession(token, user) {
  localStorage.setItem(STORAGE_TOKEN, token);
  localStorage.setItem(STORAGE_USER, JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem(STORAGE_TOKEN);
  localStorage.removeItem(STORAGE_USER);
}

// ── Déconnexion ───────────────────────────────────────────────────────────────

function logout() {
  clearSession();
  window.location.href = "login.html";
}

// ── Redirection après connexion ───────────────────────────────────────────────

function redirectByRole(user) {
  const page = ROLE_HOME[user.role] || "agriculteur.html";
  window.location.replace(page);
}

// ── Vérification serveur (silencieuse) ────────────────────────────────────────

async function verifyTokenOnServer() {
  const token = getToken();
  if (!token) return false;
  try {
    const res = await fetch(`${API_BASE}/api/auth/verify`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) return true;
    clearSession();
    return false;
  } catch {
    // Serveur injoignable → on laisse continuer (mode offline/dev)
    return true;
  }
}

// ── Injection du nom/rôle dans l'interface ───────────────────────────────────

function injectUserInfo(
  nameSelector = "#sidebarUserName",
  roleSelector = null,
) {
  const user = getUser();
  if (!user) return;

  const nameEl = document.querySelector(nameSelector);
  if (nameEl) nameEl.textContent = user.full_name || user.username;

  if (roleSelector) {
    const roleEl = document.querySelector(roleSelector);
    const labels = {
      admin:      "Administrateur",
      expert:     "Expert",
      technician: "Technicien",
      farmer:     "Agriculteur",
    };
    if (roleEl) roleEl.textContent = labels[user.role] || user.role;
  }
}

// ── Protection automatique des pages ──────────────────────────────────────────
// Ce bloc s'exécute immédiatement à l'inclusion du script sur n'importe quelle page.

(function protectPage() {
  const pathname = window.location.pathname;
  // Récupère uniquement le nom du fichier (ex: "index.html")
  const pageName = pathname.split("/").pop() || "index.html";

  const onLoginPage = pageName === "login.html";
  const onAdminPage = ADMIN_PAGES.includes(pageName);
  const onUserPage  = USER_PAGES.includes(pageName);

  // ── Page de connexion ──────────────────────────────────────────────────────
  if (onLoginPage) {
    // Déjà connecté → redirection immédiate vers la bonne zone
    if (isAuthenticated()) {
      const user = getUser();
      if (user) {
        redirectByRole(user);
      }
    }
    return; // Rien d'autre à faire sur login.html
  }

  // ── Toutes les autres pages : l'utilisateur doit être connecté ────────────
  if (!isAuthenticated()) {
    window.location.replace("login.html");
    return;
  }

  const user = getUser();

  // ── Page ADMIN : accès réservé au rôle "admin" ────────────────────────────
  if (onAdminPage && user && user.role !== "admin") {
    // Un farmer/expert/technician tente d'accéder à une page admin → renvoi
    window.location.replace("agriculteur.html");
    return;
  }

  // ── Page FARMER/USER : interdite à l'admin ────────────────────────────────
  if (onUserPage && user && user.role === "admin") {
    // L'admin n'a pas d'interface utilisateur → renvoi vers son tableau de bord
    window.location.replace("index.html");
    return;
  }

  // ── Token valide : vérification asynchrone en arrière-plan ───────────────
  verifyTokenOnServer().catch(() => { /* silencieux */ });
})();