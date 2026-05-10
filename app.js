// ============================================================
// Hoko Collectables — app.js
// ============================================================

'use strict';

// ─── Product Catalogue ────────────────────────────────────────
const PRODUCTS = [
  // ── Action Figures ──
  { id: 1,  name: 'Dragon Ball Z – Goku Ultra Instinct Figure', category: 'figures', price: 89.99,  originalPrice: null,  badge: 'hot',  rating: 4.9, reviews: 214, emoji: '🐉', new: false },
  { id: 2,  name: 'Marvel Legends – Wolverine Retro Series',    category: 'figures', price: 34.99,  originalPrice: 44.99, badge: 'sale', rating: 4.7, reviews: 189, emoji: '🦅', new: false },
  { id: 3,  name: 'One Piece – Monkey D. Luffy Gear 5 Figure',  category: 'figures', price: 124.99, originalPrice: null,  badge: 'rare', rating: 5.0, reviews: 67,  emoji: '⚓', new: true  },
  { id: 4,  name: 'Star Wars Black Series – Darth Vader',       category: 'figures', price: 54.99,  originalPrice: null,  badge: 'new',  rating: 4.8, reviews: 302, emoji: '🌑', new: true  },
  { id: 5,  name: 'DC Multiverse – Batman The Dark Knight',     category: 'figures', price: 39.99,  originalPrice: 49.99, badge: 'sale', rating: 4.6, reviews: 143, emoji: '🦇', new: false },
  { id: 6,  name: 'Transformers Masterpiece – Optimus Prime',   category: 'figures', price: 219.99, originalPrice: null,  badge: 'rare', rating: 4.9, reviews: 88,  emoji: '🤖', new: false },

  // ── Trading Cards ──
  { id: 7,  name: 'Pokémon 1st Edition Base Set Charizard',     category: 'cards', price: 799.99, originalPrice: null,    badge: 'rare', rating: 5.0, reviews: 31,  emoji: '🔥', new: false },
  { id: 8,  name: 'Magic: The Gathering Black Lotus (LP)',       category: 'cards', price: 4999.00,originalPrice: null,    badge: 'rare', rating: 5.0, reviews: 8,   emoji: '🌹', new: false },
  { id: 9,  name: 'Pokémon Scarlet & Violet 151 Booster Box',   category: 'cards', price: 149.99, originalPrice: 179.99,  badge: 'sale', rating: 4.7, reviews: 425, emoji: '📦', new: true  },
  { id: 10, name: 'Yu-Gi-Oh! Blue Eyes White Dragon PSA 9',     category: 'cards', price: 189.99, originalPrice: null,    badge: 'hot',  rating: 4.9, reviews: 57,  emoji: '🐲', new: false },
  { id: 11, name: 'Sports – Patrick Mahomes Rookie Auto /99',   category: 'cards', price: 349.99, originalPrice: null,    badge: 'rare', rating: 4.8, reviews: 42,  emoji: '🏈', new: true  },
  { id: 12, name: 'One Piece Card Game – Shanks Secret Rare',   category: 'cards', price: 59.99,  originalPrice: 74.99,   badge: 'hot',  rating: 4.8, reviews: 136, emoji: '⚔️', new: true  },

  // ── Vintage Toys ──
  { id: 13, name: 'Original 1977 Star Wars Kenner Millennium Falcon', category: 'vintage', price: 599.99, originalPrice: null,   badge: 'rare', rating: 5.0, reviews: 19, emoji: '🚀', new: false },
  { id: 14, name: 'G.I. Joe 1982 Complete Set (Boxed)',          category: 'vintage', price: 299.99, originalPrice: null,   badge: 'rare', rating: 4.9, reviews: 23,  emoji: '🪖', new: false },
  { id: 15, name: 'He-Man Masters of Universe Castle Grayskull', category: 'vintage', price: 249.99, originalPrice: 299.99, badge: 'sale', rating: 4.7, reviews: 38,  emoji: '🏰', new: false },
  { id: 16, name: 'Transformers G1 Grimlock (MIB)',              category: 'vintage', price: 179.99, originalPrice: null,   badge: 'hot',  rating: 4.8, reviews: 55,  emoji: '🦕', new: false },
  { id: 17, name: 'Strawberry Shortcake 1980 Original Doll Set', category: 'vintage', price: 89.99,  originalPrice: 119.99, badge: 'sale', rating: 4.6, reviews: 47,  emoji: '🍓', new: true  },

  // ── Anime & Manga ──
  { id: 18, name: 'Neon Genesis Evangelion Unit-01 MG Model',   category: 'anime', price: 74.99,  originalPrice: null,   badge: 'new',  rating: 4.8, reviews: 163, emoji: '🤖', new: true  },
  { id: 19, name: 'Demon Slayer – Tanjiro Nendoroid Deluxe',    category: 'anime', price: 64.99,  originalPrice: 79.99,  badge: 'sale', rating: 4.9, reviews: 278, emoji: '🌸', new: false },
  { id: 20, name: 'Attack on Titan – Levi Ackerman Figure POP', category: 'anime', price: 49.99,  originalPrice: null,   badge: 'hot',  rating: 4.8, reviews: 312, emoji: '⚔️', new: false },
  { id: 21, name: 'Naruto Shippuden – 4th Hokage Resin Statue', category: 'anime', price: 149.99, originalPrice: null,   badge: 'rare', rating: 4.9, reviews: 91,  emoji: '🍃', new: true  },
  { id: 22, name: 'My Hero Academia – All Might Jumbo Figure',  category: 'anime', price: 99.99,  originalPrice: 129.99, badge: 'sale', rating: 4.7, reviews: 184, emoji: '💪', new: false },

  // ── Comics & Art ──
  { id: 23, name: 'Amazing Fantasy #15 (Reprint, CGC 9.8)',     category: 'comics', price: 299.99, originalPrice: null,   badge: 'rare', rating: 5.0, reviews: 14,  emoji: '🕷️', new: false },
  { id: 24, name: 'Batman Year One – Frank Miller Signed HC',   category: 'comics', price: 189.99, originalPrice: null,   badge: 'rare', rating: 4.9, reviews: 27,  emoji: '🦇', new: false },
  { id: 25, name: 'Invincible #1 First Print (Near Mint)',      category: 'comics', price: 119.99, originalPrice: 149.99, badge: 'sale', rating: 4.8, reviews: 63,  emoji: '💥', new: true  },
  { id: 26, name: 'One Punch Man Manga Set Vol 1-27',           category: 'comics', price: 139.99, originalPrice: null,   badge: 'new',  rating: 4.7, reviews: 207, emoji: '👊', new: true  },

  // ── Sports ──
  { id: 27, name: 'Michael Jordan 1986 Fleer Rookie Card PSA 8', category: 'sports', price: 2499.99,originalPrice: null,   badge: 'rare', rating: 5.0, reviews: 11,  emoji: '🏀', new: false },
  { id: 28, name: 'LeBron James Signed Jersey (Authenticated)',  category: 'sports', price: 799.99, originalPrice: null,   badge: 'rare', rating: 4.9, reviews: 36,  emoji: '🏀', new: false },
  { id: 29, name: 'Lionel Messi World Cup 2022 Panini Card /50', category: 'sports', price: 449.99, originalPrice: null,   badge: 'hot',  rating: 5.0, reviews: 44,  emoji: '⚽', new: true  },
  { id: 30, name: 'Tom Brady 2000 Bowman Chrome Rookie PSA 10', category: 'sports', price: 1299.99,originalPrice: null,   badge: 'rare', rating: 4.9, reviews: 22,  emoji: '🏈', new: false },
  { id: 31, name: 'Babe Ruth 1933 Goudey Card (Graded)',        category: 'sports', price: 3499.00,originalPrice: null,   badge: 'rare', rating: 5.0, reviews: 7,   emoji: '⚾', new: false },
  { id: 32, name: 'UFC – Conor McGregor Signed Gloves',         category: 'sports', price: 299.99, originalPrice: 399.99, badge: 'sale', rating: 4.6, reviews: 88,  emoji: '🥊', new: true  },
];

