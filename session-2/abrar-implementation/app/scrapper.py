import datetime
from requests_html import HTMLSession
from .database import SessionLocal
from .crud import createNews
from .schemas import NewsCreate
import cloudscraper
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session


#title,reporter,date, category, images

def scrape_article(url: str):
    scraper = cloudscraper.create_scraper()

    try:
        # Fetch the webpage content
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title_element = soup.find('h1', class_='text-3xl leading-10 text-[#3c3c3c] font-bold mb-3')
        title = title_element.text.strip() if title_element else "Title not found"

        # Extract the reporter
        reporter_element = soup.find('div', class_='text-xl text-[#292929] mb-2 lg:mb-2')
        reporter = reporter_element.text.strip() if reporter_element else "Reporter not found"

        # Extract the publication date
        date_element = soup.find('div', class_='text-sm lg:text-base text-[#333]')

        if date_element:
         raw_date = date_element.text.strip()
         date_parts = raw_date.split("প্রকাশ : ")[1].split(",")[0]
        
         try:
            news_datetime = datetime.datetime.strptime(date_parts, "%d %B %Y")
            print(f"Extracted date: {news_datetime.date()}")  # Print only the date
         except Exception as e:
            print(f"Date parsing error: {e}")
            news_datetime = datetime.datetime.now() 
        else:
         news_datetime = datetime.datetime.now() 
        print(f"Extracted date: {news_datetime.date()}") 
        # Extract the category
        category_element = soup.find('span')  # Adjust the logic if the span is nested or specific
        category = category_element.text.strip() if category_element else "Category not found"

        # Extract the content
        content_div = soup.find("div", class_="block-full_richtext")
        content = []
        if content_div:
         for element in content_div.descendants:
          if element.name == "p":  # Only process <p> tags
            content.append(element.get_text(strip=True))
        body = "\n".join(content)

        # Extract images
        img_elements = soup.find_all('img', class_='w-full h-auto')
        images = [img['src'] for img in img_elements if 'src' in img.attrs]

        # Publisher information
        publisher_website = url.split('/')[2]
        publisher = publisher_website.split('.')[-2]

        # Log scraped data (for debugging)
        print(f"Scraped news from {url}")
        print(f"Title: {title}")
        print(f"Reporter: {reporter}")
        print(f"Date: {news_datetime}")
        print(f"Category: {category}")
        print(f"Images: {images}")

        # Return NewsCreate object
        return NewsCreate(
            publisher_website=publisher_website,
            news_publisher=publisher,
            title=title,
            news_reporter=reporter,
            datetime=news_datetime,
            link=url,
            news_category=category,
            body=body,
            images=images,
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def scrape_and_store_news(url: str, db:Session):

    try:
        # Scrape news data
        news_data = scrape_article(url)  # Assuming scrape_article is your scraping function
        if not news_data:
            print(f"Failed to scrape data from URL: {url}")
            return None

        print(f"Scraped data: {news_data}")

        # Insert scraped news into the database
        inserted_news = createNews(db=db, news=news_data)
        print(f"Successfully inserted news into the database: {inserted_news}")
        
        return inserted_news

    except Exception as e:
        print(f"An error occurred during scraping or database operations: {e}")
        return None



# if __name__ == "__main__":
#     url = "https://dailyamardesh.com/world/amdak7gqqyski"  # Replace with your desired URL
#     result = scrape_article(url)
#     result2 = scrape_and_store_news(url) 
#     if result:
#         print(result)
#         print(result2)
#     else:
#         print("Failed to scrape the article.")


