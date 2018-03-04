import requests
from os import path
import hashlib
import shutil
from bs4 import BeautifulSoup

# Make that you add your own settings file...
from  "Something..." import settings
import os
import errno


class UrlGen:
    #The settings.DATA_STORE_PATH will have to be modified on a user to user basis
    BASE_DIRECTORY = path.join(settings.DATA_STORE_PATH, "yahoo_scrapes")
    HTML_DIRECTORY = path.join(BASE_DIRECTORY, "html_files")
    URL_FILE = path.join(BASE_DIRECTORY, "urls.txt")
    MANIFEST = path.join(BASE_DIRECTORY, "manifest.txt")
    POST_DIRECTORY = path.join(BASE_DIRECTORY, "post_files")
    POST_URL_FILE = path.join(BASE_DIRECTORY, "post_urls.txt")
    POST_MANIFEST = path.join(BASE_DIRECTORY, "post_manifest.txt")

    YAHOO_CATEGORIES = {

        "family & relationships": "https://answers.yahoo.com/dir/index?sid=396545433",
        "health": "https://answers.yahoo.com/dir/index?sid=396545018",
        "society & culture": "https://answers.yahoo.com/dir/index?sid=396545454",
        "education & reference": "https://answers.yahoo.com/dir/index?sid=396545015",
        "social science": "https://answers.yahoo.com/dir/index?sid=396545301",
        "food & drink": "https://answers.yahoo.com/dir/index?sid=396545367",
        "business & finance": "https://answers.yahoo.com/dir/index?sid=396545013",
        "computers & internet": "https://answers.yahoo.com/dir/index?sid=396545660"

    }

    @staticmethod
    def initialize(yahoo_anwsers_category):
        """
        Initializes all the files and directories,
        should be called before any other functions in this class
        """

        UrlGen.make_directory(UrlGen.BASE_DIRECTORY)
        UrlGen.make_directory(UrlGen.HTML_DIRECTORY)
        UrlGen.make_directory(UrlGen.POST_DIRECTORY)

        # create the url file and put the base url in
        url_file = open(UrlGen.URL_FILE, 'w+')
        url_file.write(UrlGen.YAHOO_CATEGORIES[yahoo_anwsers_category.lower()])
        url_file.close()

        # create the manifest that will contain a list of all the html files
        manifest = open(UrlGen.MANIFEST, "w+")
        manifest.close()

        post_url_file = open(UrlGen.POST_URL_FILE, "w+")
        post_url_file.close()

        post_manifest = open(UrlGen.POST_MANIFEST, "w+")
        post_manifest.close()

    @staticmethod
    def clear_file_directories():
        shutil.rmtree(UrlGen.BASE_DIRECTORY)

    @staticmethod
    def generate_page_url(seed, number_of_urls, breakpoint=100):
        """
        Recursive function that generates new yahoo answers urls and puts them into
        the text file urls.txt
        :param number_of_urls: number of urls that have been generated so far
        :param seed: base url that will start off the loop and increment urls from there
        :param breakpoint: Number of urls that will be processed before program terminates
        """
        if number_of_urls == breakpoint:
            print("Url Batch Processed")
        else:
            try:
                r = requests.get(seed)
                if r.status_code == 200:  # make sure that the connection is correct

                    new_url = "https://answers.yahoo.com/_module?name=YANewDiscoverTabModule&sid=" + \
                              r.json()["YANewDiscoverTabModule"]["options"]["sid"] + "&bpos=" + \
                              str(r.json()["YANewDiscoverTabModule"]["options"]["bpos"]) + "&cpos=" + \
                              str(r.json()["YANewDiscoverTabModule"]["options"]["cpos"]) + "&after=" +\
                              str(r.json()["YANewDiscoverTabModule"]["options"]["after"])
                    print("New Url Generated:", new_url)

                    UrlGen.save_page_url(new_url, number_of_urls, r.json())
                    number_of_urls += 1
                    UrlGen.generate_page_url(new_url, number_of_urls, breakpoint=breakpoint)

                else:
                    UrlGen.connection_exception(1)

            except Exception:
                with Exception as e:
                    print("Terminating URL Gen with exception:", e)
                    exit(code=2)

    @staticmethod
    def connection_exception(code):
        """Terminates Program"""
        print("Failed to connect to Url correctly.\nProgram Terminating...")
        exit(code=code)

    @staticmethod
    def save_page_url(url, url_number, url_json):
        """
        :param url: the url that wants to be saved
        :param url_number: total urls generated
        :param url_json: the html information found by requests in dictionary format
        """

        # Put the new url into urls.txt
        url_file = open(UrlGen.URL_FILE, 'a')
        url_file.write('\n' + url)
        url_file.close()

        # Put the previous urls data into a new text file
        url_data_path = UrlGen.create_path(url_number)
        print(url_data_path)
        url_data_file = open(url_data_path, 'w+')
        url_data_file.write(url_json["YANewDiscoverTabModule"]["html"])
        url_data_file.close()
        print("Html file number", url_number, "created.")

    @staticmethod
    def make_directory(file_path):
        """
        Creates the directory at the path:
        :param file_path: the path of the directory that you want ot create
        """
        if file_path == "\\":  # Don't even ask how this is possible
            return 0
        try:
            os.makedirs(file_path, exist_ok=True)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(file_path):
                pass
            else:
                print("Error while attempting to create a directory.")
                exit(3)

    @staticmethod
    def create_path(number_of_urls):
        """
        Create a file path for a txt file containing a page's html
        :param number_of_urls: the actual file name will initially be n.txt where n is the number of urls
        :return: return the actual complete url string path and the appropriate directories will be created
        """

        unencrypted_text = str(number_of_urls) + ".txt"
        encrypted_text = hashlib.md5(unencrypted_text.encode('ascii')).hexdigest()
        new_url = '/'.join(encrypted_text[i:i+2] for i in range(0, len(encrypted_text), 2))

        temp_path = new_url.split("/")[0]
        UrlGen.make_directory(path.join(UrlGen.HTML_DIRECTORY, temp_path))

        for i in new_url.split("/")[1:-1]:
            temp_path += "/" + i
            UrlGen.make_directory(path.join(UrlGen.HTML_DIRECTORY, temp_path))

        final_path = path.join(UrlGen.HTML_DIRECTORY,  new_url + ".txt")

        # Store the file path into index_directory for later use
        manifest = open(UrlGen.MANIFEST, 'a+')
        manifest.write(new_url + ".txt" + '\n')
        manifest.close()

        return final_path

    @staticmethod
    def save_post_urls(verbose=False):
        """
        Cycle through and save all the post urls found within all the page html files
        :param: verbose: whether or not the user should be notified on the progress
        """

        def save_post_url(file):
            """
            Using one of the page html files, find all the post_urls within and save them
            :param verbose: whether or not the user should be notified on the progress
            :param file: The html file that contains a page of Yahoo answers posts
            """

            html_doc = open(file, 'r')
            soup = BeautifulSoup(html_doc, 'html.parser')
            html_doc.close()
            question_number = 0
            posts_file = open(UrlGen.POST_URL_FILE, 'a')

            if verbose:
                print("Gathering post urls from file:", file)

            for link in soup.find_all('a'):
                if "question" in link.get("href"):

                    question_number += 1
                    posts_file.write("https://answers.yahoo.com" + link.get("href") + '\n')

                    if verbose:
                        print("Question number", question_number, "Added to database")

            if verbose:
                print("All potential urls from the current file saved")
            posts_file.close()

        files = UrlGen.get_page_html_files()

        for f in files:
            f = path.join(UrlGen.HTML_DIRECTORY, f)
            save_post_url(f)

        if verbose:
            print("Processing complete.\nAll post urls saved in post file")

    @staticmethod
    def get_page_html_files():
        """
        :return: list of files containing page htmls
        """
        file = open(UrlGen.MANIFEST, "r")
        urls = file.read().split("\n")
        return urls[:-1]

    @staticmethod
    def get_page_urls():
        """
        :return: list of page urls
        """
        file = open(UrlGen.URL_FILE, "r")
        urls = file.read().split("\n")
        return urls

    @staticmethod
    def get_post_urls():
        """
        :return: list of post urls
        """
        file = open(UrlGen.POST_URL_FILE, "r")
        urls = file.read().split("\n")
        return urls[:-1]