// ─── State ────────────────────────────────────────────────────
let cart = JSON.parse(localStorage.getItem('hokoCart') || '[]');
let wishlist = JSON.parse(localStorage.getItem('hokoWishlist') || '[]');
let currentFilter = 'all';
let currentSort   = 'featured';
let searchQuery   = '';
let displayedCount = 8;
const PAGE_SIZE    = 8;

// ─── DOM Helpers ──────────────────────────────────────────────
const $  = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

// ─── Save Helpers ─────────────────────────────────────────────
function saveCart()     { localStorage.setItem('hokoCart',     JSON.stringify(cart));     }
function saveWishlist() { localStorage.setItem('hokoWishlist', JSON.stringify(wishlist)); }

// ─── Toast ────────────────────────────────────────────────────
function showToast(msg, duration = 3000) {
  const toast = $('#toast');
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), duration);
}

// ─── Render Products ──────────────────────────────────────────
function getFilteredProducts() {
  let list = PRODUCTS.slice();

  // Category filter
  if (currentFilter !== 'all') {
    list = list.filter(p => p.category === currentFilter);
  }

  // Search filter
  if (searchQuery.trim()) {
    const q = searchQuery.toLowerCase();
    list = list.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.category.toLowerCase().includes(q)
    );
  }

  // Sort
  switch (currentSort) {
    case 'price-asc':  list.sort((a, b) => a.price - b.price); break;
    case 'price-desc': list.sort((a, b) => b.price - a.price); break;
    case 'newest':     list.sort((a, b) => (b.new ? 1 : 0) - (a.new ? 1 : 0)); break;
    case 'rating':     list.sort((a, b) => b.rating - a.rating); break;
    default: break; // 'featured' — keep original order
  }

  return list;
}

