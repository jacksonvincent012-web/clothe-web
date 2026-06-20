# SHINNERS - Premium Fashion Store

A full-stack e-commerce web application for fashion clothing, books, and accessories.

## Tech Stack

- **Backend**: Python (Flask) + Java (Cart microservice)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Database**: SQLite
- **Images**: Unsplash, Pexels, Open Library

## Features

- Product catalog with categories (T-Shirts, Jackets, Pants, Shoes, Dresses, Sweaters, Activewear, Tops, Trousers, Books)
- Shopping cart with quantity management
- Checkout with order placement
- Search and filter by category
- Responsive design

## Quick Start

1. Install Python dependencies:
   ```
   pip install flask flask-cors requests
   ```

2. Start the Flask server:
   ```
   cd shinners/backend-python
   python app.py
   ```

3. Open http://localhost:5000 in your browser.

The database is auto-created and seeded on first run.

## Project Structure

```
shinners/
  backend-python/    Flask API (products, orders, books)
  backend-java/      Java cart microservice
  database/          SQLite schema and seed data
  frontend/
    index.html       Main page
    css/style.css    Styles
    js/app.js        Client logic
```
