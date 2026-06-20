import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'shinners.db')

UNSPLASH = "https://images.unsplash.com/photo-{}?w=400&h=500&fit=crop&q=80"
PEXELS = "https://images.pexels.com/photos/{}/pexels-photo-{}.jpeg?auto=compress&cs=tinysrgb&w=400&h=500&fit=crop"

# 44 unique Unsplash IDs
U = [
    "1521572163474-6864f9cf17ab","1596755094514-f87e34085b2c","1490481651871-ab68de25d43d","1529139574466-a303027c1d8b",
    "1483985988355-763728e1935b","1554415707-6e8cfc93fe23","1576871337622-98d48d1cf531","1593030761757-71fae45fa0e7",
    "1539533113208-f6df8cc8b543","1490114538077-0a7f8cb49891","1551232864-3f0890e580d9","1591946614720-90a587da4a36",
    "1473966968600-fa801b869a1a","1541099649105-f69ad21f3246","1441984904996-e0b6ba687e04","1445205170230-053b83016050",
    "1441986300917-64674bd600d8","1469334031218-e382a71b716b","1595777457583-95e059d581b8","1542291026-7eec264c27ff",
    "1603487742131-4160ec999306","1549298916-b41d501d3772","1460353581641-37baddab0fa2","1606107557195-0e29a4b5b4aa",
    "1620799140408-edc6dcb6d633","1556821840-3a63f95609a7","1591195853828-11db59a44f6b","1506629082955-511b1aa562c8",
    "1564257631407-4deb1f99d992","1603252109303-2751441dd157","1417325384643-aac51acc9e5d","1479862863327-e4d9a0a83c3d",
    "1725610588086-b9e38da987f7","1515886657613-9f3515b0c78f","1558769132-cb1aea458c5e","1571513800374-df1bbe650e56",
    "1603189343302-e603f7add05a","1601762603339-fd61e28b698a","1574015974293-817f0ebebb74","1532453288672-3a27e9be9efd",
    "1596609548086-85bbf8ddb6b9","1578939662863-5cd416d45a69","1603400521630-9f2de124b33b","1443527216320-7e744084f5a7",
]

# 36 unique Pexels IDs
P = [
    11844304,6833756,7081105,5325695,6153353,5560194,7969812,5325774,5325639,6153355,
    5560195,7081104,6153374,6069964,19909750,833169,5236997,29538558,8018040,10203170,
    8126621,12655540,30512491,4510111,15327091,15927094,31839879,977909,1377451,6181979,
    27863598,28517485,1000373,2307879,3507016,7758138,
]

products = []

def make(name, desc, price, cat, img_url, sizes, colors):
    products.append({"name": name, "description": desc, "price": price, "category": cat, "image_url": img_url, "sizes": sizes, "colors": colors})

# 20 T-Shirts (Unsplash 1-20)
tshirt_names = [
    "Classic Cotton Tee","V-Neck Essential","Striped Casual Shirt","Premium Polo",
    "Oversized Fit Tee","Henley Neck Top","Crew Neck Basic","Muscle Fit Tee",
    "Pocket Detail Shirt","Retro Graphic Tee","Bamboo Fiber Tee","Longline Tee",
    "Oxford Button Down","Chambray Work Shirt","Flannel Check Shirt","Denim Shirt",
    "Linen Relaxed Shirt","Poplin Classic Shirt","Seersucker Summer Shirt","Military Shirt"
]
for i, name in enumerate(tshirt_names):
    make(name, f"Premium quality {name.lower()} in breathable fabrics for all-day comfort.", round(24.99 + (i+1) * 2.5, 2), "T-Shirts", UNSPLASH.format(U[i]), "S,M,L,XL", "Black,White,Navy,Gray")