function productCardHTML(p) {
  const inWishlist   = wishlist.includes(p.id);
  const priceDisplay = p.originalPrice
    ? `<span class="product-price">$${p.price.toFixed(2)}</span><span class="price-original">$${p.originalPrice.toFixed(2)}</span>`
    : `<span class="product-price">$${p.price.toFixed(2)}</span>`;
  const stars = '★'.repeat(Math.floor(p.rating)) + (p.rating % 1 >= 0.5 ? '½' : '');

  return `
    <div class="product-card" data-id="${p.id}" data-category="${p.category}">
      ${p.badge ? `<span class="product-badge badge-${p.badge}">${p.badge}</span>` : ''}
      <button class="product-wishlist ${inWishlist ? 'wishlisted' : ''}" onclick="toggleWishlist(${p.id})" aria-label="Toggle wishlist" title="${inWishlist ? 'Remove from wishlist' : 'Add to wishlist'}">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="${inWishlist ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
      </button>
      <div class="product-img">${p.emoji}</div>
      <div class="product-info">
        <span class="product-category">${p.category}</span>
        <h3 class="product-name">${p.name}</h3>
        <div class="product-rating">
          <span class="stars-filled" aria-label="${p.rating} stars">${'★'.repeat(Math.floor(p.rating))}${p.rating % 1 >= 0.5 ? '½' : ''}</span>
          <span class="rating-count">(${p.reviews})</span>
        </div>
        <div class="product-footer">
          <div>${priceDisplay}</div>
          <button class="add-to-cart-btn" onclick="addToCart(${p.id})">Add to Cart</button>
        </div>
      </div>
    </div>
  `;
}

function renderNewArrivals() {
  const grid = $('#newArrivalsGrid');
  if (!grid) return;
  const newItems = PRODUCTS.filter(p => p.new).slice(0, 4);
  grid.innerHTML = newItems.map(productCardHTML).join('');
}

