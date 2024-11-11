import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import csv
from PIL import Image, ImageTk
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def save_to_pdf(product_name_value, details, price, about_item, img_data):
    pdf_filename = f"{product_name_value[:30]}.pdf"  # Limit filename length
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add product name
    story.append(Paragraph(product_name_value, styles['Title']))
    story.append(Spacer(1, 12))

    # Add price
    story.append(Paragraph(f"<b>Price:</b> {price}", styles['Normal']))
    story.append(Spacer(1, 6))

    # Add image
    if img_data:
        img = ReportLabImage(io.BytesIO(img_data), width=3*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 12))

    # Add details
    for detail_name, detail_value in details.items():
        story.append(Paragraph(f"<b>{detail_name}:</b> {detail_value}", styles['Normal']))
        story.append(Spacer(1, 6))

    # Add "About this item" list to PDF
    if about_item:
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>About this item:</b>", styles['Normal']))
        story.append(Spacer(1, 6))
        for item in about_item:
            story.append(Paragraph(f"• {item}", styles['Normal']))
            story.append(Spacer(1, 6))

    doc.build(story)
    return pdf_filename

def save_to_csv(product_name, details, price, about_item):
    filename = f"{product_name[:30]}.csv"  # Limit filename length
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Name', product_name])
        writer.writerow(['Price', price])  # Add price to CSV
        for detail_name, detail_value in details.items():
            writer.writerow([detail_name, detail_value])
        # Add "About this item" section to CSV
        about_item_str = " \u2022 ".join(about_item)
        writer.writerow(['About this item', about_item_str])
    return filename

def display_image(img_data):
    try:
        img = Image.open(io.BytesIO(img_data))
        img.thumbnail((200, 200))  # Resize image to fit in the GUI
        photo = ImageTk.PhotoImage(img)
        img_label.config(image=photo)
        img_label.image = photo  # Keep a reference
    except Exception as e:
        messagebox.showwarning("Warning", f"Failed to load image: {str(e)}")

def handle_error(message):
    messagebox.showerror("Error", message)

def fetch_product_details():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product name
        title_tag = soup.find(id='productTitle')
        product_name_value = title_tag.get_text(strip=True) if title_tag else 'Product name not found'

        img_tag = soup.find('img', id='landingImage')
        img_data = None

        if img_tag:
            img_url = img_tag['data-old-hires']
            img_response = requests.get(img_url)
            img_data = img_response.content
            display_image(img_data)
        else:
            messagebox.showwarning("Warning", "Could not find product image")

        # Extract price
        price_tag = soup.find('span', class_='a-price-whole')
        price_value = 'Price not found'
        if price_tag:
            whole_price = price_tag.get_text(strip=True)
            fraction_tag = soup.find('span', class_='a-price-fraction')
            if fraction_tag:
                fraction_price = fraction_tag.get_text(strip=True)
                price_value = f"£{whole_price}.{fraction_price}"
            else:
                price_value = f"£{whole_price}"

        # Extract "About this item"
        about_item = []
        about_section = soup.find(id='feature-bullets')
        if about_section:
            list_items = about_section.find_all('li', class_='a-spacing-mini')
            for li in list_items:
                about_item.append(li.get_text(strip=True))

        # Display the product name and price in the GUI
        product_name.set(f"{product_name_value} - {price_value}")
        details_text.delete(1.0, "end")  # Clear previous details
        details_text.insert("end", f"Price: {price_value}\n")

        # Extract additional details
        details = {}
        table = soup.find('table', class_='a-normal a-spacing-micro')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if len(columns) == 2:
                    detail_name = columns[0].get_text(strip=True)
                    detail_value = columns[1].get_text(strip=True)
                    details[detail_name] = detail_value

        # Add additional details to the display
        for detail_name, detail_value in details.items():
            details_text.insert("end", f"{detail_name}: {detail_value}\n")

        # Save the details to CSV, including price and "About this item"
        csv_filename = save_to_csv(product_name_value, details, price_value, about_item)
        messagebox.showinfo("Success", f"CSV saved as {csv_filename}")

        # Save the details to PDF, including price and "About this item"
        pdf_filename = save_to_pdf(product_name_value, details, price_value, about_item, img_data)
        messagebox.showinfo("Success", f"PDF saved as {pdf_filename}")

    except requests.exceptions.RequestException as e:
        handle_error(f"Failed to fetch the product page: {str(e)}")
    except Exception as e:
        handle_error(f"An unexpected error occurred: {str(e)}")

# GUI setup
root = tk.Tk()
root.title("Amazon Product Scraper")

# URL input
url_label = ttk.Label(root, text="Enter Amazon product URL:")
url_label.pack(pady=5)
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)

# Fetch button
fetch_button = ttk.Button(root, text="Fetch Product Details", command=fetch_product_details)
fetch_button.pack(pady=10)

# Product name display
product_name = tk.StringVar()
product_name_label = ttk.Label(root, textvariable=product_name, wraplength=400)
product_name_label.pack(pady=5)

# Image display
img_label = ttk.Label(root)
img_label.pack(pady=10)

# Details display
details_text = tk.Text(root, height=10, width=50)
details_text.pack(pady=10)

root.mainloop()
