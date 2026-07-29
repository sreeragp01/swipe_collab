const SC_LANGUAGES = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
    { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
    { code: 'ml', name: 'മലയാളം', flag: '🇮🇳' }
];

const SC_DICTIONARIES = {
    en: {
        nav_home: "Home",
        nav_dashboard: "Dashboard",
        nav_projects: "Projects",
        nav_swipe: "Swipe",
        nav_matches: "Matches",
        nav_chat: "Chat",
        nav_profile: "Profile",
        nav_settings: "Settings",
        nav_login: "Log in",
        nav_signup: "Sign up free",
        nav_logout: "Log out",
        nav_moderation: "Moderation",

        hero_title: "Swipe to Collaborate & Build",
        hero_subtitle: "Connect top freelancers with forward-thinking companies using AI skill-matching.",
        hero_btn_start: "Start Swiping",
        hero_btn_login: "Log In to Account",
        
        dash_welcome: "Welcome Back",
        dash_matches: "Total Matches",
        dash_active_projects: "Active Projects",
        dash_unread_chats: "Unread Chats",
        dash_quick_actions: "Quick Actions",
        dash_recent_activity: "Recent Activity",

        swipe_match_title: "Skill Match Found!",
        swipe_like: "Like",
        swipe_pass: "Pass",
        swipe_view_profile: "View Profile",
        swipe_no_candidates: "No more profiles available right now. Check back soon!",

        proj_post_btn: "+ Post Project",
        proj_browse: "Browse Projects",
        proj_budget: "Budget",
        proj_duration: "Duration",
        proj_apply: "Apply Now",
        proj_skills: "Required Skills",

        chat_placeholder: "Type a message...",
        chat_send: "Send",
        chat_translate: "🌐 Translate",
        chat_show_original: "Show Original",
        chat_translated_badge: "Translated",

        settings_title: "Settings & Preferences",
        settings_language: "Interface Language",
        settings_save: "Save Preferences",

        common_loading: "Loading...",
        common_error: "An error occurred",
        common_success: "Saved successfully"
    },
    es: {
        nav_home: "Inicio",
        nav_dashboard: "Panel",
        nav_projects: "Proyectos",
        nav_swipe: "Deslizar",
        nav_matches: "Coincidencias",
        nav_chat: "Chat",
        nav_profile: "Perfil",
        nav_settings: "Ajustes",
        nav_login: "Iniciar sesión",
        nav_signup: "Regístrate gratis",
        nav_logout: "Cerrar sesión",
        nav_moderation: "Moderación",

        hero_title: "Desliza para Colaborar y Crear",
        hero_subtitle: "Conecta a los mejores freelancers con empresas mediante emparejamiento de habilidades.",
        hero_btn_start: "Empezar a Deslizar",
        hero_btn_login: "Iniciar Sesión",

        dash_welcome: "Bienvenido de nuevo",
        dash_matches: "Coincidencias Totales",
        dash_active_projects: "Proyectos Activos",
        dash_unread_chats: "Chats no Leídos",
        dash_quick_actions: "Acciones Rápidas",
        dash_recent_activity: "Actividad Reciente",

        swipe_match_title: "¡Coincidencia Encontrada!",
        swipe_like: "Me gusta",
        swipe_pass: "Pasar",
        swipe_view_profile: "Ver Perfil",
        swipe_no_candidates: "No hay más perfiles disponibles en este momento.",

        proj_post_btn: "+ Publicar Proyecto",
        proj_browse: "Buscar Proyectos",
        proj_budget: "Presupuesto",
        proj_duration: "Duración",
        proj_apply: "Postularse Ahora",
        proj_skills: "Habilidades Requeridas",

        chat_placeholder: "Escribe un mensaje...",
        chat_send: "Enviar",
        chat_translate: "🌐 Traducir",
        chat_show_original: "Ver Original",
        chat_translated_badge: "Traducido",

        settings_title: "Ajustes y Preferencias",
        settings_language: "Idioma de Interfaz",
        settings_save: "Guardar Preferencias",

        common_loading: "Cargando...",
        common_error: "Ocurrió un error",
        common_success: "Guardado correctamente"
    },
    fr: {
        nav_home: "Accueil",
        nav_dashboard: "Tableau de bord",
        nav_projects: "Projets",
        nav_swipe: "Swipe",
        nav_matches: "Correspondances",
        nav_chat: "Discussion",
        nav_profile: "Profil",
        nav_settings: "Paramètres",
        nav_login: "Connexion",
        nav_signup: "Inscription gratuite",
        nav_logout: "Déconnexion",
        nav_moderation: "Modération",

        hero_title: "Glissez pour Collaborer et Créer",
        hero_subtitle: "Connectez les meilleurs freelances et entreprises grâce aux compétences.",
        hero_btn_start: "Commencer à Swiper",
        hero_btn_login: "Se Connecter",

        dash_welcome: "Bon retour",
        dash_matches: "Correspondances Totales",
        dash_active_projects: "Projets Actifs",
        dash_unread_chats: "Messages non lus",
        dash_quick_actions: "Actions Rapides",
        dash_recent_activity: "Activité Récente",

        swipe_match_title: "Correspondance Trouvée !",
        swipe_like: "Aimer",
        swipe_pass: "Passer",
        swipe_view_profile: "Voir le Profil",
        swipe_no_candidates: "Plus de profils disponibles pour le moment.",

        proj_post_btn: "+ Publier un Projet",
        proj_browse: "Parcourir les Projets",
        proj_budget: "Budget",
        proj_duration: "Durée",
        proj_apply: "Postuler Maintenant",
        proj_skills: "Compétences Requises",

        chat_placeholder: "Écrivez un message...",
        chat_send: "Envoyer",
        chat_translate: "🌐 Traduire",
        chat_show_original: "Afficher l'Original",
        chat_translated_badge: "Traduit",

        settings_title: "Paramètres et Préférences",
        settings_language: "Langue de l'Interface",
        settings_save: "Enregistrer les Préférences",

        common_loading: "Chargement...",
        common_error: "Une erreur est survenue",
        common_success: "Enregistré avec succès"
    },
    de: {
        nav_home: "Startseite",
        nav_dashboard: "Dashboard",
        nav_projects: "Projekte",
        nav_swipe: "Swipen",
        nav_matches: "Matches",
        nav_chat: "Chat",
        nav_profile: "Profil",
        nav_settings: "Einstellungen",
        nav_login: "Anmelden",
        nav_signup: "Kostenlos registrieren",
        nav_logout: "Abmelden",
        nav_moderation: "Moderation",

        hero_title: "Wischen zur Zusammenarbeit",
        hero_subtitle: "Verbinde Top-Freelancer und Unternehmen mit KI-Skill-Matching.",
        hero_btn_start: "Jetzt Swipen",
        hero_btn_login: "Anmelden",

        dash_welcome: "Willkommen zurück",
        dash_matches: "Gesamte Matches",
        dash_active_projects: "Aktive Projekte",
        dash_unread_chats: "Ungelesene Chats",
        dash_quick_actions: "Schnellaktionen",
        dash_recent_activity: "Letzte Aktivitäten",

        swipe_match_title: "Match Gefunden!",
        swipe_like: "Gefällt mir",
        swipe_pass: "Überspringen",
        swipe_view_profile: "Profil Ansehen",
        swipe_no_candidates: "Zurzeit keine weiteren Profile verfügbar.",

        proj_post_btn: "+ Projekt Erstellen",
        proj_browse: "Projekte Durchsuchen",
        proj_budget: "Budget",
        proj_duration: "Dauer",
        proj_apply: "Jetzt Bewerben",
        proj_skills: "Erforderliche Skills",

        chat_placeholder: "Nachricht schreiben...",
        chat_send: "Senden",
        chat_translate: "🌐 Übersetzen",
        chat_show_original: "Original Anzeigen",
        chat_translated_badge: "Übersetzt",

        settings_title: "Einstellungen",
        settings_language: "Sprache",
        settings_save: "Speichern",

        common_loading: "Laden...",
        common_error: "Ein Fehler ist aufgetreten",
        common_success: "Erfolgreich gespeichert"
    },
    hi: {
        nav_home: "होम",
        nav_dashboard: "डैशबोर्ड",
        nav_projects: "प्रोजेक्ट्स",
        nav_swipe: "स्वाइप करें",
        nav_matches: "मैचेस",
        nav_chat: "चैट",
        nav_profile: "प्रोफाइल",
        nav_settings: "सेटिंग्स",
        nav_login: "लॉग इन",
        nav_signup: "फ्री साइन अप",
        nav_logout: "लॉग आउट",
        nav_moderation: "मॉडरेशन",

        hero_title: "सहयोग और निर्माण के लिए स्वाइप करें",
        hero_subtitle: "स्किल मैचिंग के ज़रिए फ्रीलांसरों और कंपनियों को जोड़ें।",
        hero_btn_start: "स्वाइप शुरू करें",
        hero_btn_login: "लॉग इन करें",

        dash_welcome: "वापसी पर स्वागत है",
        dash_matches: "कुल मैचेस",
        dash_active_projects: "सक्रिय प्रोजेक्ट्स",
        dash_unread_chats: "अपठित चैट",
        dash_quick_actions: "त्वरित कार्रवाई",
        dash_recent_activity: "हाल की गतिविधि",

        swipe_match_title: "स्किल मैच मिला!",
        swipe_like: "पसंद",
        swipe_pass: "पास",
        swipe_view_profile: "प्रोफाइल देखें",
        swipe_no_candidates: "अभी और प्रोफाइल उपलब्ध नहीं हैं।",

        proj_post_btn: "+ नया प्रोजेक्ट बनाएं",
        proj_browse: "प्रोजेक्ट्स खोजें",
        proj_budget: "बजट",
        proj_duration: "अवधि",
        proj_apply: "अभी आवेदन करें",
        proj_skills: "आवश्यक कौशल",

        chat_placeholder: "संदेश लिखें...",
        chat_send: "भेजें",
        chat_translate: "🌐 अनुवाद करें",
        chat_show_original: "मूल पाठ देखें",
        chat_translated_badge: "अनुदित",

        settings_title: "सेटिंग्स और प्राथमिकताएं",
        settings_language: "इंटरफ़ेस भाषा",
        settings_save: "सहेजें",

        common_loading: "लोड हो रहा है...",
        common_error: "एक त्रुटि हुई",
        common_success: "सफलतापूर्वक सहेजा गया"
    },
    ml: {
        nav_home: "ഹോം",
        nav_dashboard: "ഡാഷ്‌ബോർഡ്",
        nav_projects: "പ്രൊജക്റ്റുകൾ",
        nav_swipe: "സ്വൈപ്പ്",
        nav_matches: "മാച്ചുകൾ",
        nav_chat: "ചാറ്റ്",
        nav_profile: "പ്രൊഫൈൽ",
        nav_settings: "സെറ്റിംഗ്സ്",
        nav_login: "ലോഗിൻ",
        nav_signup: "സൗജന്യമായി സൈൻ അപ്പ് ചെയ്യൂ",
        nav_logout: "ലോഗ് ഔട്ട്",
        nav_moderation: "മോഡറേഷൻ",

        hero_title: "സഹകരിക്കാനും നിർമ്മിക്കാനും സ്വൈപ്പ് ചെയ്യൂ",
        hero_subtitle: "സ്കിൽ മാച്ചിംഗ് വഴി ഫ്രീലാൻസർമാരെയും കമ്പനികളെയും ബന്ധിപ്പിക്കുന്നു.",
        hero_btn_start: "സ്വൈപ്പ് ചെയ്യൂ",
        hero_btn_login: "ലോഗിൻ ചെയ്യൂ",

        dash_welcome: "വീണ്ടും സ്വാഗതം",
        dash_matches: "ആകെ മാച്ചുകൾ",
        dash_active_projects: "നിലവിലെ പ്രൊജക്റ്റുകൾ",
        dash_unread_chats: "വായിക്കാത്ത ചാറ്റുകൾ",
        dash_quick_actions: "ക്വിക്ക് ആക്ഷനുകൾ",
        dash_recent_activity: "സമീപകാല പ്രവർത്തനങ്ങൾ",

        swipe_match_title: "സ്കിൽ മാച്ച് കണ്ടെത്തി!",
        swipe_like: "ലൈക്ക്",
        swipe_pass: "പാസ്",
        swipe_view_profile: "പ്രൊഫൈൽ കാണുക",
        swipe_no_candidates: "ഇപ്പോൾ കൂടുതൽ പ്രൊഫൈലുകൾ ലഭ്യമല്ല.",

        proj_post_btn: "+ പ്രൊജക്റ്റ് സൃഷ്ടിക്കുക",
        proj_browse: "പ്രൊജക്റ്റുകൾ കാണുക",
        proj_budget: "ബഡ്ജറ്റ്",
        proj_duration: "കാലാവധി",
        proj_apply: "അപേക്ഷിക്കൂ",
        proj_skills: "ആവശ്യമായ കഴിവുകൾ",

        chat_placeholder: "സന്ദേശം ടൈപ്പ് ചെയ്യൂ...",
        chat_send: "അയക്കുക",
        chat_translate: "🌐 തർജ്ജമ ചെയ്യൂ",
        chat_show_original: "യഥാർത്ഥ രൂപം",
        chat_translated_badge: "തർജ്ജമ ചെയ്തത്",

        settings_title: "സെറ്റിംഗ്സ്",
        settings_language: "ഭാഷ",
        settings_save: "സേവ് ചെയ്യുക",

        common_loading: "ലോഡ് ചെയ്യുന്നു...",
        common_error: "ഒരു പിശക് സംഭവിച്ചു",
        common_success: "സേവ് ചെയ്തു"
    }
};

