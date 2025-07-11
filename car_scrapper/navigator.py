"""
Navigateur web pour le scraping
"""

import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from .models import PageInfo


class AlbiNavigator:
    """
    Navigateur pour Albi.ca
    """
    def __init__(self):
        self.base_url = "https://www.albioccasion.com"
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.goto(self.base_url)
        # Attendre que la page soit complètement chargée
        self.page.wait_for_load_state("networkidle")
        # Attendre un peu plus pour s'assurer que tous les scripts sont exécutés
        self.page.wait_for_timeout(3000)

    def get_inventory_url(self, page_number: int):
        return f"{self.base_url}/fr/inventaire/?page={page_number}"
        
    def get_html(self):
        return self.page.content()
    
    def get_page_infos(self) -> PageInfo:
        """
        Récupère les informations de pagination
        """
        try:
            # Attendre que la page soit complètement chargée
            self.page.wait_for_load_state("networkidle")
            
            # Attendre que l'élément de pagination soit visible
            self.page.wait_for_selector(".InventoryPaging > .pagination-container", timeout=10000)
            
            # Récupérer le HTML de la pagination (utiliser le premier élément)
            pagination_html = self.page.locator(".InventoryPaging > .pagination-container").first.inner_html()
            
            # Parser le HTML avec BeautifulSoup
            soup = BeautifulSoup(pagination_html, "html.parser")
            
            # Extraire la page courante
            current_page_element = soup.find("span", {"id": "cph_ContainerLarger_pgr_Lower_ctl00_CurrentPageLabel"})
            current_page = int(current_page_element.text) if current_page_element else 1
            
            # Extraire le nombre total de pages
            total_pages_element = soup.find("span", {"id": "cph_ContainerLarger_pgr_Lower_ctl00_TotalPagesLabel"})
            total_pages = int(total_pages_element.text) if total_pages_element else 1
        
            return PageInfo(
                current_page=current_page,
                total_pages=total_pages,
            )
            
        except Exception as e:
            print(f"Erreur lors de la récupération des informations de pagination: {e}")
            return PageInfo(current_page=1, total_pages=1)
    
    def go_to_page(self, page_url: str):
        # Aller à la page suivante
        current_url = self.page.url
        self.page.goto(page_url)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000) 