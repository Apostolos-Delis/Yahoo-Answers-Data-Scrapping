from app.yahoo_answers_data_scrapping.post import Post
from app.yahoo_answers_data_scrapping.user import User
from app.yahoo_answers_data_scrapping.comment import Comment

"""Create the 3 tables within the Yahoo Answers Database"""""
User.create_table()
Post.create_table()
Comment.create_table()