let currentLanguage = localStorage.getItem('sc_lang') || 'en';

function getCurrentLanguage() {
    return currentLanguage;
}

function setLanguage(langCode) {
    if (!SC_DICTIONARIES[langCode]) langCode = 'en';
    currentLanguage = langCode;
    localStorage.setItem('sc_lang', langCode);
    document.documentElement.lang = langCode;
    
    translatePage();
    updateLanguageSelectorUI();

    // Dispatch event so reactive UI components can update if needed
    window.dispatchEvent(new CustomEvent('sc_language_changed', { detail: { language: langCode } }));
}

function t(key, defaultValue = '') {
    const dict = SC_DICTIONARIES[currentLanguage] || SC_DICTIONARIES.en;
    return dict[key] || SC_DICTIONARIES.en[key] || defaultValue || key;
}

function translatePage() {
    // Update innerText / textContent for elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translated = t(key);
        if (translated) {
            el.textContent = translated;
        }
    });

    // Update placeholders for inputs/textareas with data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        const translated = t(key);
        if (translated) {
            el.placeholder = translated;
        }
    });

    // Update titles for elements with data-i18n-title
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        const translated = t(key);
        if (translated) {
            el.title = translated;
        }
    });
}

// Machine Learning Translation API Integration for dynamic text
async function translateDynamicText(text, targetLang = null) {
    if (!text || !text.trim()) return text;
    const target = targetLang || currentLanguage;

    try {
        const res = await fetch('/api/v1/translate/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, target_lang: target, source_lang: 'auto' })
        });
        if (res.ok) {
            const data = await res.json();
            return data.translated || text;
        }
    } catch (err) {
        console.error('Translation error:', err);
    }
    return text;
}

