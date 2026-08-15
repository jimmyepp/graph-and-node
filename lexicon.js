/**
 * Graph & Node Lexicon Controller
 * Manages search, filtering, drawer overlays, and routing for GEO/SEO terms.
 */

document.addEventListener('DOMContentLoaded', () => {
  // --- State Variables ---
  let searchQuery = '';
  let activeCategory = 'all';
  let activeDepth = 'all';
  let activeRisk = 'all';

  // --- Category Map ---
  const CATEGORY_NAMES = {
    'dense-retrieval': 'Retrieval & RAG',
    'entity-architecture': 'Entity & Graph',
    'conversational-synthesis': 'Synthesis & AEO',
    'performance-metrics': 'Metrics & Tracking',
    'enterprise-strategy': 'Enterprise Strategy'
  };

  const DEPTH_NAMES = {
    'algorithmic': 'Algorithmic Substrate',
    'strategic': 'Strategic Framework'
  };

  const RISK_NAMES = {
    'high': 'High Risk',
    'medium': 'Medium Risk',
    'low': 'Low Risk'
  };

  // --- DOM Elements ---
  const searchInput = document.getElementById('lexicon-search');
  const lexiconGrid = document.getElementById('lexicon-grid');
  const emptyState = document.getElementById('empty-state');
  const resultsCount = document.getElementById('results-count');
  const resetFiltersBtn = document.getElementById('reset-filters');
  const emptyResetBtn = document.getElementById('empty-reset');
  
  // Drawer Elements
  const detailsDrawer = document.getElementById('details-drawer');
  const drawerBackdrop = document.getElementById('drawer-backdrop');
  const closeDrawerBtn = document.getElementById('close-drawer');
  
  const drawerTermName = document.getElementById('drawer-term-name');
  const drawerCategory = document.getElementById('drawer-category-badge');
  const drawerDepth = document.getElementById('drawer-depth-badge');
  const drawerRisk = document.getElementById('drawer-risk-badge');
  const drawerDefinition = document.getElementById('drawer-definition');
  const drawerStrategicFocus = document.getElementById('drawer-strategic-focus');
  const drawerHealthcareImpact = document.getElementById('drawer-healthcare-impact');
  const drawerSources = document.getElementById('drawer-sources');
  const drawerRelated = document.getElementById('drawer-related');
  const drawerCodeSection = document.getElementById('drawer-code-section');
  const drawerCodeBlock = document.getElementById('drawer-code-block');
  const copyCodeBtn = document.getElementById('copy-code-btn');

  // Mobile Menu Elements
  const hamburgerBtn = document.getElementById('lexicon-hamburger');
  const mobileMenuDrawer = document.getElementById('mobile-menu-drawer');
  const body = document.body;

  // --- Rendering Logic ---

  function renderGrid() {
    // 1. Get all static cards in the grid
    const cards = lexiconGrid.querySelectorAll('.term-card');
    let visibleCount = 0;

    cards.forEach(card => {
      const termId = card.dataset.id;
      const term = LEXICON_DATA.find(t => t.id === termId);
      
      if (!term) {
        card.classList.add('hidden');
        return;
      }

      // Evaluate filters and search
      const matchesSearch = searchQuery === '' || 
        term.name.toLowerCase().includes(searchQuery) ||
        term.definition.toLowerCase().includes(searchQuery) ||
        term.strategicFocus.toLowerCase().includes(searchQuery) ||
        (term.healthcareImpact && term.healthcareImpact.toLowerCase().includes(searchQuery));
      
      const matchesCategory = activeCategory === 'all' || term.category === activeCategory;
      const matchesDepth = activeDepth === 'all' || term.depth === activeDepth;
      const matchesRisk = activeRisk === 'all' || term.riskLevel === activeRisk;

      if (matchesSearch && matchesCategory && matchesDepth && matchesRisk) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    // 2. Update count & visibility
    resultsCount.textContent = `Found ${visibleCount} ${visibleCount === 1 ? 'term' : 'terms'}`;
    
    // Toggle Reset Button visibility
    const isFiltered = searchQuery !== '' || activeCategory !== 'all' || activeDepth !== 'all' || activeRisk !== 'all';
    resetFiltersBtn.style.display = isFiltered ? 'inline-block' : 'none';

    if (visibleCount === 0) {
      lexiconGrid.style.display = 'none';
      emptyState.style.display = 'block';
    } else {
      lexiconGrid.style.display = 'grid';
      emptyState.style.display = 'none';
    }
  }

  function bindCardEvents() {
    const cards = lexiconGrid.querySelectorAll('.term-card');
    cards.forEach(card => {
      const termId = card.dataset.id;
      card.addEventListener('click', () => openDrawer(termId));
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openDrawer(termId);
        }
      });
    });
  }

  // --- Drawer Interaction ---

  function openDrawer(termId) {
    const term = LEXICON_DATA.find(t => t.id === termId);
    if (!term) return;

    // Set text contents
    drawerTermName.textContent = term.name;
    drawerDefinition.textContent = term.definition;
    drawerStrategicFocus.textContent = term.strategicFocus;
    drawerHealthcareImpact.textContent = term.healthcareImpact || 'Not evaluated yet.';

    // Setup Badges
    drawerCategory.textContent = CATEGORY_NAMES[term.category] || term.category;
    
    drawerDepth.textContent = DEPTH_NAMES[term.depth] || term.depth;
    
    // Risk badge styling update
    drawerRisk.className = `drawer-badge ${term.riskLevel}`;
    drawerRisk.textContent = RISK_NAMES[term.riskLevel] || term.riskLevel;

    // Load Sources
    drawerSources.innerHTML = '';
    if (term.sources && term.sources.length > 0) {
      term.sources.forEach(src => {
        const li = document.createElement('li');
        li.innerHTML = `<a href="${src.url}" target="_blank" rel="noopener noreferrer">${src.name} &nearr;</a>`;
        drawerSources.appendChild(li);
      });
    } else {
      drawerSources.innerHTML = '<li>No citations registered.</li>';
    }

    // Load Related Terms
    drawerRelated.innerHTML = '';
    if (term.related && term.related.length > 0) {
      term.related.forEach(relId => {
        const relTerm = LEXICON_DATA.find(t => t.id === relId);
        if (relTerm) {
          const btn = document.createElement('button');
          btn.className = 'related-node-btn';
          btn.textContent = relTerm.name;
          btn.addEventListener('click', () => {
            // Smoothly swap drawer content
            openDrawer(relId);
          });
          drawerRelated.appendChild(btn);
        }
      });
    } else {
      drawerRelated.innerHTML = '<span style="font-size: 0.85rem; color: var(--pico-muted-color);">No direct parent/child nodes linked.</span>';
    }

    // Setup Code Sandbox (Option 2)
    if (term.codeTemplate) {
      drawerCodeBlock.textContent = term.codeTemplate;
      drawerCodeSection.style.display = 'block';
      copyCodeBtn.textContent = 'Copy Code';
      copyCodeBtn.style.borderColor = 'rgba(0, 245, 196, 0.3)';
      copyCodeBtn.style.color = '#00f5c4';
    } else {
      drawerCodeSection.style.display = 'none';
      drawerCodeBlock.textContent = '';
    }

    // Slide open UI
    detailsDrawer.classList.add('open');
    drawerBackdrop.classList.add('open');
    detailsDrawer.setAttribute('aria-hidden', 'false');
    body.style.overflow = 'hidden'; // Lock main page scrolling

    // Update URL hash without jumping page scroll
    try {
      history.replaceState(null, null, `#${term.id}`);
    } catch (e) {
      console.warn('History navigation blocked by browser security policy (common under file:// protocol).', e);
    }
  }

  function closeDrawer() {
    detailsDrawer.classList.remove('open');
    drawerBackdrop.classList.remove('open');
    detailsDrawer.setAttribute('aria-hidden', 'true');
    body.style.overflow = ''; // Unlock page scroll

    // Clear URL hash
    try {
      history.replaceState(null, null, ' ');
    } catch (e) {
      console.warn('History navigation blocked by browser security policy (common under file:// protocol).', e);
    }
  }

  // --- Pill Event Handlers ---

  function setupPillFilters(containerId, stateUpdater) {
    const pills = document.querySelectorAll(`#${containerId} .pill`);
    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        // Toggle active class among group
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');

        // Update state and re-render
        stateUpdater(pill.dataset.value);
        renderGrid();
      });
    });
  }

  function resetAllFilters() {
    // Reset state
    searchQuery = '';
    activeCategory = 'all';
    activeDepth = 'all';
    activeRisk = 'all';

    // Clear Search Input
    searchInput.value = '';

    // Reset Pill Active states
    document.querySelectorAll('.filter-pills').forEach(group => {
      const pills = group.querySelectorAll('.pill');
      pills.forEach(p => p.classList.remove('active'));
      const allPill = group.querySelector('[data-value="all"]');
      if (allPill) allPill.classList.add('active');
    });

    renderGrid();
  }

  // --- Mobile Hamburger Menu Logic ---
  
  if (hamburgerBtn && mobileMenuDrawer) {
    function toggleMobileMenu() {
      const isOpen = mobileMenuDrawer.classList.toggle('open');
      hamburgerBtn.classList.toggle('active');
      hamburgerBtn.setAttribute('aria-expanded', isOpen);
      body.classList.toggle('menu-open', isOpen);
    }

    hamburgerBtn.addEventListener('click', toggleMobileMenu);

    const drawerLinks = mobileMenuDrawer.querySelectorAll('a');
    drawerLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileMenuDrawer.classList.remove('open');
        hamburgerBtn.classList.remove('active');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
        body.classList.remove('menu-open');
      });
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileMenuDrawer.classList.contains('open')) {
        toggleMobileMenu();
      }
    });
  }

  // --- Initial Bindings ---

  // Bind Search Input
  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderGrid();
  });

  // Bind Pill Groups
  setupPillFilters('category-pills', val => activeCategory = val);
  setupPillFilters('depth-pills', val => activeDepth = val);
  setupPillFilters('risk-pills', val => activeRisk = val);

  // Bind Reset Buttons
  resetFiltersBtn.addEventListener('click', resetAllFilters);
  emptyResetBtn.addEventListener('click', resetAllFilters);

  // Bind Drawer Close
  closeDrawerBtn.addEventListener('click', closeDrawer);
  drawerBackdrop.addEventListener('click', closeDrawer);

  // Bind Copy Code Button
  if (copyCodeBtn) {
    copyCodeBtn.addEventListener('click', () => {
      const code = drawerCodeBlock.textContent;
      if (!code) return;

      navigator.clipboard.writeText(code).then(() => {
        copyCodeBtn.textContent = 'Copied!';
        copyCodeBtn.style.borderColor = '#00f5c4';
        copyCodeBtn.style.color = '#0c0e14';
        copyCodeBtn.style.backgroundColor = '#00f5c4';
        setTimeout(() => {
          copyCodeBtn.textContent = 'Copy Code';
          copyCodeBtn.style.borderColor = 'rgba(0, 245, 196, 0.3)';
          copyCodeBtn.style.color = '#00f5c4';
          copyCodeBtn.style.backgroundColor = 'transparent';
        }, 2000);
      }).catch(err => {
        console.error('Failed to copy code: ', err);
      });
    });
  }

  // Close drawer on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && detailsDrawer.classList.contains('open')) {
      closeDrawer();
    }
  });

  // --- Deep Linking Routing ---

  function checkUrlHash() {
    const hash = window.location.hash.slice(1);
    if (hash) {
      const matchedTerm = LEXICON_DATA.find(t => t.id === hash);
      if (matchedTerm) {
        // Delay opening drawer slightly to ensure DOM is fully ready
        setTimeout(() => openDrawer(matchedTerm.id), 200);
      }
    }
  }

  // Run initial setup
  bindCardEvents();
  renderGrid();
  checkUrlHash();

  // Listen for hash changes (e.g. forward/back browser buttons)
  window.addEventListener('hashchange', () => {
    const hash = window.location.hash.slice(1);
    if (hash) {
      openDrawer(hash);
    } else {
      closeDrawer();
    }
  });
});
