import booksdatasource
import unittest

booksdatasource = booksdatasource.BooksDataSource("test_books.csv", "test_authors.csv", "test_books_authors.csv")
#print(booksdatasource.authors())

authors_names_containing_ga = [{'id': 1, 'last_name': 'Christie', 'first_name': 'Agatha',
                               'birth_year': 1890, 'death_year': 1976},
                               {'id': 5, 'last_name': 'Gaiman', 'first_name': 'Neil',
                               'birth_year': 1960, 'death_year': None}]
print(booksdatasource.authors(search_text="ga"))
#print(booksdatasource.authors(book_id=0, search_text='Willis',start_year=1900, end_year=3000))

# print(booksdatasource.book(4))
# print(booksdatasource.author(4))
# print(booksdatasource.books(author_id=3))
# print(booksdatasource.authors(end_year=1900, sort_by="birth_year"))

# author_connie_willis = {'id': 0, 'last_name': 'Willis', 'first_name': 'Connie',
#                        'birth_year': 1945, 'death_year': None}

# print(book == author_connie_willis)

# class BooksDataSourceTest(unittest.TestCase):
#     def setUp(self):
#         self.booksdatasource = booksdatasource.BooksDataSource("test_books.csv", "test_authors.csv", "test_books_authors.csv")
#
#     def tearDown(self):
#         pass
#
#     def test_authors_all_args(self):
#         author_connie_willis = [{'id': 0, 'last_name': 'Willis', 'first_name': 'Connie', 'birth_year': 1945, 'death_year': None}]
#         self.assertEqual(self.booksdatasource.authors(book_id=0, search_text='Willis', start_year=1900, end_year=3000), author_connie_willis)
#
#     def test_books_all(self):
#         all_test_books = [{'id': 0, 'title': 'All Clear', 'publication_year': 2010},
#                      {'id': 1, 'title': 'And Then There Were None', 'publication_year': 1939},
#                      {'id': 2, 'title': 'Beloved', 'publication_year': 1987},
#                      {'id': 3, 'title': 'Blackout', 'publication_year': 2010},
#                      {'id': 4, 'title': 'Elmer Gantry', 'publication_year': 1927},
#                      {'id': 5, 'title': 'Emma', 'publication_year': 1815},
#                      {'id': 6, 'title': 'Good Omens', 'publication_year': 1990}]
#         self.assertEqual(self.booksdatasource.books(), all_test_books)

# if __name__ == '__main__':
#     print(booksdatasourceobject.books())
#     unittest.main()
