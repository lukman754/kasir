import streamlit as st
import pandas as pd
import io
from PIL import Image, ImageDraw, ImageFont

# Data produk
products = [
    {'id': 1, 'name': 'Es Teh', 'price': 5000},
    {'id': 2, 'name': 'Es Jeruk', 'price': 6000},
    {'id': 3, 'name': 'Jus Mangga', 'price': 12000},
    {'id': 4, 'name': 'Jus Alpukat', 'price': 15000},
    {'id': 5, 'name': 'Soda Gembira', 'price': 7000},
]

# Simpan keranjang belanja dalam session_state
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Fungsi untuk menambahkan produk ke keranjang
def add_to_cart(product_id, quantity):
    product = next(p for p in products if p['id'] == product_id)
    # Cek jika produk sudah ada di keranjang, update jumlahnya
    for item in st.session_state.cart:
        if item['product']['id'] == product_id:
            item['quantity'] += quantity
            return
    # Jika produk belum ada, tambahkan ke keranjang
    st.session_state.cart.append({'product': product, 'quantity': quantity})

# Fungsi untuk menghapus produk dari keranjang
def remove_from_cart(product_id):
    st.session_state.cart = [item for item in st.session_state.cart if item['product']['id'] != product_id]

# Fungsi untuk menghitung total harga
def calculate_total():
    return sum(item['product']['price'] * item['quantity'] for item in st.session_state.cart)

# Fungsi untuk mencetak struk menjadi gambar
def print_receipt():
    total = calculate_total()
    img = Image.new('RGB', (400, 300), color='white')
    d = ImageDraw.Draw(img)

    # Menggunakan font default
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    y_position = 20
    d.text((10, y_position), "Toko Minuman XYZ", font=font, fill=(0, 0, 0))
    y_position += 30
    d.text((10, y_position), "-----------------------------", font=font, fill=(0, 0, 0))
    y_position += 20

    # Tampilkan produk di keranjang
    for item in st.session_state.cart:
        product_name = item['product']['name']
        quantity = item['quantity']
        price = item['product']['price']
        total_price = price * quantity
        d.text((10, y_position), f"{product_name} x{quantity}: {total_price} IDR", font=font, fill=(0, 0, 0))
        y_position += 20

    y_position += 20
    d.text((10, y_position), "-----------------------------", font=font, fill=(0, 0, 0))
    y_position += 20
    d.text((10, y_position), f"Total: {total} IDR", font=font, fill=(0, 0, 0))
    
    # Simpan gambar dan tampilkan
    img_path = "/tmp/receipt.png"
    img.save(img_path)
    return img_path

# Menampilkan produk dan menambahkan ke keranjang
st.title("Kasir Toko Minuman")

# Tampilkan daftar produk
st.subheader("Pilih Produk")
for product in products:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(product['name'])
    with col2:
        quantity = st.number_input(f"Jumlah {product['name']}", min_value=1, max_value=10, key=product['id'])
        if st.button(f"Tambahkan {product['name']}", key=f"add_{product['id']}"):
            add_to_cart(product['id'], quantity)

# Menampilkan keranjang belanja
st.subheader("Keranjang Belanja")
for item in st.session_state.cart:
    product = item['product']
    quantity = item['quantity']
    st.write(f"{product['name']} x{quantity} = {product['price'] * quantity} IDR")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(f"Hapus {product['name']}", key=f"remove_{product['id']}"):
            remove_from_cart(product['id'])

# Total harga dan kembalian
st.subheader("Total Belanja")
total = calculate_total()
st.write(f"Total: {total} IDR")

amount_paid = st.number_input("Jumlah Uang yang Dibayar", min_value=0, max_value=1000000, step=1000)
change = amount_paid - total
st.write(f"Kembalian: {change} IDR")

# Tombol untuk mencetak struk
if st.button("Print Struk"):
    receipt_image_path = print_receipt()
    img = Image.open(receipt_image_path)
    st.image(img, caption="Struk Pembelian", use_column_width=True)