# 20 Jackets (Unsplash 21-40)
jacket_names = [
    "Denim Jacket","Leather Biker Jacket","Bomber Jacket","Harrington Jacket",
    "Field Jacket","Parka Coat","Puffer Jacket","Trucker Jacket",
    "Varsity Letterman","Moto Racing Jacket","Blazer Sport Coat","Trench Coat",
    "Wool Peacoat","Windbreaker Shell","Fleece Zip-Up","Softshell Jacket",
    "Rain Hooded Jacket","Quilted Vest","Safari Jacket","Flight Bomber"
]
for i, name in enumerate(jacket_names):
    make(name, f"Stylish {name.lower()} crafted to keep you warm while making a bold fashion statement.", round(69.99 + (i+1) * 4.0, 2), "Jackets", UNSPLASH.format(U[i+20]), "S,M,L,XL", "Black,Brown,Navy,Olive")

# 20 Pants (Unsplash 41-44 + Pexels 1-16)
pant_names = [
    "Slim Fit Chinos","Straight Leg Trousers","Jogger Sweatpants","Cargo Pants",
    "Pleated Dress Pants","High-Waist Jeans","Bootcut Denim","Skinny Jeans",
    "Relaxed Fit Cords","Linen Drawstring Pants","Cropped Ankle Pants","Wide Leg Trousers",
    "Tapered Suit Pants","Utility Cargo","Paperbag Waist Pants","Palazzo Trousers",
    "Culotte Pants","Capri Leggings","Track Pants","Dress Slacks"
]
for i, name in enumerate(pant_names):
    if i < 4:
        img = UNSPLASH.format(U[i+40])
    else:
        img = PEXELS.format(P[i-4], P[i-4])
    make(name, f"Versatile {name.lower()} designed for the perfect fit from boardroom to weekend.", round(44.99 + (i+1) * 2.0, 2), "Pants", img, "30,32,34,36,38", "Black,Khaki,Navy,Gray")

# 20 Others (Pexels 17-36)
others = [
    ("Floral Summer Dress","Dresses",49.99,"Beautiful floral dress in premium fabric for a stunning silhouette."),
    ("Maxi Evening Gown","Dresses",89.99,"Elegant maxi gown designed for unforgettable evenings."),
    ("Shirt Dress Classic","Dresses",59.99,"Classic shirt dress that transitions from desk to dinner effortlessly."),
    ("Wrap Midi Dress","Dresses",69.99,"Flattering wrap midi dress that accentuates your curves."),
    ("Bodycon Mini Dress","Dresses",44.99,"Sleek bodycon mini dress for a night out on the town."),
    ("Leather Sneakers","Shoes",79.99,"Trendy leather sneakers engineered for style and comfort."),
    ("Loafers Casual","Shoes",69.99,"Classic loafers for a polished yet relaxed look."),
    ("Chelsea Boots","Shoes",99.99,"Premium Chelsea boots crafted from supple leather."),
    ("Platform Sandals","Shoes",59.99,"Chic platform sandals to elevate your summer style."),
    ("Stiletto Heels","Shoes",89.99,"Daring stiletto heels that command attention."),
    ("Cashmere Sweater","Sweaters",129.99,"Luxuriously soft cashmere sweater for warmth and elegance."),
    ("Graphic Hoodie","Sweaters",54.99,"Bold graphic hoodie for street-ready style."),
    ("Turtleneck Knit","Sweaters",69.99,"Classic turtleneck knit in a cozy blended fabric."),
    ("Cardigan Open Front","Sweaters",79.99,"Open front cardigan perfect for layering year-round."),
    ("Yoga Leggings","Activewear",44.99,"High-performance yoga leggings for your toughest workouts."),
    ("Athletic Shorts","Activewear",34.99,"Breathable athletic shorts for maximum mobility."),
    ("Sports Bra Top","Activewear",39.99,"Supportive sports bra top engineered for intense training."),
    ("Silk Blouse","Tops",69.99,"Luxurious silk blouse to elevate any outfit from desk to dinner."),
    ("Cropped Denim Top","Tops",39.99,"Trendy cropped denim top for a casual chic vibe."),
    ("Lace Cami Top","Tops",34.99,"Delicate lace cami top perfect for layering or solo."),
]
sizes_map = {"Shoes": "6,7,8,9,10,11,12"}
colors_map = {"Sweaters": "Charcoal,Cream,Burgundy,Navy", "Activewear": "Black,Navy,Pattern,Pink"}

