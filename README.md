# tkmaxx Product Scraper and GUI Tool

This project demonstrates a Python-based web scraper that extracts detailed product information from tkmaxx.com product pages. The data is displayed in a simple graphical user interface (GUI) and saved in a structured CSV and PDF file, which can be used for eCommerce platforms like WooCommerce.

## Features

- **Scrape tkmaxx Product Pages**: Extract key product details such as:
  - Product Name
  - Brand
  - Price
  - Description
- **User-Friendly GUI**: Built using Tkinter, the GUI allows users to input an tkmaxx product URL, fetch product details, and view the extracted information.
- **CSV Export**: Saves the extracted data in a CSV file, making it easy to store, process, or import into eCommerce platforms.
- **Error Handling**: Robust error handling ensures smooth execution, even in the case of malformed URLs or connection issues.

## Technologies Used

- **Python**: The main programming language for the project.
- **BeautifulSoup**: Web scraping library to parse and extract product data from tkmaxx product pages.
- **Tkinter**: Python library for creating the graphical user interface.
- **CSV**: For saving extracted product data in a CSV format.
- **ReportLab**: For saving extracted product data in a PDF format.
- **Pyinstaller**: For building a script as an executable.