const API_BASE = 'http://localhost:5000/api';
let products = [];
let cartItems = [];
let currentCategory = '';
let cartOpen = false;
let checkoutOpen = false;
const sessionId = 'user_' + Date.now();

function $(sel) { return document.querySelector(sel); }
function $$(sel) { return document.querySelectorAll(sel); }

async function fetchAPI(endpoint, opts = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  };
  if (config.body && typeof config.body === 'object') config.body = JSON.stringify(config.body);
  const res = await fetch(url, config);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || 'Request failed');
  }
  return res.json();
}

function showToast(msg, type = 'success') {
  let t = $('#toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'toast'; t.className = 'toast';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.className = 'toast';
  t.classList.add(type);
  requestAnimationFrame(() => t.classList.add('show'));
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 3000);
}

function formatPrice(n) {
  return '$' + Number(n).toFixed(2);
}

async function loadProducts(category = '', search = '') {
  const grid = $('#productsGrid');
  grid.innerHTML = '<div class="loading">Loading amazing fashion...</div>';
  let url = '/products';
  const params = [];
  if (category) params.push('category=' + encodeURIComponent(category));
  if (search) params.push('search=' + encodeURIComponent(search));
  if (params.length) url += '?' + params.join('&');
  try {
    products = await fetchAPI(url);
    renderProducts(products);
  } catch (e) {
    grid.innerHTML = `<div class="loading">Couldn't load products. Make sure the server is running.<br><span style="color:#e94560;font-size:13px;">${e.message}</span></div>`;
  }
}

function renderProducts(items) {
  const grid = $('#productsGrid');
  if (!items.length) {
    grid.innerHTML = '<div class="loading">No products found</div>';
    return;
  }
  grid.innerHTML = items.map(p => `
    <div class="product-card">
      <div class="product-image">
        <img src="${p.image_url}" alt="${p.name}" loading="lazy" onerror="this.parentElement.style.background='linear-gradient(135deg,#1a1a2e,#2d4059)';this.style.display='none';this.parentElement.innerHTML='<span style=\\"font-size:48px;opacity:0.2\\">📸</span>'">
      </div>
      <div class="product-info">
        <div class="product-category">${p.category}</div>
        <div class="product-name">${p.name}</div>
        <div class="product-description">${p.description}</div>
        <div class="product-bottom">
          <span class="product-price">${formatPrice(p.price)}</span>
          <button class="add-to-cart-btn" data-id="${p.id}" data-name="${p.name.replace(/"/g,'&quot;')}" data-price="${p.price}">Add to Bag</button>
        </div>
      </div>
    </div>
  `).join('');
  grid.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const id = parseInt(btn.dataset.id);
      const name = btn.dataset.name;
      const price = parseFloat(btn.dataset.price);
      await addToCart(id, name, price);
      btn.textContent = '✓ Added';
      btn.classList.add('added');
      setTimeout(() => { btn.textContent = 'Add to Bag'; btn.classList.remove('added'); }, 1500);
    });
  });
}

async function addToCart(id, name, price, qty = 1, size = '', color = '') {
  try {
    const data = await fetchAPI(`/cart?session_id=${sessionId}`, {
      method: 'POST',
      body: { id, name, price, quantity: qty, size, color },
    });
    cartItems = data.items || [];
    updateCartUI(data);
    const badge = $('#cartCount');
    badge.textContent = data.item_count || 0;
    badge.classList.remove('bounce');
    void badge.offsetWidth;
    badge.classList.add('bounce');
    showToast(`${name} added to bag!`);
  } catch (e) {
    showToast('Cart service unavailable', 'error');
  }
}

async function removeFromCart(id, size = '', color = '', qty = 1) {
  try {
    const data = await fetchAPI(`/cart?session_id=${sessionId}`, {
      method: 'DELETE',
      body: { id, size, color, quantity: qty },
    });
    cartItems = data.items || [];
    updateCartUI(data);
    $('#cartCount').textContent = data.item_count || 0;
  } catch (e) {
    showToast('Failed to update cart', 'error');
  }
}

async function clearCart() {
  try {
    const data = await fetchAPI(`/cart?session_id=${sessionId}`, { method: 'DELETE' });
    cartItems = [];
    updateCartUI(data);
    $('#cartCount').textContent = '0';
  } catch (e) {}
}

async function loadCart() {
  try {
    const data = await fetchAPI(`/cart?session_id=${sessionId}`);
    cartItems = data.items || [];
    updateCartUI(data);
    $('#cartCount').textContent = data.item_count || 0;
  } catch (e) {
    console.log('Cart service not available yet');
  }
}

