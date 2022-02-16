from bs4 import BeautifulSoup
import requests
import csv


# get html
url = "https://www.amazon.com/Best-Sellers-Books/zgbs/books"

# change the user-agent value based on your web browser
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

# get all books
books = soup.find_all(id="gridItemRoot")

csv_headers = ['Rank', 'Title', 'Author', 'Price']
with open('amazon_books.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)


for book in books:

    rank = book.find('span', class_='zg-bdg-text').text[1:]

    children = book.find('div', class_='zg-grid-general-faceout').div

    title = children.contents[1].text
    author = children.contents[2].text
    price = children.contents[-1].text
   
    with open('amazon_books.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([rank, title, author, price])
