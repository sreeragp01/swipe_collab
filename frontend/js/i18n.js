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

        // Settings Page Translations
        settings_page_title: "⚙️ App Settings & Preferences",
        settings_page_sub: "Manage your security, swipe preferences, visual themes, and app options.",
        
        settings_sec_account: "🔐 Account & Security Settings",
        settings_sec_account_desc: "Update your login credentials and check verification badges.",
        settings_email_status: "Email Verification Status",
        settings_face_status: "Identity Face Verification (OpenCV)",
        settings_manage_email: "Manage Email",
        settings_manage_face: "Manage Face Scan",
        settings_change_password: "Change Password",
        settings_current_password: "Current password",
        settings_new_password: "New password",
        settings_update_password: "Update Password",

        settings_sec_privacy: "👁️ Privacy & Swipe Discovery",
        settings_sec_privacy_desc: "Control how your profile appears in the swipe feed and discovery search.",
        settings_show_profile: "Show Profile in Swipe Feed",
        settings_show_profile_sub: "Allow other freelancers & companies to discover your profile.",
        settings_show_online: "Show Online / Active Badge",
        settings_show_online_sub: "Display a green online indicator when you are active on the app.",

        settings_lang_title: "🌐 Interface Language",
        settings_lang_desc: "Select your preferred application interface language.",
        settings_app_lang: "Application Interface Language",
        settings_app_lang_sub: "Applies to buttons, menus, titles, and system messages instantly.",

        settings_sec_themes: "🎨 Custom App Themes & Sound FX",
        settings_sec_themes_desc: "Personalize your visual experience and toggle audio haptics.",
        settings_swipe_audio: "Swipe Audio & Sound Effects",
        settings_swipe_audio_sub: "Play subtle audio feedback when Swiping Like or Match request.",
        settings_select_theme: "Select Visual Theme",

        sidebar_main_workspace: "Main Workspace",
        sidebar_projects_talent: "Projects & Talent",
        sidebar_account_controls: "Account Controls",
        sidebar_edit_profile: "Edit Profile",
        sidebar_safety: "Safety & Verification",

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

        // Settings Page Translations
        settings_page_title: "⚙️ Configuración y Preferencias",
        settings_page_sub: "Administra tu seguridad, preferencias de deslizamiento y temas visuales.",
        
        settings_sec_account: "🔐 Configuración de Cuenta y Seguridad",
        settings_sec_account_desc: "Actualiza tus credenciales y revisa tus insignias de verificación.",
        settings_email_status: "Estado de Verificación de Correo",
        settings_face_status: "Verificación Facial de Identidad (OpenCV)",
        settings_manage_email: "Gestionar Correo",
        settings_manage_face: "Gestionar Escaneo Facial",
        settings_change_password: "Cambiar Contraseña",
        settings_current_password: "Contraseña actual",
        settings_new_password: "Nueva contraseña",
        settings_update_password: "Actualizar Contraseña",

        settings_sec_privacy: "👁️ Privacidad y Descubrimiento",
        settings_sec_privacy_desc: "Controla cómo aparece tu perfil en el feed de deslizamiento.",
        settings_show_profile: "Mostrar Perfil en el Feed",
        settings_show_profile_sub: "Permite que freelancers y empresas descubran tu perfil.",
        settings_show_online: "Mostrar Insignia En Línea",
        settings_show_online_sub: "Muestra un indicador verde cuando estés activo en la app.",

        settings_lang_title: "🌐 Idioma de la Interfaz",
        settings_lang_desc: "Selecciona tu idioma preferido para la aplicación.",
        settings_app_lang: "Idioma de la Interfaz de la App",
        settings_app_lang_sub: "Se aplica instantáneamente a botones, menús, títulos y avisos.",

        settings_sec_themes: "🎨 Temas Visuales y Efectos de Sonido",
        settings_sec_themes_desc: "Personaliza tu experiencia visual y activa sonidos táctiles.",
        settings_swipe_audio: "Efectos de Sonido de Deslizamiento",
        settings_swipe_audio_sub: "Reproduce sonidos al deslizar 'Me Gusta' o recibir coincidencias.",
        settings_select_theme: "Seleccionar Tema Visual",

        sidebar_main_workspace: "Área Principal",
        sidebar_projects_talent: "Proyectos y Talento",
        sidebar_account_controls: "Controles de Cuenta",
        sidebar_edit_profile: "Editar Perfil",
        sidebar_safety: "Seguridad y Verificación",

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

        // Settings Page Translations
        settings_page_title: "⚙️ Paramètres et Préférences",
        settings_page_sub: "Gérez votre sécurité, vos préférences de swipe et vos thèmes visuels.",
        
        settings_sec_account: "🔐 Paramètres du Compte et Sécurité",
        settings_sec_account_desc: "Mettez à jour vos identifiants et vérifiez vos badges.",
        settings_email_status: "Statut de Vérification de l'E-mail",
        settings_face_status: "Vérification Faciale d'Identité (OpenCV)",
        settings_manage_email: "Gérer l'E-mail",
        settings_manage_face: "Gérer le Scan Facial",
        settings_change_password: "Changer le Mot de Passe",
        settings_current_password: "Mot de passe actuel",
        settings_new_password: "Nouveau mot de passe",
        settings_update_password: "Mettre à jour le Mot de Passe",

        settings_sec_privacy: "👁️ Confidentialité et Découverte",
        settings_sec_privacy_desc: "Contrôlez comment votre profil apparaît dans le flux.",
        settings_show_profile: "Afficher le Profil dans le Flux",
        settings_show_profile_sub: "Permettez aux freelances et entreprises de vous découvrir.",
        settings_show_online: "Afficher le Badge En Ligne",
        settings_show_online_sub: "Affichez un voyant vert lorsque vous êtes actif sur l'application.",

        settings_lang_title: "🌐 Langue de l'Interface",
        settings_lang_desc: "Sélectionnez votre langue d'interface préférée.",
        settings_app_lang: "Langue de l'Application",
        settings_app_lang_sub: "S'applique immédiatement aux boutons, menus et titres.",

        settings_sec_themes: "🎨 Thèmes Visuels et Effets Sonores",
        settings_sec_themes_desc: "Personnalisez votre expérience visuelle et sonore.",
        settings_swipe_audio: "Effets Sonores de Swipe",
        settings_swipe_audio_sub: "Jouer un son lors d'un 'J'aime' ou d'un match.",
        settings_select_theme: "Sélectionner un Thème Visuel",

        sidebar_main_workspace: "Espace Principal",
        sidebar_projects_talent: "Projets & Talents",
        sidebar_account_controls: "Contrôles du Compte",
        sidebar_edit_profile: "Modifier le Profil",
        sidebar_safety: "Sécurité et Vérification",

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

        // Settings Page Translations
        settings_page_title: "⚙️ App-Einstellungen & Präferenzen",
        settings_page_sub: "Verwalte deine Sicherheit, Swipe-Präferenzen und visuellen Themes.",
        
        settings_sec_account: "🔐 Konto & Sicherheitseinstellungen",
        settings_sec_account_desc: "Aktualisiere deine Zugangsdaten und überprüfe Verifizierungsbadges.",
        settings_email_status: "E-Mail-Verifizierungsstatus",
        settings_face_status: "Gesichtsverifizierung (OpenCV)",
        settings_manage_email: "E-Mail Verwalten",
        settings_manage_face: "Gesichtsscan Verwalten",
        settings_change_password: "Passwort Ändern",
        settings_current_password: "Aktuelles Passwort",
        settings_new_password: "Neues Passwort",
        settings_update_password: "Passwort Aktualisieren",

        settings_sec_privacy: "👁️ Datenschutz & Entdeckung",
        settings_sec_privacy_desc: "Steuere, wie dein Profil im Swipe-Feed erscheint.",
        settings_show_profile: "Profil im Swipe-Feed Anzeigen",
        settings_show_profile_sub: "Erlaube anderen Freelancern & Unternehmen, dein Profil zu entdecken.",
        settings_show_online: "Online-Badge Anzeigen",
        settings_show_online_sub: "Zeige einen grünen Online-Indikator, wenn du aktiv bist.",

        settings_lang_title: "🌐 App-Sprache",
        settings_lang_desc: "Wähle deine bevorzugte Benutzeroberflächensprache.",
        settings_app_lang: "Sprache der Benutzeroberfläche",
        settings_app_lang_sub: "Wird sofort auf Buttons, Menüs und Titel angewendet.",

        settings_sec_themes: "🎨 Themes & Soundeffekte",
        settings_sec_themes_desc: "Personalisiere dein visuelles Erlebnis und Audiosignale.",
        settings_swipe_audio: "Swipe-Soundeffekte",
        settings_swipe_audio_sub: "Spiele Soundeffekte beim Wischen oder bei Matches ab.",
        settings_select_theme: "Visuelles Theme Auswählen",

        sidebar_main_workspace: "Hauptarbeitsbereich",
        sidebar_projects_talent: "Projekte & Talente",
        sidebar_account_controls: "Kontoverwaltung",
        sidebar_edit_profile: "Profil Bearbeiten",
        sidebar_safety: "Sicherheit & Verifizierung",

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

        // Settings Page Translations
        settings_page_title: "⚙️ ऐप सेटिंग्स और प्राथमिकताएं",
        settings_page_sub: "अपनी सुरक्षा, स्वाइप प्राथमिकताओं और दृश्य थीम प्रबंधित करें।",
        
        settings_sec_account: "🔐 खाता और सुरक्षा सेटिंग्स",
        settings_sec_account_desc: "अपने लॉगिन क्रेडेंशियल अपडेट करें और सत्यापन बैज जांचें।",
        settings_email_status: "ईमेल सत्यापन स्थिति",
        settings_face_status: "पहचान चेहरा सत्यापन (OpenCV)",
        settings_manage_email: "ईमेल प्रबंधित करें",
        settings_manage_face: "फेस स्कैन प्रबंधित करें",
        settings_change_password: "पासवर्ड बदलें",
        settings_current_password: "वर्तमान पासवर्ड",
        settings_new_password: "नया पासवर्ड",
        settings_update_password: "पासवर्ड अपडेट करें",

        settings_sec_privacy: "👁️ गोपनीयता और खोज",
        settings_sec_privacy_desc: "नियंत्रित करें कि आपकी प्रोफाइल स्वाइप फीड में कैसे दिखाई देती है।",
        settings_show_profile: "स्वाइप फीड में प्रोफाइल दिखाएं",
        settings_show_profile_sub: "अन्य फ्रीलांसरों और कंपनियों को अपनी प्रोफाइल खोजने की अनुमति दें।",
        settings_show_online: "ऑनलाइन / सक्रिय बैज दिखाएं",
        settings_show_online_sub: "जब आप ऐप पर सक्रिय हों तो एक हरा ऑनलाइन संकेतक प्रदर्शित करें।",

        settings_lang_title: "🌐 इंटरफ़ेस भाषा",
        settings_lang_desc: "अपनी पसंदीदा एप्लिकेशन भाषा चुनें।",
        settings_app_lang: "एप्लिकेशन इंटरफ़ेस भाषा",
        settings_app_lang_sub: "बटन, मेनू, शीर्षक और सिस्टम संदेशों पर तुरंत लागू होता है।",

        settings_sec_themes: "🎨 कस्टम ऐप थीम और साउंड इफेक्ट्स",
        settings_sec_themes_desc: "अपने दृश्य अनुभव को कस्टमाइज़ करें और ऑडियो साउंड चालू/बंद करें।",
        settings_swipe_audio: "स्वाइप ऑडियो और ध्वनि प्रभाव",
        settings_swipe_audio_sub: "लाइक या मैच स्वाइप करने पर ध्वनि चलाएं।",
        settings_select_theme: "दृश्य थीम चुनें",

        sidebar_main_workspace: "मुख्य कार्यक्षेत्र",
        sidebar_projects_talent: "प्रोजेक्ट्स और प्रतिभा",
        sidebar_account_controls: "खाता नियंत्रण",
        sidebar_edit_profile: "प्रोफाइल संपादित करें",
        sidebar_safety: "सुरक्षा और सत्यापन",

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

        // Settings Page Translations
        settings_page_title: "⚙️ ആപ്പ് സെറ്റിംഗ്സും മുൻഗണനകളും",
        settings_page_sub: "നിങ്ങളുടെ സുരക്ഷ, സ്വൈപ്പ് മുൻഗണനകൾ, തീമുകൾ എന്നിവ നിയന്ത്രിക്കുക.",
        
        settings_sec_account: "🔐 അക്കൗണ്ട് & സുരക്ഷാ സെറ്റിംഗ്സ്",
        settings_sec_account_desc: "നിങ്ങളുടെ ലോഗിൻ വിവരങ്ങളും വെരിഫിക്കേഷൻ ബാഡ്ജുകളും കാണുക.",
        settings_email_status: "ഇമെയിൽ വെരിഫിക്കേഷൻ അവസ്ഥ",
        settings_face_status: "ഫേസ് വെരിഫിക്കേഷൻ (OpenCV)",
        settings_manage_email: "ഇമെയിൽ മാനേജ് ചെയ്യുക",
        settings_manage_face: "ഫേസ് സ്കാൻ മാനേജ് ചെയ്യുക",
        settings_change_password: "പാസ്‌വേഡ് മാറ്റുക",
        settings_current_password: "നിലവിലെ പാസ്‌വേഡ്",
        settings_new_password: "പുതിയ പാസ്‌വേഡ്",
        settings_update_password: "പാസ്‌വേഡ് അപ്ഡേറ്റ് ചെയ്യുക",

        settings_sec_privacy: "👁️ പ്രൈവസിയും സ്വൈപ്പ് ഡിസ്കവറിയും",
        settings_sec_privacy_desc: "സ്വൈപ്പ് ഫീഡിൽ നിങ്ങളുടെ പ്രൊഫൈൽ എങ്ങനെ കാണിക്കണമെന്ന് തിരഞ്ഞെടുക്കുക.",
        settings_show_profile: "സ്വൈപ്പ് ഫീഡിൽ പ്രൊഫൈൽ കാണിക്കുക",
        settings_show_profile_sub: "മറ്റ് ഫ്രീലാൻസർമാർക്കും കമ്പനികൾക്കും നിങ്ങളുടെ പ്രൊഫൈൽ കാണാൻ അനുവാദം നൽകുക.",
        settings_show_online: "ഓൺലൈൻ ബാഡ്ജ് കാണിക്കുക",
        settings_show_online_sub: "നിങ്ങൾ ആപ്പിൽ സജീവമായിരിക്കുമ്പോൾ പച്ച ഇൻഡിക്കേറ്റർ കാണിക്കുക.",

        settings_lang_title: "🌐 ആപ്പ് ഭാഷ",
        settings_lang_desc: "നിങ്ങൾക്ക് ഇഷ്ടമുള്ള ഭാഷ തിരഞ്ഞെടുക്കുക.",
        settings_app_lang: "ആപ്പ് ഇന്റർഫേസ് ഭാഷ",
        settings_app_lang_sub: "ബട്ടണുകൾ, മെനുകൾ, ടൈറ്റിലുകൾ എന്നിവ ഉടനടി മാറും.",

        settings_sec_themes: "🎨 തീമുകളും സൗണ്ട് ഇഫക്റ്റുകളും",
        settings_sec_themes_desc: "നിങ്ങളുടെ വിഷ്വൽ അനുഭവവും ശബ്ദങ്ങളും തിരഞ്ഞെടുക്കുക.",
        settings_swipe_audio: "സ്വൈപ്പ് സൗണ്ട് ഇഫക്റ്റുകൾ",
        settings_swipe_audio_sub: "ലൈക്ക് അല്ലെങ്കിൽ മാച്ച് ചെയ്യുമ്പോൾ ശബ്ദം പ്ലേ ചെയ്യുക.",
        settings_select_theme: "തീം തിരഞ്ഞെടുക്കുക",

        sidebar_main_workspace: "പ്രധാന വർക്ക്സ്പേസ്",
        sidebar_projects_talent: "പ്രൊജക്റ്റുകളും കഴിവുകളും",
        sidebar_account_controls: "അക്കൗണ്ട് നിയന്ത്രണങ്ങൾ",
        sidebar_edit_profile: "പ്രൊഫൈൽ തിരുത്തുക",
        sidebar_safety: "സുരക്ഷയും വെരിഫിക്കേഷനും",

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
