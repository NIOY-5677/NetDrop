/**
 * NETDROP DYNAMIC THEME ENGINE (DUAL SYNC: DISK SERVER + LOCALSTORAGE)
 */

const DEFAULT_THEMES = [
  {
    "id": "warm",
    "name": "Cálido Terracota",
    "bgBase": "#faf8f5",
    "surface": "#ffffff",
    "surfaceHover": "#f3efe9",
    "text": "#1a1a1a",
    "textHeading": "#111111",
    "textMuted": "#666360",
    "accent": "#c85a32",
    "accentHover": "#b04923",
    "accentBg": "rgba(200, 90, 50, 0.08)",
    "border": "#e6e2dc",
    "borderHover": "#c5c0b8",
    "danger": "#c93b2b",
    "dangerHover": "#a82e20",
    "dangerBg": "rgba(201, 59, 43, 0.08)"
  },
  {
    "id": "dark-slate",
    "name": "Oscuro Minimal",
    "bgBase": "#0f172a",
    "surface": "#1e293b",
    "surfaceHover": "#334155",
    "text": "#cbd5e1",
    "textHeading": "#f8fafc",
    "textMuted": "#94a3b8",
    "accent": "#6366f1",
    "accentHover": "#4f46e5",
    "accentBg": "rgba(99, 102, 241, 0.15)",
    "border": "#334155",
    "borderHover": "#475569",
    "danger": "#ef4444",
    "dangerHover": "#dc2626",
    "dangerBg": "rgba(239, 68, 68, 0.15)"
  },
  {
    "id": "forest",
    "name": "Bosque Verde",
    "bgBase": "#f2f7f4",
    "surface": "#ffffff",
    "surfaceHover": "#e5efe9",
    "text": "#2d3d34",
    "textHeading": "#0f1f16",
    "textMuted": "#527060",
    "accent": "#2d6a4f",
    "accentHover": "#1b4332",
    "accentBg": "rgba(45, 106, 79, 0.1)",
    "border": "#d3e3da",
    "borderHover": "#b7d1c3",
    "danger": "#bc4749",
    "dangerHover": "#9b2226",
    "dangerBg": "rgba(188, 71, 73, 0.1)"
  },
  {
    "id": "midnight-amber",
    "name": "Noche Ámbar",
    "bgBase": "#1a1918",
    "surface": "#262422",
    "surfaceHover": "#33302c",
    "text": "#d6d2c9",
    "textHeading": "#ffffff",
    "textMuted": "#9c9689",
    "accent": "#d97706",
    "accentHover": "#b45309",
    "accentBg": "rgba(217, 119, 6, 0.15)",
    "border": "#3a3733",
    "borderHover": "#4d4944",
    "danger": "#e11d48",
    "dangerHover": "#be123c",
    "dangerBg": "rgba(225, 29, 72, 0.15)"
  },
  {
    "id": "nordic",
    "name": "Nórdico Frío",
    "bgBase": "#f0f4f8",
    "surface": "#ffffff",
    "surfaceHover": "#e1e9f0",
    "text": "#334155",
    "textHeading": "#0f172a",
    "textMuted": "#64748b",
    "accent": "#2563eb",
    "accentHover": "#1d4ed8",
    "accentBg": "rgba(37, 99, 235, 0.1)",
    "border": "#cbd5e1",
    "borderHover": "#94a3b8",
    "danger": "#e11d48",
    "dangerHover": "#be123c",
    "dangerBg": "rgba(225, 29, 72, 0.1)"
  }
];

function applyThemeVariables(theme, syncServer = true) {
    if (!theme) return;
    const root = document.documentElement;

    if (theme.bgBase) {
        root.style.setProperty('--color-bg-base', theme.bgBase);
        if (document.body) {
            document.body.style.backgroundColor = theme.bgBase;
        }
    }
    if (theme.surface) root.style.setProperty('--color-surface', theme.surface);
    if (theme.surfaceHover) root.style.setProperty('--color-surface-hover', theme.surfaceHover);
    if (theme.text) root.style.setProperty('--color-text', theme.text);
    if (theme.textHeading) root.style.setProperty('--color-text-heading', theme.textHeading);
    if (theme.textMuted) root.style.setProperty('--color-text-muted', theme.textMuted);
    if (theme.accent) root.style.setProperty('--color-accent', theme.accent);
    if (theme.accentHover) root.style.setProperty('--color-accent-hover', theme.accentHover);
    if (theme.accentBg) root.style.setProperty('--color-accent-bg', theme.accentBg);
    if (theme.border) root.style.setProperty('--color-border', theme.border);
    if (theme.borderHover) root.style.setProperty('--color-border-hover', theme.borderHover);
    if (theme.danger) root.style.setProperty('--color-danger', theme.danger);
    if (theme.dangerHover) root.style.setProperty('--color-danger-hover', theme.dangerHover);
    if (theme.dangerBg) root.style.setProperty('--color-danger-bg', theme.dangerBg);

    // Guardar en localStorage
    try {
        localStorage.setItem('netdrop_active_theme_data', JSON.stringify(theme));
    } catch (e) {}

    // Persistir en servidor (para Escritorio pywebview / Móvil)
    if (syncServer && window.fetch) {
        fetch('/api/theme', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(theme)
        }).catch(() => {});
    }
}

async function initThemeEngine() {
    // 1. Carga ultra-rápida desde localStorage (si existe)
    let applied = false;
    try {
        const savedThemeData = localStorage.getItem('netdrop_active_theme_data');
        if (savedThemeData) {
            const theme = JSON.parse(savedThemeData);
            applyThemeVariables(theme, false);
            applied = true;
        }
    } catch (e) {}

    // 2. Si no hay localStorage o estamos en app de escritorio WebKit, consultar al servidor backend
    if (window.fetch) {
        try {
            const res = await fetch('/api/theme');
            if (res.ok) {
                const data = await res.json();
                if (data.ok && data.theme) {
                    applyThemeVariables(data.theme, false);
                    applied = true;
                }
            }
        } catch (e) {}
    }

    // 3. Fallback a tema por defecto (Warm Terracota)
    if (!applied) {
        applyThemeVariables(DEFAULT_THEMES[0], false);
    }
}

// Iniciar inmediatamente
initThemeEngine();

// Re-asegurar al completar DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThemeEngine);
} else {
    initThemeEngine();
}