function updateCartUI(data) {
  const list = $('#cartItems');
  const summary = $('#cartSummary');
  if (!data || !data.items || !data.items.length) {
    list.innerHTML = `
      <div class="cart-empty">
        <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="1.2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
        <p>Your bag is empty</p>
        <span>Add some items to get started</span>
      </div>`;
    summary.style.display = 'none';
    return;
  }
  summary.style.display = 'block';
  list.innerHTML = data.items.map(item => `
    <div class="cart-item">
      <div class="cart-item-image">
        <div style="width:100%;height:100%;background:linear-gradient(135deg,#1a1a2e,#2d4059);display:flex;align-items:center;justify-content:center;font-size:28px;">📦</div>
      </div>
      <div class="cart-item-details">
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-meta">${item.size ? item.size + ' / ' : ''}${item.color || ''}</div>
        <div class="cart-item-price">${formatPrice(item.price)}</div>
        <div class="cart-item-actions">
          <button class="qty-btn" data-action="minus" data-id="${item.id}" data-size="${item.size}" data-color="${item.color}">−</button>
          <span class="cart-item-qty">${item.quantity}</span>
          <button class="qty-btn" data-action="plus" data-id="${item.id}" data-size="${item.size}" data-color="${item.color}">+</button>
          <button class="cart-item-remove" data-id="${item.id}" data-size="${item.size}" data-color="${item.color}">Remove</button>
        </div>
      </div>
    </div>
  `).join('');

  list.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = parseInt(btn.dataset.id);
      const size = btn.dataset.size;
      const color = btn.dataset.color;
      const isPlus = btn.dataset.action === 'plus';
      if (isPlus) {
        const p = products.find(x => x.id === id);
        await addToCart(id, p ? p.name : 'Item', p ? p.price : 0, 1, size, color);
      } else {
        await removeFromCart(id, size, color, 1);
      }
    });
  });
  list.querySelectorAll('.cart-item-remove').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = parseInt(btn.dataset.id);
      const size = btn.dataset.size;
      const color = btn.dataset.color;
      await removeFromCart(id, size, color, 999);
    });
  });

  const discRow = $('#discountRow');
  if (data.discount > 0) { discRow.style.display = 'flex'; $('#cartDiscount').textContent = '-' + formatPrice(data.discount); }
  else { discRow.style.display = 'none'; }
  $('#cartSubtotal').textContent = formatPrice(data.subtotal || 0);
  $('#cartTax').textContent = formatPrice(data.tax || 0);
  $('#cartTotal').textContent = formatPrice(data.grand_total || 0);
}

function toggleCart(open) {
  cartOpen = open !== undefined ? open : !cartOpen;
  $('#cartOverlay').classList.toggle('open', cartOpen);
  $('#cartSidebar').classList.toggle('open', cartOpen);
  document.body.style.overflow = cartOpen ? 'hidden' : '';
}

function toggleCheckout(open) {
  checkoutOpen = open !== undefined ? open : !checkoutOpen;
  $('#modalOverlay').classList.toggle('open', checkoutOpen);
  $('#checkoutModal').classList.toggle('open', checkoutOpen);
  document.body.style.overflow = checkoutOpen ? 'hidden' : (cartOpen ? 'hidden' : '');
  if (checkoutOpen) updateCheckoutSummary();
}

function updateCheckoutSummary() {
  const div = $('#orderSummaryMini');
  const total = $('#cartTotal').textContent;
  const subtotal = $('#cartSubtotal').textContent;
  const tax = $('#cartTax').textContent;
  div.innerHTML = `
    <div class="mini-row"><span>Subtotal</span><span>${subtotal}</span></div>
    <div class="mini-row"><span>Tax</span><span>${tax}</span></div>
    <div class="mini-row mini-total"><span>Total</span><span>${total}</span></div>
  `;
}

function filterCategory(cat) {
  currentCategory = cat;
  loadProducts(cat, $('#searchInput').value);
  $$('.nav-link').forEach(l => l.classList.toggle('active', l.dataset.category === cat));
}

function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// === Event Listeners ===
document.addEventListener('DOMContentLoaded', () => {
  loadProducts();
  loadCart();

  // Nav link clicks
  $$('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      filterCategory(link.dataset.category);
    });
  });

  // Category pills
  $$('.pill').forEach(pill => {
    pill.addEventListener('click', () => {
      $$('.pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      currentCategory = pill.dataset.category;
      loadProducts(currentCategory, $('#searchInput').value);
    });
  });

  // Search
  let searchTimer;
  $('#searchInput').addEventListener('input', () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      loadProducts(currentCategory, $('#searchInput').value);
    }, 300);
  });

  // Cart
  $('#cartBtn').addEventListener('click', () => toggleCart(true));
  $('#cartClose').addEventListener('click', () => toggleCart(false));
  $('#cartOverlay').addEventListener('click', () => toggleCart(false));

  // Checkout
  $('#checkoutBtn').addEventListener('click', () => {
    toggleCart(false);
    setTimeout(() => toggleCheckout(true), 300);
  });
  $('#modalClose').addEventListener('click', () => toggleCheckout(false));
  $('#modalOverlay').addEventListener('click', () => toggleCheckout(false));

  $('#checkoutForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = e.target.querySelector('.btn-place-order');
    btn.disabled = true;
    btn.textContent = 'Processing...';
    try {
      const totalText = $('#cartTotal').textContent;
      const subtotalText = $('#cartSubtotal').textContent;
      const taxText = $('#cartTax').textContent;
      await fetchAPI('/orders', {
        method: 'POST',
        body: {
          name: $('#customerName').value,
          email: $('#customerEmail').value,
          address: $('#customerAddress').value,
          total: parseFloat(totalText.replace('$', '')),
          tax: parseFloat(taxText.replace('$', '')),
          items: cartItems,
        },
      });
      showToast('Order placed successfully! Thank you for shopping at SHINNERS!');
      toggleCheckout(false);
      await clearCart();
      $('#cartCount').textContent = '0';
      $('#checkoutForm').reset();
    } catch (err) {
      showToast('Failed to place order: ' + err.message, 'error');
    }
    btn.disabled = false;
    btn.textContent = 'Place Order';
  });

  // Hamburger
  $('#hamburger').addEventListener('click', () => {
    $('#navLinks').classList.toggle('open');
  });

  // Close nav on link click (mobile)
  $$('.nav-link').forEach(l => l.addEventListener('click', () => {
    $('#navLinks').classList.remove('open');
  }));

  // Keyboard
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (checkoutOpen) toggleCheckout(false);
      else if (cartOpen) toggleCart(false);
    }
  });
});