for i, (name, cat, price, desc) in enumerate(others):
    pid = P[i+16]
    sz = sizes_map.get(cat, "S,M,L,XL")
    cl = colors_map.get(cat, "Black,White,Tan,Blue")
    make(name, desc, price, cat, PEXELS.format(pid, pid), sz, cl)

# 20 Men's Long Trousers (new Pexels IDs)
TROUSER_IMG = "https://images.pexels.com/photos/{}/pexels-photo-{}.jpeg?auto=compress&cs=tinysrgb&w=400&h=500&fit=crop"
trouser_photos = [
    10216931,6998103,6316245,10189122,7674841,7674833,7674825,7674817,
    7674809,7674801,7674793,7674785,15985071,12628461,5705679,9963299,
    7674769,7674761,7674753,7674745,
]
trouser_names = [
    "Slim Fit Tailored Trousers","Pleated Formal Trousers","Flat Front Chinos","Wool Dress Trousers",
    "Cuffed Smart Trousers","Stretch Comfort Trousers","Linen Blend Trousers","Corduroy Casual Trousers",
    "Cotton Twill Trousers","High-Waist Dress Trousers","Wide Leg Formal Trousers","Cropped Ankle Trousers",
    "Double Pleat Trousers","Tapered Fit Trousers","Pin Stripe Formal Trousers","Cargo Style Trousers",
    "Dock Style Chinos","Elastic Waist Trousers","Houndstooth Pattern Trousers","Classic Dress Trousers",
]
for i, name in enumerate(trouser_names):
    pid = trouser_photos[i]
    make(name, f"Premium {name.lower()} crafted from fine fabrics for a sharp, sophisticated look.", 39.99, "Trousers", TROUSER_IMG.format(pid, pid), "30,32,34,36,38", "Black,Navy,Gray,Khaki,Brown")

# 28 Books (real covers from Open Library by ISBN)
BOOK_IMG = "https://covers.openlibrary.org/b/ISBN/{}-L.jpg"
book_isbns = [
    "9780061122415","9780735211292","9781612680194","9780452267251",
    "9780735211292","9780132350884","9780062316110","9780135957059",
    "9780061122415","9781455586691","9781612680194","9781585424337",
    "9780857197689","9780804139298","9780307887894","9781455586691",
    "9780804139298","9780061122415","9780399590504","9780553380163",
    "9780061122415","9780735211292","9781612680194","9780132350884",
    "9780743273565","9780062316110","9781455586691","9781585424337",
]
book_prices = [20.00]*28
book_descs = [
    "A captivating story about following your dreams and listening to your heart.",
    "Transform your habits and transform your life with proven strategies.",
    "Learn the principles of wealth-building and financial independence.",
    "Timeless wisdom from the ancient city of Babylon on wealth creation.",
    "Write clean, maintainable code that stands the test of time.",
    "A brief history of humankind from the Stone Age to the modern age.",
    "Master the art of pragmatic software development and engineering.",
    "Stay laser-focused in a distracted world and produce meaningful work.",
    "The classic guide to building wealth through smart investing and mindset.",
    "Harness the power of your thoughts to achieve success and prosperity.",
    "Understand your relationship with money and make smarter financial decisions.",
    "How to build a successful startup from zero to one in the tech world.",
    "Build a lean, efficient startup that learns and adapts quickly.",
    "A powerful memoir about education, family, and finding your voice.",
    "Explore the mysteries of the universe from the Big Bang to black holes.",
    "The timeless American classic about love, wealth, and the American Dream.",
    "A thought-provoking journey through human history and evolution.",
    "A gripping dystopian novel about love, identity, and totalitarianism.",
    "The art of war applied to modern business and competitive strategy.",
    "Discover your 'why' and lead with purpose and inspiration.",
    "Master the subtle art of not giving up and finding real success.",
    "Break through limitations and achieve extraordinary results in life.",
    "A deep dive into how successful people think and make decisions.",
    "Unlock your creative potential and innovate like never before.",
    "Build meaningful relationships and master the art of connection.",
    "The definitive guide to building wealth and financial freedom.",
    "Think differently, act boldly, and change the world around you.",
    "A practical guide to living a life of purpose and fulfillment.",
]

