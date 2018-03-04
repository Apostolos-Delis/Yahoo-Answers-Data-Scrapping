from yahoo_anwsers_db import schema, Model


class Post(Model):
    """A single post"""

    __table__ = 'Post'
    __primary_key__ = 'qid'

    __visible__ = [
        "user_id",
        "category",
        "subcat",
        "has_best_answer",
        "timestamps",
        "summary",
        "body",
    ]

    @staticmethod
    def create_table():
        """
        Creates Table in SQL DataBase with all the categories in __visible__ as columns
        All the columns will be of type str except has_best_answer which is boolean
        :return: SQL table
        """
        with schema.create(Post.__table__) as table:
            table.string(Post.__primary_key__)
            table.primary(Post.__primary_key__)

        with schema.table(Post.__table__) as table:

            for column in Post.__visible__:

                if column == "has_best_answer":
                    table.boolean(column)

                elif column == "user_id":
                    table.string(column).nullable()
                    table.foreign('user_id').references('id').on('user')

                elif column == "body":
                    table.string(column).nullable()

                else:
                    table.string(column)

        return table
