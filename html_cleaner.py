from os import path
from bs4 import BeautifulSoup
from app import settings
from app.yahoo_answers_data_scrapping.url_generator import UrlGen
from app.yahoo_answers_data_scrapping.html_parsing import YahooAnswersHTMLParser

import requests
import hashlib
import os
import errno
import random
import html
import string
import re


class HtmlCleaner:

    @staticmethod
    def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def save_post_html(url:str, verbose=False):
        """
        Saves the post's html file into the post directory
        :param verbose: if you want the user to be notified when a file has been saved
        :param url: url that will be scrapped
        """
        r = requests.get(url=url)
        if r.status_code == 200:

            file_name = path.join(UrlGen.POST_DIRECTORY, HtmlCleaner.id_generator(10) + ".txt")
            url_data_file = open(file_name, 'w+')
            url_data_file.write(r.text)
            url_data_file.close()

            post_manifest = open(UrlGen.POST_MANIFEST, "a")
            post_manifest.write(file_name + '\n')
            post_manifest.close()

            if verbose:
                print("post from url:", url, "saved...")

        else:
            UrlGen.connection_exception(1)

    @staticmethod
    def parse_html_file(file, verbose=False):

        html_doc = open(file, 'r')

        file_contents = str(html_doc.read())
        file_contents = file_contents.replace("/activity/questions?show=", "δ")
        # print(file_contents)
        print(file_contents.split("δ"))
        count = 0
        for i in file_contents.split('δ'):

            if "span itemprop=\"text\" class=\"ya-q-full-text\"" in i:
                print("\n=============================================================================================================================================================")
                count += 1
                print(i.split('alt="')[1].split('"'))

        print(count)
        soup = BeautifulSoup(html_doc, 'html.parser')
        # html_doc.close()

        if verbose:
            print("Gathering post urls from file:", file)

        j = 0
        for i in soup.find_all("a"):
            j += 1
            if j <= 400:

                print("===========================================================================================", j)
                print(i.get("ite"))
                # print(i.get("content").split(',')[-2])

                print(i)

        print(html_doc.read())

    @staticmethod
    def test_html_parser(file: str):
        """
        Tests all the various functions in the html parser class to see if they are compatible with the html file
        :param file: html file that will be used to test the parser
        :return: TODO: see if we need a return
        """
        parser = YahooAnswersHTMLParser(file)

        print("===========================================================================================")
        print("Beginning html parseing test....")
        print("\n===========================================================================================")
        print("Post id:          ", parser.get_post_id())
        print("\n===========================================================================================")
        print("Summary:            ", parser.get_post_summary())
        print("\n===========================================================================================")
        print("Post user id:     ", parser.get_post_user_id())
        print("\n===========================================================================================")
        print("Post Category:    ", parser.get_post_category())
        print("\n===========================================================================================")
        print("Post Subcat:      ", parser.get_post_subcat())
        print("\n===========================================================================================")
        print("Has best answer:  ", parser.post_has_best_anwser())
        print("\n===========================================================================================")
        print("Body   :          ", parser.get_post_body())



if __name__ == "__main__":
    html_file = path.join(UrlGen.POST_DIRECTORY, "HPJOORAIRI.txt")
    soup = BeautifulSoup(open(html_file), "html.parser")
    HtmlCleaner.parse_html_file(html_file)
    # HtmlCleaner.test_html_parser(html_file)

"""
Comment: Best Anwser

<a href="/activity/questions?show=CSX7CIVTXO6QMJSPVEZGZKJQOI&amp;t=g" class="Clr-b">
    <img data-id="CSX7CIVTXO6QMJSPVEZGZKJQOI" class="profileImage Wpx-45 Hpx-45 Bdrs-25 Bdx-1g" src="https://s.yimg.com/dg/users/1EDN-2GwnAAECHKJplCXqRM4WKG4F.medium.jpg" alt="Ranchmom1"/>
</a>
    </div>
    <div class="Mstart-75 Pos-r">
        <div class="Fw-n">
            <span class="Hpx-15 Wpx-14 D-ib shared-sprite win-best-answer-icon-14"></span>
            <span class="ya-ba-title Fw-b">Best Answer:</span>&nbsp;
            <span itemprop="text" class="ya-q-full-text"> My husband and I have different interests too. He does his thing and I do mine. No big deal. </span>
        </div>


<a href="/activity/questions?show=NS5MP6Z3UTWNXCFVHGBIIFYJW4&amp;t=g" class="Clr-b">
    <img data-id="NS5MP6Z3UTWNXCFVHGBIIFYJW4" class="profileImage Wpx-45 Hpx-45 Bdrs-25 Bdx-1g" src="https://s.yimg.com/wm/modern/images/default_user_profile_pic_96.png" alt="Froll"/>
</a>
    </div>
    <div class="Mstart-75  Pos-r">
        <div class="answer-detail Fw-n">
            <span itemprop="text" class="ya-q-full-text"> Just a quick correction. Work cannot become &quot;stagnate&quot; since &quot;stagnate&quot; is a verb. His work became &quot;stagnant&quot;.</span>
        </div>

        

"""