from snippet.lazy_dict import LazyDict, lazy_property
from nose import tools


class Book(LazyDict):
    def __init__(self, book_id):
        super(Book, self).__init__()
        self.id = book_id
        self.__subset__ = {'review'}

    @lazy_property
    def author(self):
        return self._get_author()

    def _get_author(self):
        # read file content from book_id.json
        info = {'author': 'author'}
        return info.get('author')

    @lazy_property
    def content(self):
        cmd = 'scp remote_host:/data/book/book_id.pdf /data/book/book_id/content.pdf'
        # run cmd
        return 'binary stream of /data/book/book_id/content.pdf'

    @lazy_property
    def review(self):
        return Review(self.id)


class Review(LazyDict):
    def __init__(self, book_id):
        super(Review, self).__init__()
        self.id = book_id

    @lazy_property
    def count(self):
        sql = 'select count(*) from db.review where book_id=self.id'
        # run sql
        return 10

    @lazy_property
    def latest(self):
        sql = 'select * from db.review where book_id=self.id order by time desc limit 1'
        # run sql
        return 'Latest review'


def test():
    book = Book('book1 id')
    tools.eq_(len(book.__dict__), 2, 'Book should have only 2 properties, id and _subset')
    author = book['author']
    tools.eq_(len(book.__dict__), 3, 'Book should have 1 more property, author')
    review = book.review
    tools.eq_(len(book.__dict__), 4, 'Book should have 1 more property, review')
    tools.eq_(len(book.review.__dict__), 2, 'Review should have only 2 properties, id and _subset')
    latest = book.review.latest
    tools.eq_(len(book.review.__dict__), 3, 'Review should have 1 more property, review')
    structure = book._get_structure()
    tools.eq_(len(structure), 4, 'Structure should have 4 properties.')
    tools.eq_(structure['id'], None, 'Structure should have id with no value.')
    # structure should not have _subset
    tools.assert_raises(KeyError, structure.__getitem__, '__subset__')
    data = book._to_dict()
    tools.eq_(len(data), 4, 'Data should have 4 properties.')
    tools.eq_(data['review']['count'], 10, 'Data should have actual data.')