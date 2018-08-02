from src.app import db


class BaseModel(object):
    """Generalize __init__, __repr__ and to_json based on the models columns.
    """

    def __repr__(self):
        """Define a base way to print models. Columns inside `print_filter`
        are excluded.
        """
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
            if column not in self.print_filter
        })

    def update(self):
        db.session.commit()
        return self

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True