function renderProducts(reset = false) {
  const grid = $('#productsGrid');
  if (!grid) return;

  if (reset) displayedCount = PAGE_SIZE;

  const all = getFilteredProducts();
  const visible = all.slice(0, displayedCount);

  grid.innerHTML = visible.length
    ? visible.map(productCardHTML).join('')
    : '<p class="no-results" style="color:var(--gray);text-align:center;padding:40px 0;grid-column:1/-1">No products found. Try a different filter or search term.</p>';

  const loadBtn = $('#loadMoreBtn');
  if (loadBtn) {
    loadBtn.style.display = (displayedCount >= all.length) ? 'none' : 'inline-block';
    loadBtn.textContent = `Load More Products (${Math.min(PAGE_SIZE, all.length - displayedCount)} more)`;
  }
}

// ─── Filter & Sort ────────────────────────────────────────────
function filterCategory(cat) {
  currentFilter = cat;
  searchQuery   = '';
  renderProducts(true);
  // Update filter tabs
  $$('.filter-tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.filter === cat);
  });
  // Scroll to shop section
  $('#shop').scrollIntoView({behavior: 'smooth'});
}

$$('.filter-tab').forEach(btn => {
  btn.addEventListener('click', () => filterCategory(btn.dataset.filter));
});

const sortSelect = $('#sortSelect');
if (sortSelect) {
  sortSelect.addEventListener('change', () => {
    currentSort = sortSelect.value;
    renderProducts(true);
  });
}

$('#loadMoreBtn')?.addEventListener('click', () => {
  displayedCount += PAGE_SIZE;
  renderProducts(false);
});

// ─── Cart ─────────────────────────────────────────────────────
function addToCart(id) {
  const product = PRODUCTS.find(p => p.id === id);
  if (!product) return;

  const existing = cart.find(i => i.id === id);
  if (existing) {
    existing.qty++;
  } else {
    cart.push({ id, qty: 1 });
  }

  saveCart();
  updateCartUI();
  showToast(`✓ "${product.name.split('–')[0].trim()}" added to cart`);
}

function removeFromCart(id) {
  cart = cart.filter(i => i.id !== id);
  saveCart();
  updateCartUI();
  renderCartItems();
}

function updateQty(id, delta) {
  const item = cart.find(i => i.id === id);
  if (!item) return;
  item.qty = Math.max(1, item.qty + delta);
  saveCart();
  updateCartUI();
  renderCartItems();
}

function getCartTotal() {
  return cart.reduce((sum, item) => {
    const p = PRODUCTS.find(p => p.id === item.id);
    return p ? sum + p.price * item.qty : sum;
  }, 0);
}

function getCartItemCount() {
  return cart.reduce((n, i) => n + i.qty, 0);
}

function updateCartUI() {
  const count = getCartItemCount();
  const cartCount = $('#cartCount');
  const cartItemCount = $('#cartItemCount');
  if (cartCount)     cartCount.textContent = count;
  if (cartItemCount) cartItemCount.textContent = `(${count} ${count === 1 ? 'item' : 'items'})`;

  const cartSubtotal = $('#cartSubtotal');
  if (cartSubtotal) cartSubtotal.textContent = `$${getCartTotal().toFixed(2)}`;

  const cartFooter = $('#cartFooter');
  if (cartFooter) cartFooter.style.display = cart.length ? 'block' : 'none';
}

