from yahoo_anwsers_db import schema, Model


class Comment(Model):
    """A single comment"""

    __table__ = 'comment'
    __primary_key__ = 'id'

    __visible__ = [
        "qid",
        "user_id",
        "upvotes",
        "downvotes",
        "askers_rating",
        "is_best_answer",
        "body",
    ]

    @staticmethod
    def create_table():
        """
        Creates Table in SQL DataBase with all the categories in __visible__ as columns
        :return: SQL table
        """
        with schema.create(Comment.__table__) as table:
            table.string(Comment.__primary_key__)
            table.primary(Comment.__primary_key__)

        with schema.table(Comment.__table__) as table:

            for column in Comment.__visible__:

                if column == "upvotes" or column == "downvotes":
                    table.integer(column)

                if column == "askers_rating":
                    table.integer(column).nullable()

                elif column == "is_best_answer":
                    table.boolean(column)

                elif column == "user_id":
                    table.string(column)
                    table.foreign(column).references('id').on('user')

                elif column == "qid":
                    table.string(column)
                    table.foreign(column).references('qid').on('post')

                else:
                    table.string(column)

        return table
