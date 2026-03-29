class BasePage:
    def __init__(self, page):
        self.page = page
    # Navigation   
    def navigate(self, url):
        self.page.goto(url)
    #Generic click, fill, get_text, is_visible, wait_for_selector methods    
    def click(self, selector):
        self.page.click(selector)
        
    def fill(self, selector, text):
        self.page.fill(selector, text)  
        
    def get_text(self, selector):
        return self.page.text_content(selector)
    
    def is_visible(self, selector):
        return self.page.is_visible(selector)
    
    def wait_for_selector(self, selector):
        self.page.locator(selector).wait_for()