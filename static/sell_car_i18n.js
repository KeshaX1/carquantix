(() => {
  const lang = (localStorage.getItem('appLang') || 'en').toLowerCase();
  if (lang === 'en') return;

  const packs = {
    tr: {
      'CarQuantix Marketplace': 'CarQuantix Pazaryeri',
      'Marketplace clarity for every car decision.': 'Her araç kararı için şeffaf bir pazaryeri.',
      'Compare public offers by price, mileage and location, then create a structured listing that gives buyers the details they need.': 'Herkese açık ilanları fiyat, kilometre ve konuma göre karşılaştırın; ardından alıcıların ihtiyaç duyduğu bilgileri içeren düzenli bir ilan oluşturun.',
      'active offers': 'aktif ilan', 'listing fee': 'ilan ücreti', 'Direct': 'Doğrudan', 'seller contact': 'satıcı iletişimi',
      'Search the market': 'Pazarda ara', 'Search listings': 'İlanlarda ara', 'Sell Your Car': 'Aracınızı Satın',
      'Structured listings. Clear buyer signals.': 'Düzenli ilanlar. Açık alıcı bilgileri.', 'Every offer is organized for faster comparison.': 'Her teklif hızlı karşılaştırma için düzenlenir.',
      'Shop by need': 'İhtiyaca göre ara', 'Family SUVs': 'Aile SUV’ları', 'Daily commuters': 'Günlük araçlar', 'Performance cars': 'Performans araçları', 'Low mileage': 'Düşük kilometre', 'Budget picks': 'Bütçe dostu', 'Newly listed': 'Yeni eklenenler',
      'Popular brands': 'Popüler markalar', 'Reduced Car Offers': 'İndirimli Araç İlanları',
      'Discover public car listings with clear prices, mileage, location and seller contact details.': 'Açık fiyat, kilometre, konum ve satıcı bilgileri içeren araç ilanlarını keşfedin.',
      'All Offers': 'Tüm İlanlar', 'My Listings': 'İlanlarım',
      'No public listings yet. The first submitted car will appear here as a marketplace card.': 'Henüz herkese açık ilan yok. Gönderilen ilk araç burada ilan kartı olarak görünecek.',
      'Corporate': 'Kurumsal', 'Home': 'Ana Sayfa', 'Pricing': 'Fiyatlandırma', 'Explore': 'Keşfet', 'News': 'Haberler', 'Guides': 'Rehberler', 'Methodology': 'Metodoloji', 'Information': 'Bilgi', 'About Us': 'Hakkımızda', 'Contact': 'İletişim', 'Terms': 'Koşullar', 'Refund Policy': 'İade Politikası', 'Privacy Policy': 'Gizlilik Politikası', 'Follow Us': 'Bizi Takip Edin',
      placeholders: ['Marka, model veya anahtar kelime', 'Şehir veya bölge', 'En yüksek bütçe'],
    },
    de: {
      'CarQuantix Marketplace': 'CarQuantix Marktplatz', 'Marketplace clarity for every car decision.': 'Klare Marktdaten für jede Autoentscheidung.',
      'Compare public offers by price, mileage and location, then create a structured listing that gives buyers the details they need.': 'Vergleichen Sie Angebote nach Preis, Kilometerstand und Standort und erstellen Sie ein übersichtliches Inserat.',
      'active offers': 'aktive Angebote', 'listing fee': 'Inseratsgebühr', 'Direct': 'Direkt', 'seller contact': 'Verkäuferkontakt', 'Search the market': 'Markt durchsuchen', 'Search listings': 'Inserate suchen', 'Sell Your Car': 'Auto verkaufen',
      'Structured listings. Clear buyer signals.': 'Klare Inserate. Verständliche Kaufsignale.', 'Every offer is organized for faster comparison.': 'Jedes Angebot ist für einen schnellen Vergleich geordnet.',
      'Shop by need': 'Nach Bedarf suchen', 'Family SUVs': 'Familien-SUVs', 'Daily commuters': 'Alltagsautos', 'Performance cars': 'Sportwagen', 'Low mileage': 'Wenig Kilometer', 'Budget picks': 'Preiswerte Auswahl', 'Newly listed': 'Neu eingestellt', 'Popular brands': 'Beliebte Marken',
      'Reduced Car Offers': 'Reduzierte Fahrzeugangebote', 'Discover public car listings with clear prices, mileage, location and seller contact details.': 'Entdecken Sie Inserate mit klaren Preisen, Kilometerstand, Standort und Kontaktdaten.', 'All Offers': 'Alle Angebote', 'My Listings': 'Meine Inserate', 'No public listings yet. The first submitted car will appear here as a marketplace card.': 'Noch keine öffentlichen Inserate. Das erste eingestellte Fahrzeug erscheint hier.',
      'Corporate': 'Unternehmen', 'Home': 'Startseite', 'Pricing': 'Preise', 'Explore': 'Entdecken', 'News': 'Neuigkeiten', 'Guides': 'Ratgeber', 'Methodology': 'Methodik', 'Information': 'Information', 'About Us': 'Über uns', 'Contact': 'Kontakt', 'Terms': 'Bedingungen', 'Refund Policy': 'Rückerstattung', 'Privacy Policy': 'Datenschutz', 'Follow Us': 'Folgen Sie uns',
      placeholders: ['Marke, Modell oder Stichwort', 'Stadt oder Region', 'Maximales Budget'],
    },
    fr: {
      'CarQuantix Marketplace': 'Marché CarQuantix', 'Marketplace clarity for every car decision.': 'Un marché clair pour chaque décision automobile.',
      'Compare public offers by price, mileage and location, then create a structured listing that gives buyers the details they need.': 'Comparez les offres par prix, kilométrage et lieu, puis créez une annonce structurée.',
      'active offers': 'offres actives', 'listing fee': 'frais d’annonce', 'Direct': 'Direct', 'seller contact': 'contact vendeur', 'Search the market': 'Rechercher sur le marché', 'Search listings': 'Rechercher', 'Sell Your Car': 'Vendre votre voiture',
      'Structured listings. Clear buyer signals.': 'Annonces structurées. Informations claires.', 'Every offer is organized for faster comparison.': 'Chaque offre est organisée pour une comparaison rapide.',
      'Shop by need': 'Rechercher par besoin', 'Family SUVs': 'SUV familiaux', 'Daily commuters': 'Trajets quotidiens', 'Performance cars': 'Voitures sportives', 'Low mileage': 'Faible kilométrage', 'Budget picks': 'Petits budgets', 'Newly listed': 'Nouvelles annonces', 'Popular brands': 'Marques populaires',
      'Reduced Car Offers': 'Offres automobiles réduites', 'Discover public car listings with clear prices, mileage, location and seller contact details.': 'Découvrez des annonces avec prix, kilométrage, lieu et coordonnées du vendeur.', 'All Offers': 'Toutes les offres', 'My Listings': 'Mes annonces', 'No public listings yet. The first submitted car will appear here as a marketplace card.': 'Aucune annonce publique pour le moment. La première voiture apparaîtra ici.',
      'Corporate': 'Entreprise', 'Home': 'Accueil', 'Pricing': 'Tarifs', 'Explore': 'Explorer', 'News': 'Actualités', 'Guides': 'Guides', 'Methodology': 'Méthodologie', 'Information': 'Informations', 'About Us': 'À propos', 'Contact': 'Contact', 'Terms': 'Conditions', 'Refund Policy': 'Remboursement', 'Privacy Policy': 'Confidentialité', 'Follow Us': 'Suivez-nous',
      placeholders: ['Marque, modèle ou mot-clé', 'Ville ou région', 'Budget maximal'],
    },
    es: {
      'CarQuantix Marketplace': 'Mercado CarQuantix', 'Marketplace clarity for every car decision.': 'Un mercado claro para cada decisión de compra.',
      'Compare public offers by price, mileage and location, then create a structured listing that gives buyers the details they need.': 'Compara ofertas por precio, kilometraje y ubicación y crea un anuncio estructurado.',
      'active offers': 'ofertas activas', 'listing fee': 'tarifa de anuncio', 'Direct': 'Directo', 'seller contact': 'contacto del vendedor', 'Search the market': 'Buscar en el mercado', 'Search listings': 'Buscar anuncios', 'Sell Your Car': 'Vende tu auto',
      'Structured listings. Clear buyer signals.': 'Anuncios estructurados. Información clara.', 'Every offer is organized for faster comparison.': 'Cada oferta se organiza para comparar más rápido.',
      'Shop by need': 'Buscar por necesidad', 'Family SUVs': 'SUV familiares', 'Daily commuters': 'Uso diario', 'Performance cars': 'Autos deportivos', 'Low mileage': 'Poco kilometraje', 'Budget picks': 'Opciones económicas', 'Newly listed': 'Recién publicados', 'Popular brands': 'Marcas populares',
      'Reduced Car Offers': 'Ofertas de autos rebajados', 'Discover public car listings with clear prices, mileage, location and seller contact details.': 'Descubre anuncios con precio, kilometraje, ubicación y contacto claros.', 'All Offers': 'Todas las ofertas', 'My Listings': 'Mis anuncios', 'No public listings yet. The first submitted car will appear here as a marketplace card.': 'Aún no hay anuncios públicos. El primer auto publicado aparecerá aquí.',
      'Corporate': 'Empresa', 'Home': 'Inicio', 'Pricing': 'Precios', 'Explore': 'Explorar', 'News': 'Noticias', 'Guides': 'Guías', 'Methodology': 'Metodología', 'Information': 'Información', 'About Us': 'Acerca de', 'Contact': 'Contacto', 'Terms': 'Términos', 'Refund Policy': 'Reembolsos', 'Privacy Policy': 'Privacidad', 'Follow Us': 'Síguenos',
      placeholders: ['Marca, modelo o palabra clave', 'Ciudad o región', 'Presupuesto máximo'],
    },
    ru: {
      'CarQuantix Marketplace': 'Рынок CarQuantix', 'Marketplace clarity for every car decision.': 'Понятный рынок для каждого решения об автомобиле.',
      'Compare public offers by price, mileage and location, then create a structured listing that gives buyers the details they need.': 'Сравнивайте предложения по цене, пробегу и месту, затем создавайте подробное объявление.',
      'active offers': 'активных предложений', 'listing fee': 'плата за объявление', 'Direct': 'Напрямую', 'seller contact': 'контакт продавца', 'Search the market': 'Поиск по рынку', 'Search listings': 'Найти объявления', 'Sell Your Car': 'Продать автомобиль',
      'Structured listings. Clear buyer signals.': 'Структурированные объявления. Понятные данные.', 'Every offer is organized for faster comparison.': 'Каждое предложение удобно для быстрого сравнения.',
      'Shop by need': 'Выбор по потребностям', 'Family SUVs': 'Семейные кроссоверы', 'Daily commuters': 'На каждый день', 'Performance cars': 'Спортивные автомобили', 'Low mileage': 'Малый пробег', 'Budget picks': 'Доступные варианты', 'Newly listed': 'Новые объявления', 'Popular brands': 'Популярные марки',
      'Reduced Car Offers': 'Автомобили со сниженной ценой', 'Discover public car listings with clear prices, mileage, location and seller contact details.': 'Изучайте объявления с понятной ценой, пробегом, местом и контактами продавца.', 'All Offers': 'Все предложения', 'My Listings': 'Мои объявления', 'No public listings yet. The first submitted car will appear here as a marketplace card.': 'Публичных объявлений пока нет. Первый добавленный автомобиль появится здесь.',
      'Corporate': 'Компания', 'Home': 'Главная', 'Pricing': 'Цены', 'Explore': 'Разделы', 'News': 'Новости', 'Guides': 'Руководства', 'Methodology': 'Методология', 'Information': 'Информация', 'About Us': 'О нас', 'Contact': 'Контакты', 'Terms': 'Условия', 'Refund Policy': 'Возврат средств', 'Privacy Policy': 'Конфиденциальность', 'Follow Us': 'Подписывайтесь',
      placeholders: ['Марка, модель или ключевое слово', 'Город или регион', 'Максимальный бюджет'],
    },
  };

  const pack = packs[lang];
  if (!pack) return;
  const roots = [document.querySelector('.market-shell'), document.querySelector('.site-footer')].filter(Boolean);
  roots.forEach((root) => {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      const original = node.nodeValue.trim();
      if (!original || !pack[original]) continue;
      const leading = node.nodeValue.match(/^\s*/)?.[0] || '';
      const trailing = node.nodeValue.match(/\s*$/)?.[0] || '';
      node.nodeValue = `${leading}${pack[original]}${trailing}`;
    }
  });
  document.querySelectorAll('.market-search-control').forEach((input, index) => {
    if (pack.placeholders?.[index]) input.placeholder = pack.placeholders[index];
  });
  document.documentElement.lang = lang;
})();
