import requests
from bs4 import BeautifulSoup

def extract_blog_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        if not content:
            article = soup.find('article')
            if article:
                paragraphs = article.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        return content if content else "No content found."
    except Exception as e:
        return f"Error: {str(e)}"