function renderCartItems() {
  const container = $('#cartItems');
  if (!container) return;

  if (!cart.length) {
    container.innerHTML = `
      <div class="cart-empty">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        <p>Your cart is empty</p>
        <a href="#shop" class="btn-primary" onclick="closeCart()">Start Shopping</a>
      </div>`;
    return;
  }

  container.innerHTML = cart.map(item => {
    const p = PRODUCTS.find(prod => prod.id === item.id);
    if (!p) return '';
    return `
      <div class="cart-item">
        <div class="cart-item-img">${p.emoji}</div>
        <div class="cart-item-info">
          <div class="cart-item-name">${p.name}</div>
          <div class="cart-item-price">$${p.price.toFixed(2)}</div>
          <div class="cart-item-qty">
            <button class="qty-btn" onclick="updateQty(${p.id}, -1)">−</button>
            <span>${item.qty}</span>
            <button class="qty-btn" onclick="updateQty(${p.id}, 1)">+</button>
            <button class="qty-btn" style="margin-left:auto;color:var(--primary)" onclick="removeFromCart(${p.id})" title="Remove">✕</button>
          </div>
        </div>
      </div>`;
  }).join('');
}

// ─── Cart Sidebar ─────────────────────────────────────────────
function openCart() {
  renderCartItems();
  updateCartUI();
  $('#cartSidebar').classList.add('active');
  $('#cartOverlay').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeCart() {
  $('#cartSidebar').classList.remove('active');
  $('#cartOverlay').classList.remove('active');
  document.body.style.overflow = '';
}

$('#cartToggle')?.addEventListener('click', openCart);
$('#cartClose')?.addEventListener('click', closeCart);
$('#cartOverlay')?.addEventListener('click', closeCart);

// ─── Wishlist ────────────────────────────────────────────────
function toggleWishlist(id) {
  const idx = wishlist.indexOf(id);
  if (idx === -1) {
    wishlist.push(id);
    showToast('❤️ Added to wishlist');
  } else {
    wishlist.splice(idx, 1);
    showToast('Removed from wishlist');
  }
  saveWishlist();
  updateWishlistUI();
  // Update button appearance without full re-render
  const btn = `[data-id="${id}"] .product-wishlist`;
  $(btn).forEach(el => {
    const svg = el.querySelector('svg');
    if (wishlist.includes(id)) {
      el.classList.add('wishlisted');
      svg?.setAttribute('fill', 'currentColor');
    } else {
      el.classList.remove('wishlisted');
      svg?.setAttribute('fill', 'none');
    }
  });
}

function updateWishlistUI() {
  const count = wishlist.length;
  const badge = $('#wishlistCount');
  if (badge) {
    badge.textContent = count;
    badge.style.display = count > 0 ? 'flex' : 'none';
  }
}

$('#wishlistBtn')?.addEventListener('click', () => {
  if (!wishlist.length) {
    showToast('Your wishlist is empty');
    return;
  }
  showToast(`❤️ You have ${wishlist.length} item${wishlist.length > 1 ? 's' : ''} in your wishlist`);
});

// ─── Search ───────────────────────────────────────────────────
const searchToggle = $('#searchToggle');
const searchBar    = $('#searchBar');
const searchInput  = $('#searchInput');

searchToggle?.addEventListener('click', () => {
  searchBar?.classList.toggle('active');
  if (searchBar?.classList.contains('active')) {
    searchInput?.focus();
  }
});

searchInput?.addEventListener('input', () => {
  searchQuery   = searchInput.value;
  currentFilter = 'all';
  $$('.filter-tab').forEach(b => b.classList.toggle('active', b.dataset.filter === 'all'));
  renderProducts(true);
  if (searchQuery.trim()) {
    $('#shop').scrollIntoView({behavior: 'smooth'});
  }
});

searchInput?.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    searchBar?.classList.remove('active');
    searchQuery  = '';
    searchInput.value = '';
    renderProducts(true);
  }
});

// ─── Navigation ───────────────────────────────────────────────
const hamburger = $('#hamburger');
const navLinks  = $('#navLinks');

hamburger?.addEventListener('click', () => {
  navLinks?.classList.toggle('active');
  hamburger.classList.toggle('active');
});

// Close mobile nav on link click
$$('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    navLinks?.classList.remove('active');
    hamburger?.classList.remove('active');
  });
});

// Active nav link on scroll
const sections = $$('section[id]');
const navItems = $$('.nav-link');

