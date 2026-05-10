# 🏪 Hoko Collectables

> **Your premier destination for rare and unique collectables.**  
> Discover authentic figures, trading cards, vintage toys, anime merchandise, comics, and sports memorabilia — all hand-verified by our expert team.

---

## ✨ Features

- **Product Catalogue** — 32 curated items across 6 categories with badges (New, Hot, Rare, Sale)
- **Shopping Cart** — Add, remove, and update quantities with real-time subtotal; persisted in `localStorage`
- **Wishlist** — Save favourites with heart toggle; persisted in `localStorage`
- **Category Filtering** — Filter by Figures, Cards, Vintage, Anime, Comics, or Sports
- **Sort Options** — Sort by Featured, Price (low → high / high → low), Newest, or Top Rated
- **Live Search** — Instant search across product names and categories
- **Load More Pagination** — Reveal products in batches of 8
- **Countdown Timer** — Persistent session-based offer timer on the bundle banner
- **Scroll-Reveal Animations** — Intersection Observer-based fade-in as you scroll
- **Hero Parallax** — Subtle mousemove parallax on the hero cards
- **Newsletter & Contact Forms** — With toast confirmation feedback
- **Responsive Design** — Mobile-first layout supporting all screen sizes

---

## 📁 Project Structure

```
hoko-collectables/
├── index.html     # Full single-page website structure
├── style.css      # Dark-theme design system (CSS custom properties)
├── app.js         # All dynamic behaviour — products, cart, search, animations
└── README.md      # This file
```

---

## 🛍️ Product Categories

| Category       | Items | Examples                                      |
|----------------|-------|-----------------------------------------------|
| Action Figures | 6     | Goku Ultra Instinct, Optimus Prime, Darth Vader |
| Trading Cards  | 6     | Pokémon Charizard 1st Ed, Magic Black Lotus   |
| Vintage Toys   | 5     | 1977 Millennium Falcon, G1 Grimlock           |
| Anime & Manga  | 5     | Demon Slayer Nendoroid, Eva Unit-01 MG        |
| Comics & Art   | 4     | Amazing Fantasy #15, Batman Year One Signed   |
| Sports         | 6     | Jordan 1986 Fleer RC, LeBron Signed Jersey    |

---

## 🚀 Getting Started

Since this is a static site, simply open `index.html` in any modern browser — no build step required.

```bash
# Clone the repository
git clone https://github.com/ethanryan28-cmd/hoko-collectables.git
cd hoko-collectables

# Open directly in your browser
open index.html        # macOS
xdg-open index.html   # Linux
start index.html       # Windows
```

Or use any static file server:

```bash
# Using Python
python -m http.server 8000

# Using Node (npx)
npx serve .
```

---

## 🎨 Design System

The site uses CSS custom properties for a consistent dark theme:

| Token            | Value      | Usage                          |
|------------------|------------|--------------------------------|
| `--primary`      | `#c0392b`  | Buttons, accents, badges       |
| `--dark`         | `#1a1a2e`  | Page background                |
| `--card-bg`      | `#1e2240`  | Product and category cards     |
| `--font-serif`   | Playfair Display | Headings                 |
| `--font-sans`    | Inter      | Body text and UI               |

---

## 📋 Roadmap

- [ ] Product detail modal / page
- [ ] User account & order history
- [ ] Checkout flow & payment integration
- [ ] Backend API + database (product management)
- [ ] Admin dashboard for inventory
- [ ] Advanced filtering (price range, rating threshold)
- [ ] Product image uploads (replacing emoji placeholders)
- [ ] SEO meta tags & Open Graph

---

## 📄 License

© 2026 Hoko Collectables. All rights reserved.