function renderLanguageSwitcher() {
    const containers = document.querySelectorAll('.sc-lang-switcher-container');
    if (!containers || containers.length === 0) return;

    const activeLangObj = SC_LANGUAGES.find(l => l.code === currentLanguage) || SC_LANGUAGES[0];

    const html = `
        <div class="sc-lang-dropdown">
            <button class="sc-lang-btn" type="button" aria-label="Select Language">
                <span class="sc-lang-flag">${activeLangObj.flag}</span>
                <span class="sc-lang-name">${activeLangObj.code.toUpperCase()}</span>
                <span class="sc-lang-arrow">▾</span>
            </button>
            <div class="sc-lang-menu">
                ${SC_LANGUAGES.map(lang => `
                    <button type="button" class="sc-lang-option ${lang.code === currentLanguage ? 'active' : ''}" data-lang="${lang.code}">
                        <span class="sc-lang-flag">${lang.flag}</span>
                        <span>${lang.name}</span>
                    </button>
                `).join('')}
            </div>
        </div>
    `;

    containers.forEach(c => {
        c.innerHTML = html;
        const btn = c.querySelector('.sc-lang-btn');
        const menu = c.querySelector('.sc-lang-menu');

        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('show');
        });

        c.querySelectorAll('.sc-lang-option').forEach(opt => {
            opt.addEventListener('click', (e) => {
                const lang = opt.getAttribute('data-lang');
                setLanguage(lang);
                menu.classList.remove('show');
            });
        });
    });

    document.addEventListener('click', () => {
        document.querySelectorAll('.sc-lang-menu').forEach(m => m.classList.remove('show'));
    });
}

function updateLanguageSelectorUI() {
    const activeLangObj = SC_LANGUAGES.find(l => l.code === currentLanguage) || SC_LANGUAGES[0];
    document.querySelectorAll('.sc-lang-btn').forEach(btn => {
        const flagEl = btn.querySelector('.sc-lang-flag');
        const nameEl = btn.querySelector('.sc-lang-name');
        if (flagEl) flagEl.textContent = activeLangObj.flag;
        if (nameEl) nameEl.textContent = activeLangObj.code.toUpperCase();
    });

    document.querySelectorAll('.sc-lang-option').forEach(opt => {
        if (opt.getAttribute('data-lang') === currentLanguage) {
            opt.classList.add('active');
        } else {
            opt.classList.remove('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setLanguage(currentLanguage);
    renderLanguageSwitcher();
});
