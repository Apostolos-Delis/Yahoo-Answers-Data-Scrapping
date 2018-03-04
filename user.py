from app.yahoo_answers_data_scrapping.yahoo_anwsers_db import schema, Model


class User(Model):
    """A single user"""

    __table__ = 'user'
    __primary_key__ = 'id'

    __visible__ = [
        "name"
    ]

    @staticmethod
    def create_table():
        """
        Creates Table in SQL DataBase with all the categories in __visible__ as columns
        All the columns will be of type str
        :return: SQL table
        """
        with schema.create(User.__table__) as table:
            table.string(User.__primary_key__)
            table.primary(User.__primary_key__)

        with schema.table(User.__table__) as table:

            for column in User.__visible__:
                table.string(column)

        return table
