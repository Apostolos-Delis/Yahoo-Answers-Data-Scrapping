from app.yahoo_answers_data_scrapping.html_cleaner import HtmlCleaner
from app.yahoo_answers_data_scrapping.url_generator import UrlGen

if __name__ == "__main__":

    category = "family & relationships"
    UrlGen.clear_file_directories()

    # Create the directories
    UrlGen.initialize(category)
    page_urls = UrlGen.get_page_urls()

    # Start generating page urls in urls.txt
    UrlGen.generate_page_url(page_urls[-1], 1)

    # save the post urls located in the html files of the pages
    UrlGen.save_post_urls(verbose=True)

    # Create files containing the text content of the post
    post_urls = UrlGen.get_post_urls()

    for post in post_urls:
        HtmlCleaner.save_post_html(post)

