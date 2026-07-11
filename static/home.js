(function () {
  const homeScriptEl = document.currentScript;
  const fullScriptSrc = homeScriptEl?.dataset.fullScript || '';

  const LANGUAGES = [
    { code: 'en', label: 'English' },
    { code: 'tr', label: 'Turkce' },
    { code: 'de', label: 'Deutsch' },
    { code: 'fr', label: 'Francais' },
    { code: 'es', label: 'Espanol' },
  ];

  const TEXT = {
    en: {
      darkMode: 'Dark Mode',
      navNews: 'News',
      navGuides: 'Guides',
      navBlog: 'Blog',
      navPricing: 'Pricing',
      login: 'Log In',
      homeHeroTitlePrefix: 'Compare cars by the',
      homeHeroTitleAccent: 'numbers that matter',
      homeHeroTitleSuffix: '.',
      homeHeroLead: 'See performance, running costs, ownership data and market insight side by side before you decide.',
      homeHeroCompare: 'Compare Cars',
      homeHeroSell: 'Sell Your Cars',
      footerCorporate: 'Corporate',
      footerExplore: 'Explore',
      footerInfo: 'Information',
      footerFollow: 'Follow Us',
      navHome: 'Home',
      navAbout: 'About Us',
      navContact: 'Contact',
      navSellCar: 'Sell Your Car',
      navMethodology: 'Methodology',
      navTerms: 'Terms',
      navRefund: 'Refund Policy',
      navPrivacy: 'Privacy Policy',
    },
    tr: {
      darkMode: 'Karanlik Mod',
      navNews: 'Haberler',
      navGuides: 'Rehberler',
      navBlog: 'Blog',
      navPricing: 'Fiyatlandirma',
      login: 'Giris Yap',
      homeHeroTitlePrefix: 'Arabalari',
      homeHeroTitleAccent: 'onemli rakamlarla',
      homeHeroTitleSuffix: ' karsilastirin.',
      homeHeroLead: 'Karar vermeden once performansi, kullanim maliyetlerini, sahiplik verilerini ve pazar bilgilerini yan yana inceleyin.',
      homeHeroCompare: 'Arabalari Karsilastir',
      homeHeroSell: 'Arabanizi Satin',
      footerCorporate: 'Kurumsal',
      footerExplore: 'Kesfet',
      footerInfo: 'Bilgi',
      footerFollow: 'Bizi Takip Edin',
      navHome: 'Ana Sayfa',
      navAbout: 'Hakkimizda',
      navContact: 'Iletisim',
      navSellCar: 'Arabanizi Satin',
      navMethodology: 'Metodoloji',
      navTerms: 'Kosullar',
      navRefund: 'Iade Politikasi',
      navPrivacy: 'Gizlilik Politikasi',
    },
    de: {
      darkMode: 'Dunkelmodus',
      navNews: 'News',
      navGuides: 'Guides',
      navBlog: 'Blog',
      navPricing: 'Preise',
      login: 'Einloggen',
      homeHeroTitlePrefix: 'Autos nach den',
      homeHeroTitleAccent: 'wichtigen Zahlen',
      homeHeroTitleSuffix: ' vergleichen.',
      homeHeroLead: 'Vergleiche Leistung, Betriebskosten, Besitzdaten und Marktsignale nebeneinander, bevor du entscheidest.',
      homeHeroCompare: 'Autos vergleichen',
      homeHeroSell: 'Auto verkaufen',
      footerCorporate: 'Unternehmen',
      footerExplore: 'Entdecken',
      footerInfo: 'Information',
      footerFollow: 'Folge uns',
      navHome: 'Startseite',
      navAbout: 'Uber uns',
      navContact: 'Kontakt',
      navSellCar: 'Auto verkaufen',
      navMethodology: 'Methodik',
      navTerms: 'Bedingungen',
      navRefund: 'Rueckerstattung',
      navPrivacy: 'Datenschutz',
    },
    fr: {
      darkMode: 'Mode sombre',
      navNews: 'Actualites',
      navGuides: 'Guides',
      navBlog: 'Blog',
      navPricing: 'Tarifs',
      login: 'Connexion',
      homeHeroTitlePrefix: 'Comparez les voitures avec les',
      homeHeroTitleAccent: 'chiffres qui comptent',
      homeHeroTitleSuffix: '.',
      homeHeroLead: 'Comparez performances, couts d utilisation, donnees de possession et signaux du marche avant de decider.',
      homeHeroCompare: 'Comparer les voitures',
      homeHeroSell: 'Vendre votre voiture',
      footerCorporate: 'Entreprise',
      footerExplore: 'Explorer',
      footerInfo: 'Information',
      footerFollow: 'Suivez-nous',
      navHome: 'Accueil',
      navAbout: 'A propos',
      navContact: 'Contact',
      navSellCar: 'Vendre votre voiture',
      navMethodology: 'Methodologie',
      navTerms: 'Conditions',
      navRefund: 'Politique de remboursement',
      navPrivacy: 'Politique de confidentialite',
    },
    es: {
      darkMode: 'Modo oscuro',
      navNews: 'Noticias',
      navGuides: 'Guias',
      navBlog: 'Blog',
      navPricing: 'Precios',
      login: 'Iniciar sesion',
      homeHeroTitlePrefix: 'Compara autos por los',
      homeHeroTitleAccent: 'numeros que importan',
      homeHeroTitleSuffix: '.',
      homeHeroLead: 'Compara rendimiento, costos de uso, datos de propiedad e informacion de mercado antes de decidir.',
      homeHeroCompare: 'Comparar autos',
      homeHeroSell: 'Vende tu auto',
      footerCorporate: 'Empresa',
      footerExplore: 'Explorar',
      footerInfo: 'Informacion',
      footerFollow: 'Siguenos',
      navHome: 'Inicio',
      navAbout: 'Acerca de',
      navContact: 'Contacto',
      navSellCar: 'Vende tu auto',
      navMethodology: 'Metodologia',
      navTerms: 'Terminos',
      navRefund: 'Politica de reembolso',
      navPrivacy: 'Politica de privacidad',
    },
  };

  const getLang = (code) => LANGUAGES.find((lang) => lang.code === code) || LANGUAGES[0];
  let currentLang = getLang((localStorage.getItem('appLang') || 'en').toLowerCase()).code;

  const applyText = () => {
    const pack = TEXT[currentLang] || TEXT.en;
    document.documentElement.lang = currentLang;
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const value = pack[el.dataset.i18n];
      if (value) el.textContent = value;
    });
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn && pack.login) loginBtn.textContent = pack.login;
  };

  const initTheme = () => {
    const themeToggle = document.getElementById('themeToggle');
    const mobileThemeToggle = document.getElementById('mobileThemeToggle');
    const storedTheme = localStorage.getItem('theme');
    const defaultDark = ['127.0.0.1', 'localhost'].includes(window.location.hostname)
      ? true
      : (storedTheme ? storedTheme === 'dark' : true);
    const syncTheme = (next) => {
      document.body.classList.toggle('dark', next);
      if (themeToggle) themeToggle.checked = next;
      if (mobileThemeToggle) {
        mobileThemeToggle.classList.toggle('is-dark', next);
        mobileThemeToggle.setAttribute('aria-pressed', String(next));
      }
      localStorage.setItem('theme', next ? 'dark' : 'light');
    };
    syncTheme(defaultDark);
    if (themeToggle) themeToggle.addEventListener('change', (event) => syncTheme(event.target.checked));
    if (mobileThemeToggle) mobileThemeToggle.addEventListener('click', () => syncTheme(!document.body.classList.contains('dark')));
  };

  const initLanguage = () => {
    const host = document.getElementById('topLangHost');
    if (!host) return;
    const select = host.querySelector('select') || document.createElement('select');
    select.className = 'topbar-lang-select';
    select.setAttribute('aria-label', 'Language selector');
    if (!select.options.length) {
      LANGUAGES.forEach((lang) => {
        const option = document.createElement('option');
        option.value = lang.code;
        option.textContent = lang.label;
        select.appendChild(option);
      });
    }
    select.value = currentLang;
    select.addEventListener('change', () => {
      currentLang = getLang(select.value).code;
      localStorage.setItem('appLang', currentLang);
      applyText();
    });
    if (!select.parentElement) host.replaceChildren(select);
  };

  const initHeroHover = () => {
    const img = document.getElementById('homeHeroImage');
    const compareLink = document.getElementById('homeCompareLink');
    const sellLink = document.getElementById('homeSellLink');
    if (!img) return;
    const defaultSrc = img.getAttribute('src') || img.currentSrc || img.src;
    const defaultAlt = img.alt;
    const preload = (src) => {
      if (!src) return;
      const preview = new Image();
      preview.decoding = 'async';
      preview.src = src;
    };
    const setImage = (src, alt) => {
      if (!src || img.getAttribute('src') === src) return;
      img.classList.add('is-switching');
      window.setTimeout(() => {
        img.setAttribute('src', src);
        img.classList.remove('is-switching');
      }, 60);
      img.alt = alt || defaultAlt;
    };
    const restore = () => setImage(defaultSrc, defaultAlt);
    const mobileMedia = window.matchMedia('(max-width: 760px)');
    const mobileSlides = [
      [img.dataset.mobileHoverSrc, img.dataset.hoverAlt],
      [img.dataset.mobileSellHoverSrc, img.dataset.sellHoverAlt]
    ].filter(([src]) => Boolean(src));
    let mobileSlideIndex = 0;
    let mobileRotationTimer = null;

    const stopMobileRotation = () => {
      if (mobileRotationTimer !== null) {
        window.clearInterval(mobileRotationTimer);
        mobileRotationTimer = null;
      }
    };
    const startMobileRotation = () => {
      stopMobileRotation();
      if (!mobileMedia.matches || mobileSlides.length < 2) return;
      mobileSlides.forEach(([src]) => preload(src));
      mobileSlideIndex = 0;
      setImage(...mobileSlides[mobileSlideIndex]);
      mobileRotationTimer = window.setInterval(() => {
        mobileSlideIndex = (mobileSlideIndex + 1) % mobileSlides.length;
        setImage(...mobileSlides[mobileSlideIndex]);
      }, 3500);
    };

    startMobileRotation();
    mobileMedia.addEventListener('change', () => {
      if (mobileMedia.matches) {
        startMobileRotation();
      } else {
        stopMobileRotation();
        restore();
      }
    });

    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    [img.dataset.hoverSrc, img.dataset.sellHoverSrc].forEach(preload);
    if (compareLink && img.dataset.hoverSrc) {
      compareLink.addEventListener('mouseenter', () => setImage(img.dataset.hoverSrc, img.dataset.hoverAlt));
      compareLink.addEventListener('mouseleave', restore);
      compareLink.addEventListener('focus', () => setImage(img.dataset.hoverSrc, img.dataset.hoverAlt));
      compareLink.addEventListener('blur', restore);
    }
    if (sellLink && img.dataset.sellHoverSrc) {
      sellLink.addEventListener('mouseenter', () => setImage(img.dataset.sellHoverSrc, img.dataset.sellHoverAlt));
      sellLink.addEventListener('mouseleave', restore);
      sellLink.addEventListener('focus', () => setImage(img.dataset.sellHoverSrc, img.dataset.sellHoverAlt));
      sellLink.addEventListener('blur', restore);
    }
  };

  let fullScriptPromise = null;
  const loadFullScript = () => {
    if (fullScriptPromise) return fullScriptPromise;
    const src = fullScriptSrc;
    if (!src) return Promise.resolve();
    fullScriptPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.async = true;
      script.onload = resolve;
      script.onerror = reject;
      document.body.appendChild(script);
    });
    return fullScriptPromise;
  };

  const initLoginLazyLoad = () => {
    const loginBtn = document.getElementById('loginBtn');
    if (!loginBtn) return;
    loginBtn.addEventListener('click', (event) => {
      event.preventDefault();
      window.__carQuantixOpenLoginAfterLoad = true;
      loginBtn.disabled = true;
      loadFullScript().finally(() => {
        loginBtn.disabled = false;
      });
    });
  };

  const initDeferredAdsense = () => {
    const account = document.querySelector('meta[name="google-adsense-account"]')?.content;
    if (!account) return;
    let didLoad = false;
    const loadAdsense = () => {
      if (didLoad) return;
      didLoad = true;
      if (document.querySelector('script[src*="pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]')) return;
      const script = document.createElement('script');
      script.async = true;
      script.crossOrigin = 'anonymous';
      script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(account)}`;
      document.head.appendChild(script);
    };
    const scheduleAdsense = () => {
      window.setTimeout(loadAdsense, 12000);
      ['pointerdown', 'keydown', 'scroll'].forEach((eventName) => {
        window.addEventListener(eventName, loadAdsense, { once: true, passive: true });
      });
    };
    if (document.readyState === 'complete') {
      scheduleAdsense();
    } else {
      window.addEventListener('load', scheduleAdsense, { once: true });
    }
  };

  const initWheelScrollFallback = () => {
    window.addEventListener('wheel', (event) => {
      const target = event.target;
      if (target && target.closest && target.closest('input, textarea, select, [role="dialog"], .modal, .vehicle-picker-modal')) {
        return;
      }
      const delta = Math.abs(event.deltaY) >= Math.abs(event.deltaX) ? event.deltaY : event.deltaX;
      if (!delta) return;
      const scroller = document.scrollingElement || document.documentElement;
      const multiplier = event.deltaMode === 1 ? 18 : event.deltaMode === 2 ? window.innerHeight : 1;
      event.preventDefault();
      scroller.scrollTop += delta * multiplier;
    }, { passive: false });
  };

  initTheme();
  initLanguage();
  applyText();
  initHeroHover();
  initLoginLazyLoad();
  initDeferredAdsense();
  initWheelScrollFallback();
})();
