from os import path
from bs4 import BeautifulSoup
from app import settings
from url_generator import UrlGen

import html
import requests
import hashlib
import os
import errno
import random
import string
import re


def html_decode(func):
    """
    decorator to clean html strings
    :param func: function that returns html string
    :return: function that returns decoded html strings
    """
    def wrapper_func(*args, **kwargs):
        return html.unescape(html.unescape(func(*args, **kwargs)))

    return wrapper_func


class YahooAnswersHTMLParser:
    # TODO: FINISH THIS PARSING CLASS

    def __init__(self, file: str):

        self.file = open(file, 'r')
        self.soup = BeautifulSoup(self.file, 'html.parser')
        self.comments = {}
        self.comment_count = 0

    @html_decode
    def get_post_summary(self)->str:
        """
        :return: a string with the post title
        """
        return str(self.soup.title).split('>')[1].split('|')[0]

    def get_post_body(self):
        """
        :return: string with the post's question
        """
        for i in self.soup.find_all("meta"):
            if i.get("name") == "description":
                return html.unescape(html.unescape(i.get("content")))

        return None

    def get_post_id(self)->str:
        """
        :return: a string with the post id
        """
        return str(self.soup.find_all("script")[1]).split(',')[7].split('?')[-1].split('=')[-1]

    def get_post_user_id(self):
        """
        :return: returns the id of the user who wrote the post
        """
        for i in self.soup.find_all("img"):
            if i.get("data-id") is not None:
                return i.get("data-id")

        return None

    @html_decode
    def get_post_category(self)->str:
        """
        :return: a string with the main category of the post
        """
        for i in self.soup.find_all("meta"):
            if i.get("name") == "keywords":
                return i.get("content").split(',')[-2]

    @html_decode
    def get_post_subcat(self)->str:
        """
        :return: a string with the subcategory of the post
        """
        for i in self.soup.find_all("meta"):
            if i.get("name") == "keywords":
                return i.get("content").split(',')[-1]

    def post_has_best_anwser(self)->bool:
        """
        :return: returns true if the post has a best answer
        """
        return ">Best Answer:</span>" in str(self.soup.contents)

    def get_post_comments(self):
        """
        :return: a dictionary of dictionaries with all the comments info:

        dictionary structure:
        {
            1:{
                user_id: 1,
                body: body,
                id: id,
                askers_rating: rating,
                ...
            },
            2:{...
        }
        """

        file_contents = self.file.read()
        file_contents = file_contents.replace("/activity/questions?show=", "δδδ")

        for i in file_contents.split('δδδ'):

            # check to see if this is a comment
            if "span itemprop=\"text\" class=\"ya-q-full-text\"" in i:
                self.comments[self.comment_count] = {}

                # Check to see if the answer is the best answer
                self.comments[self.comment_count]["is_best_answer"] = self.is_best_comment(i)

                if self.is_best_comment():
                    self.comments[self.comment_count]["askers_rating"] = None  # TODO: FIX THIS
                else:
                    self.comments[self.comment_count]["askers_rating"] = None

                # Get the comment id
                self.comments[self.comment_count]["id"] = i.split('&')[0]

                # Get the user id
                self.comments[self.comment_count]["user_id"] = i.split('alt="')[1].split('"')

                # Get Upvotes
                div_split = i.split("div")
                for div in div_split:
                    if "itemprop=\"upvoteCount\"" in div:
                        self.comments[self.comment_count]["upvotes"] = int(div.split("count\">")[-1][0])
                        break

                # Get Downvotes


                # Get Body
                self.comments[self.comment_count]["body"] = self.get_comment_body(i)

    def is_best_comment(self, comment: str)->bool:
        """
        :param comment: comment to be tested on whether or not this is the best comment
        :return: true if the comment is the best
        """
        if "class=\"ya-ba-title Fw-b\">Best Answer:</', '>" in comment:
            return True

        else:
            return False

    def get_comment_askers_rating(self, comment: str)->int:
        """
        :param comment: the comment that is the best answer of the post
        :return: integer value out of 5 with the asker's rating
        """
        pass

    @html_decode
    def get_comment_body(self, comment: str)->str:
        """
        :param comment: the comment you want the body for
        :return: string with the comment's body
        """
        return re.sub('[<>/]', '', comment.split('span')[1].split('ya-q-full-text')[-1][1:])

    def __del__(self):
        self.file.close()
        del self.__dict__