for i, (title, author) in enumerate(zip(
    ["The Alchemist","Atomic Habits","Rich Dad Poor Dad","The Richest Man in Babylon",
     "Atomic Habits","Clean Code","Sapiens","The Pragmatic Programmer","The Alchemist",
     "Deep Work","Rich Dad Poor Dad","Think and Grow Rich","The Psychology of Money",
     "Zero to One","The Lean Startup","Deep Work","Zero to One","The Alchemist",
     "Educated","A Brief History of Time","The Alchemist","Atomic Habits",
     "Rich Dad Poor Dad","Clean Code","The Great Gatsby","Sapiens","Deep Work",
     "Think and Grow Rich"],
    ["Paulo Coelho","James Clear","Robert Kiyosaki","George S. Clason",
     "James Clear","Robert C. Martin","Yuval Noah Harari","Andrew Hunt & David Thomas",
     "Paulo Coelho","Cal Newport","Robert Kiyosaki","Napoleon Hill","Morgan Housel",
     "Peter Thiel","Eric Ries","Cal Newport","Peter Thiel","Paulo Coelho",
     "Tara Westover","Stephen Hawking","Paulo Coelho","James Clear",
     "Robert Kiyosaki","Robert C. Martin","F. Scott Fitzgerald","Yuval Noah Harari",
     "Cal Newport","Napoleon Hill"],
)):
    products.append({
        "name": title, "description": book_descs[i],
        "price": book_prices[i], "category": "Books",
        "image_url": BOOK_IMG.format(book_isbns[i]),
        "sizes": "", "colors": ""
    })

books_data = [(title, author) for title, author in zip(
    ["The Alchemist","Atomic Habits","Rich Dad Poor Dad","The Richest Man in Babylon",
     "Atomic Habits","Clean Code","Sapiens","The Pragmatic Programmer","The Alchemist",
     "Deep Work","Rich Dad Poor Dad","Think and Grow Rich","The Psychology of Money",
     "Zero to One","The Lean Startup","Deep Work","Zero to One","The Alchemist",
     "Educated","A Brief History of Time","The Alchemist","Atomic Habits",
     "Rich Dad Poor Dad","Clean Code","The Great Gatsby","Sapiens","Deep Work",
     "Think and Grow Rich"],
    ["Paulo Coelho","James Clear","Robert Kiyosaki","George S. Clason",
     "James Clear","Robert C. Martin","Yuval Noah Harari","Andrew Hunt & David Thomas",
     "Paulo Coelho","Cal Newport","Robert Kiyosaki","Napoleon Hill","Morgan Housel",
     "Peter Thiel","Eric Ries","Cal Newport","Peter Thiel","Paulo Coelho",
     "Tara Westover","Stephen Hawking","Paulo Coelho","James Clear",
     "Robert Kiyosaki","Robert C. Martin","F. Scott Fitzgerald","Yuval Noah Harari",
     "Cal Newport","Napoleon Hill"],
)]

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM products")
    cur.execute("DELETE FROM books")
    for p in products:
        cur.execute(
            "INSERT INTO products (name, description, price, category, image_url, sizes, colors) VALUES (?,?,?,?,?,?,?)",
            (p["name"], p["description"], p["price"], p["category"], p["image_url"], p["sizes"], p["colors"])
        )
    for title, author in books_data:
        cur.execute(
            "INSERT INTO books (title, author, price) VALUES (?,?,?)",
            (title, author, round(14.99, 2))
        )
    conn.commit()
    conn.close()
    print(f"Seeded {len(products)} products and {len(books_data)} books successfully!")

if __name__ == "__main__":
    seed()