function updateActiveNav() {
  let current = '';
  sections.forEach(sec => {
    if (window.scrollY >= sec.offsetTop - 120) {
      current = sec.id;
    }
  });
  navItems.forEach(link => {
    const href = link.getAttribute('href')?.replace('#', '');
    link.classList.toggle('active', href === current);
  });
}

window.addEventListener('scroll', updateActiveNav, {passive: true});

// ─── Countdown Timer ─────────────────────────────────────────
function startCountdown(endTimeKey, displayEl) {
  if (!displayEl) return;

  let end = parseInt(sessionStorage.getItem(endTimeKey), 10);
  if (!end || end < Date.now()) {
    // 3 hours from now
    end = Date.now() + 3 * 60 * 60 * 1000;
    sessionStorage.setItem(endTimeKey, end.toString());
  }

  function tick() {
    const diff = end - Date.now();
    if (diff <= 0) {
      displayEl.textContent = 'Offer expired!';
      return;
    }
    const h = Math.floor(diff / 3600000).toString().padStart(2, '0');
    const m = Math.floor((diff % 3600000) / 60000).toString().padStart(2, '0');
    const s = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
    displayEl.textContent = `Offer ends in: ${h}:${m}:${s}`;
    setTimeout(tick, 1000);
  }
  tick();
}

startCountdown('hokoBannerEnd', $('#bannerTimer'));

// ─── Newsletter Form ─────────────────────────────────────────
$('#newsletterForm')?.addEventListener('submit', e => {
  e.preventDefault();
  const name  = $('#nlName').value.trim();
  const email = $('#nlEmail').value.trim();
  if (!name || !email) return;
  showToast(`🎉 Thanks ${name}! Check ${email} for your 10% off code.`);
  e.target.reset();
});

// ─── Contact Form ─────────────────────────────────────────────
$('#contactForm')?.addEventListener('submit', e => {
  e.preventDefault();
  showToast('✉️ Message sent! We'll be in touch within 24 hours.');
  e.target.reset();
});

// ─── Sticky Nav Shadow ────────────────────────────────────────
const navbar = $('#navbar');
window.addEventListener('scroll', () => {
  if (navbar) {
    navbar.style.boxShadow = window.scrollY > 20
      ? '0 4px 24px rgba(0,0,0,0.5)'
      : 'none';
  }
}, {passive: true});

// ─── Scroll-reveal Animation ─────────────────────────────────
const observerOpts = { threshold: 0.1, rootMargin: '0px 0px -40px 0px' };

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      revealObserver.unobserve(entry.target);
    }
  });
}, observerOpts);

function setupReveal() {
  $$('.category-card, .product-card, .testimonial-card, .trust-item').forEach(el => {
    el.style.opacity   = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    revealObserver.observe(el);
  });
}

// Add "revealed" styles
const revealStyle = document.createElement('style');
revealStyle.textContent = '.revealed { opacity: 1 !important; transform: translateY(0) !important; }';
document.head.appendChild(revealStyle);

// ─── Hero Card Parallax ───────────────────────────────────────
document.addEventListener('mousemove', e => {
  const cards = $$('.hero-card');
  if (!cards.length) return;
  const xAxis = (window.innerWidth  / 2 - e.clientX) / 40;
  const yAxis = (window.innerHeight / 2 - e.clientY) / 40;
  cards[0]?.style.setProperty('transform', `translateY(-4px) rotateX(${yAxis}deg) rotateY(${-xAxis}deg)`);
  cards[1]?.style.setProperty('transform', `translateY(-4px) rotateX(${yAxis * 0.8}deg) rotateY(${-xAxis * 0.8}deg)`);
  cards[2]?.style.setProperty('transform', `translateY(-4px) rotateX(${yAxis * 0.6}deg) rotateY(${-xAxis * 0.6}deg)`);
});

