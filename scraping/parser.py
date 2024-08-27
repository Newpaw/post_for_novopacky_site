from bs4 import BeautifulSoup

def parse_html(html_content):
    """Funkce pro extrakci dat z HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extrakce specifických dat z <div id="web-header">
    web_header_div = soup.find('div', id='web-header')
    web_header_text = ""
    
    if web_header_div:
        # Získání textu z <h1> a <h2>
        h1 = web_header_div.find('h1')
        h2 = web_header_div.find('h2')
        
        if h1:
            web_header_text += h1.get_text(strip=True) + "\n\n"
        if h2:
            web_header_text += h2.get_text(strip=True) + "\n\n"
        
        # Můžete přidat další extrakce, pokud potřebujete další informace z web_header_div

    # Extrakce specifických dat z <div id="content-blocks">
    content_blocks_div = soup.find('div', id='content-blocks')
    content_blocks_text = ""
    
    if content_blocks_div:
        # Získání textu ze všech <p> elementů
        paragraphs = content_blocks_div.find_all('p')
        
        for p in paragraphs:
            content_blocks_text += p.get_text(strip=True) + "\n\n"
    
    # Spojení extrahovaných textů
    extracted_data = web_header_text + content_blocks_text

    return extracted_data
