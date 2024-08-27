import logging

def setup_logger(debug=False):
    """Nastavení základního loggeru."""
    logger = logging.getLogger("web_scraper_service")
    
    # Nastavení úrovně logování podle parametru debug
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    
    # Nastavení úrovně logování handleru podle parametru debug
    if debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    # Formátování logů včetně názvu souboru
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger

# Inicializace loggeru
logger = setup_logger(debug=True)  # Přepnutí na debug mód