// ─── "Proceed to Checkout" placeholder ────────────────────────
document.addEventListener('click', e => {
  if (e.target.closest('.cart-footer .btn-primary:not(.btn-secondary)')) {
    if (!e.target.closest('.btn-secondary')) {
      showToast('🛒 Checkout coming soon! We're working on it.', 4000);
    }
  }
});


// ─── Product Detail Modal ─────────────────────────────────────
const PRODUCT_DESCS = {
  figures: 'A highly detailed, museum-quality figure from our certified-authentic collection. Perfect mint condition, comes with original packaging and certificate of authenticity.',
  cards:   'A rare and highly sought-after trading card in excellent condition. Independently graded and verified. Stored in protective sleeve. Perfect addition to any collection.',
  vintage: 'An original vintage piece in remarkable condition for its age. Thoroughly cleaned and professionally inspected. A true collector\'s treasure from a golden era.',
  anime:   'Official licensed merchandise from a reputable manufacturer. Highly detailed sculpt with premium paint applications. Comes in original box with all accessories.',
  comics:  'A premium-condition comic or art piece, independently graded and verified. Stored in archival-quality materials. A cornerstone for any serious collection.',
  sports:  'Authentic sports memorabilia with certificate of authenticity. Verified by a reputable third-party service. An iconic piece of sports history.',
};

function openModal(id) {
  const p = PRODUCTS.find(prod => prod.id === id);
  if (!p) return;

  $('#modalImg').textContent   = p.emoji;
  $('#modalCategory').textContent = p.category.charAt(0).toUpperCase() + p.category.slice(1);
  $('#modalTitle').textContent = p.name;
  $('#modalStars').textContent = '★'.repeat(Math.floor(p.rating)) + (p.rating % 1 >= 0.5 ? '½' : '');
  $('#modalReviews').textContent = `(${p.reviews} reviews)`;
  $('#modalDesc').textContent  = PRODUCT_DESCS[p.category] || '';

  const badge = $('#modalBadge');
  if (badge) {
    badge.textContent  = p.badge || '';
    badge.className    = 'product-badge' + (p.badge ? ` badge-${p.badge}` : '');
    badge.style.display = p.badge ? 'inline-block' : 'none';
  }

  const price = $('#modalPrice');
  if (price) {
    price.innerHTML = p.originalPrice
      ? `${p.price.toFixed(2)} <span style="font-size:.9rem;color:var(--gray);text-decoration:line-through;margin-left:8px">${p.originalPrice.toFixed(2)}</span>`
      : `${p.price.toFixed(2)}`;
  }

  const addBtn = $('#modalAddCart');
  if (addBtn) {
    addBtn.onclick = () => { addToCart(p.id); closeModal(); };
  }

  const wishBtn = $('#modalWishlist');
  if (wishBtn) {
    const inWishlist = wishlist.includes(p.id);
    wishBtn.textContent = inWishlist ? '♥ In Wishlist' : '♡ Wishlist';
    wishBtn.onclick = () => {
      toggleWishlist(p.id);
      wishBtn.textContent = wishlist.includes(p.id) ? '♥ In Wishlist' : '♡ Wishlist';
    };
  }

  $('#productModal').classList.add('active');
  $('#modalOverlay').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  $('#productModal')?.classList.remove('active');
  $('#modalOverlay')?.classList.remove('active');
  document.body.style.overflow = '';
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    closeModal();
    closeCart();
  }
});

// Make product images/names clickable to open modal
document.addEventListener('click', e => {
  const card = e.target.closest('.product-card');
  if (!card) return;
  // Don't open modal if they clicked a button
  if (e.target.closest('button, .add-to-cart-btn')) return;
  const id = parseInt(card.dataset.id);
  if (id) openModal(id);
});

// ─── Init ─────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  renderNewArrivals();
  renderProducts(true);
  updateCartUI();
  updateWishlistUI();
  setupReveal();
});

// Also run if DOM already loaded (script at end of body)
if (document.readyState !== 'loading') {
  renderNewArrivals();
  renderProducts(true);
  updateCartUI();
  updateWishlistUI();
  setupReveal();
}
