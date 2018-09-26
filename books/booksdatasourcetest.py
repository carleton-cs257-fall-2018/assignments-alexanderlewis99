'''
   booksdatasourcetest.py
   Alec Wang, 21 September 2018
   Bat-Orgil Batjargal
'''

import booksdatasource
import unittest

class BooksDataSourceTest(unittest.TestCase):
    def setUp(self):
        self.booksdatasource = booksdatasource.BooksDataSource("test_books.csv", "test_authors.csv", "test_books_authors.csv")

    def tearDown(self):
        pass

	# book() function tests
    def test_book_positive(self):
        book_all_clear = {'id': 0, 'title': 'All Clear', 'publication_year': 2010}
        self.assertEqual(self.booksdatasource.book(0), book_all_clear)

    def test_book_error_invalid_id(self):
        self.assertRaises(ValueError, self.booksdatasource.book, 1000)

    def test_book_error_decimal_id(self):
        self.assertRaises(TypeError, self.booksdatasource.book, 3.14159265358979323846)

    def test_book_error_negative_id(self):
        self.assertRaises(TypeError, self.booksdatasource.book, -1)

    def test_book_error_string_id(self):
        self.assertRaises(TypeError, self.booksdatasource.book, "pancakes")

    def test_book_error_boolean_id(self):
        self.assertRaises(TypeError, self.booksdatasource.book, False)

    # books() function tests
    def test_books_all(self):
        all_test_books = [{'id': 0, 'title': 'All Clear', 'publication_year': 2010},
                     {'id': 1, 'title': 'And Then There Were None', 'publication_year': 1939},
                     {'id': 2, 'title': 'Beloved', 'publication_year': 1987},
                     {'id': 3, 'title': 'Blackout', 'publication_year': 2010},
                     {'id': 4, 'title': 'Elmer Gantry', 'publication_year': 1927},
                     {'id': 5, 'title': 'Emma', 'publication_year': 1815},
                     {'id': 6, 'title': 'Good Omens', 'publication_year': 1990}]
        self.assertEqual(self.booksdatasource.books(), all_test_books)

    def test_books_author_id(self):
        elmer_gantry_book = {'id': 4, 'title': 'Elmer Gantry', 'publication_year': 1927}
        self.assertEqual(self.booksdatasource.books(author_id=3), elmer_gantry_book)

    def test_books_search_text(self):
        good_omens_book = {'id': 6, 'title': 'Good Omens', 'publication_year': 1990}
        self.assertEqual(self.booksdatasource.books(search_text="oMenS"), good_omens_book)

    def test_books_start_year(self):
        books_start_year_1990 = [{'id': 0, 'title': 'All Clear', 'publication_year': 2010},
                                 {'id': 3, 'title': 'Blackout', 'publication_year': 2010},
                                 {'id': 6, 'title': 'Good Omens', 'publication_year': 1990}]
        self.assertEqual(self.booksdatasource.books(start_year=1990), books_start_year_1990)

    def test_books_end_year(self):
        books_end_year_1987 = [{'id': 1, 'title': 'And Then There Were None', 'publication_year': 1939},
                               {'id': 2, 'title': 'Beloved', 'publication_year': 1987},
                               {'id': 4, 'title': 'Elmer Gantry', 'publication_year': 1927},
                               {'id': 5, 'title': 'Emma', 'publication_year': 1815}]
        self.assertEqual(self.booksdatasource.books(end_year=1987), books_end_year_1987)

    def test_books_all_args(self):
        beloved_book = {'id': 2, 'title': 'Beloved', 'publication_year': 1987}
        self.assertEqual(self.booksdatasource.books(author_id=2, search_text='lOVe', start_year=1980, end_year=2000), beloved_book)

    def test_books_sort_by_year(self):
        books_sorted_by_year = [{'id': 5, 'title': 'Emma', 'publication_year': 1815},
                                {'id': 4, 'title': 'Elmer Gantry', 'publication_year': 1927},
                                {'id': 1, 'title': 'And Then There Were None', 'publication_year': 1939},
                                {'id': 2, 'title': 'Beloved', 'publication_year': 1987},
                                {'id': 6, 'title': 'Good Omens', 'publication_year': 1990},
                                {'id': 0, 'title': 'All Clear', 'publication_year': 2010},
                                {'id': 3, 'title': 'Blackout', 'publication_year': 2010}]
        self.assertEqual(self.booksdatasource.books(sort_by='year'), books_sorted_by_year)

    def test_books_invalid_author_id(self):
        self.assertRaises(ValueError, self.booksdatasource.books, author_id=1000)

    def test_books_invalid_search_text(self):
        self.assertRaises(ValueError, self.booksdatasource.books, search_text='The Shining')

    def test_books_invalid_start_year(self):
        self.assertRaises(ValueError, self.booksdatasource.books, start_year=3000)

    def test_books_invalid_end_year(self):
        self.assertRaises(ValueError, self.booksdatasource.books, end_year=0)

    def test_books_invalid_start_year_end_year(self):
        self.assertRaises(ValueError, self.booksdatasource.books, start_year=2000, end_year=1800)

    def test_books_error_correct_id_invalid_start_year(self):
        self.assertRaises(ValueError, self.booksdatasource.books, author_id=3, start_year=3000)

    def test_books_error_sort_by(self):
        self.assertRaises(ValueError, self.booksdatasource.books, sort_by='pancakes')

    # author() function tests
    def test_author(self):
        author_jane_austen = {'id': 4, 'last_name': 'Austen', 'first_name': 'Jane', 'birth_year': 1775, 'death_year': 1817}
        self.assertEqual(self.booksdatasource.author(4), author_jane_austen)

    def test_author_error_invalid_id(self):
        self.assertRaises(ValueError, self.booksdatasource.author, 1000)

    def test_author_error_decimal_id(self):
        self.assertRaises(TypeError, self.booksdatasource.author, 3.14159265358979323846)

    def test_author_error_negative_id(self):
        self.assertRaises(TypeError, self.booksdatasource.author, -1)

    def test_author_error_string_id(self):
        self.assertRaises(TypeError, self.booksdatasource.author, "pancakes")

    def test_author_error_boolean_id(self):
        self.assertRaises(TypeError, self.booksdatasource.author, False)

    # authors() function tests
    def test_authors_all(self):
        authors = [{'id': 4, 'last_name': 'Austen', 'first_name': 'Jane',
                    'birth_year': 1775, 'death_year': 1817},
                    {'id': 3, 'last_name': 'Lewis', 'first_name': 'Sinclair',
                    'birth_year': 1885, 'death_year': None},
                    {'id': 1, 'last_name': 'Christie', 'first_name': 'Agatha',
                    'birth_year': 1890, 'death_year': 1976},
                    {'id': 2, 'last_name': 'Morrison', 'first_name': 'Toni',
                    'birth_year': 1931, 'death_year': None},
                    {'id': 0, 'last_name': 'Willis', 'first_name': 'Connie',
                    'birth_year': 1945, 'death_year': None},
                    {'id': 6, 'last_name': 'Pratchett', 'first_name': 'Terry',
                    'birth_year': 1948, 'death_year': 2015},
                    {'id': 5, 'last_name': 'Gaiman', 'first_name': 'Neil',
                    'birth_year': 1960, 'death_year': None}]
        self.assertEqual(self.booksdatasource.authors(), authors)

    def test_authors_book_id(self):
        author_toni_morrison = {'id': 2, 'last_name': 'Morrison', 'first_name': 'Toni',
                                'birth_year': 1931, 'death_year': None}
        self.assertEqual(self.booksdatasource.authors(book_id=2), author_toni_morrison)

    def test_authors_book_id_multiple_authors(self):
        authors_good_omen = [{'id': 6, 'last_name': 'Pratchett', 'first_name': 'Terry',
                             'birth_year': 1948, 'death_year': 2015},
                             {'id': 5, 'last_name': 'Gaiman', 'first_name': 'Neil',
                             'birth_year': 1960, 'death_year': None}]
        self.assertEqual(self.booksdatasource.authors(book_id=6), authors_good_omen)

    def test_authors_search_text(self):
        authors_names_containing_ga = [{'id': 1, 'last_name': 'Christie', 'first_name': 'Agatha',
                                       'birth_year': 1890, 'death_year': 1976},
                                       {'id': 5, 'last_name': 'Gaiman', 'first_name': 'Neil',
                                       'birth_year': 1960, 'death_year': None}]
        self.assertEqual(self.booksdatasource.authors(search_text="ga"), authors_names_containing_ga)

    def test_authors_start_year(self):
        authors_since_1950 = [{'id': 0, 'last_name': 'Willis', 'first_name': 'Connie',
                              'birth_year': 1945, 'death_year': None},
                              {'id': 1, 'last_name': 'Christie', 'first_name': 'Agatha',
                              'birth_year': 1890, 'death_year': 1976},
                              {'id': 2, 'last_name': 'Morrison', 'first_name': 'Toni',
                              'birth_year': 1931, 'death_year': None},
                              {'id': 3, 'last_name': 'Lewis', 'first_name': 'Sinclair',
                              'birth_year': 1885, 'death_year': None},
                              {'id': 5, 'last_name': 'Gaiman', 'first_name': 'Neil',
                              'birth_year': 1960, 'death_year': None},
                              {'id': 6, 'last_name': 'Pratchett', 'first_name': 'Terry',
                              'birth_year': 1948, 'death_year': 2015}]
        self.assertEqual(self.booksdatasource.authors(start_year=1950), authors_since_1950)

    def test_authors_start_year_only_living_authors(self):
        authors_living = [{'id': 0, 'last_name': 'Willis', 'first_name': 'Connie',
                          'birth_year': 1945, 'death_year': None},
                          {'id': 2, 'last_name': 'Morrison', 'first_name': 'Toni',
                          'birth_year': 1931, 'death_year': None},
                          {'id': 3, 'last_name': 'Lewis', 'first_name': 'Sinclair',
                          'birth_year': 1885, 'death_year': None},
                          {'id': 5, 'last_name': 'Gaiman', 'first_name': 'Neil',
                          'birth_year': 1960, 'death_year': None}]
        self.assertEqual(self.booksdatasource.authors(start_year=2016), authors_living)

    def test_authors_end_year(self):
        authors_before_1900 = [{'id': 4, 'last_name': 'Austen', 'first_name': 'Jane',
                                'birth_year': 1775, 'death_year': 1817},
                                {'id': 3, 'last_name': 'Lewis', 'first_name': 'Sinclair',
                                'birth_year': 1885, 'death_year': None},
                                {'id': 1, 'last_name': 'Christie', 'first_name': 'Agatha',
                                'birth_year': 1890, 'death_year': 1976}]
        self.assertEqual(self.booksdatasource.authors(end_year=1900), authors_before_1900)

    def test_authors_all_args(self):
        author_connie_willis = {'id': 0, 'last_name': 'Willis', 'first_name': 'Connie',
                               'birth_year': 1945, 'death_year': None}
        self.assertEqual(self.booksdatasource.authors(book_id=0, search_text='Willis',
                                                       start_year=1900, end_year=3000),
                                                       author_connie_willis)

    def test_authors_sort_by_last_name(self):
        authors_sorted_by_last_name = [{'id': 4, 'last_name': 'Austen', 'first_name': 'Jane',
                                        'birth_year': 1775, 'death_year': 1817},
                                        {'id': 1, 'last_name': 'Christie', 'first_name': 'Agatha',
                                        'birth_year': 1890, 'death_year': 1976},
                                        {'id': 5, 'last_name': 'Gaiman', 'first_name': 'Neil',
                                        'birth_year': 1960, 'death_year': None},
                                        {'id': 3, 'last_name': 'Lewis', 'first_name': 'Sinclair',
                                       'birth_year': 1885, 'death_year': None},
                                       {'id': 2, 'last_name': 'Morrison', 'first_name': 'Toni',
                                       'birth_year': 1931, 'death_year': None},
                                       {'id': 6, 'last_name': 'Pratchett', 'first_name': 'Terry',
                                       'birth_year': 1948, 'death_year': 2015},
                                       {'id': 0, 'last_name': 'Willis', 'first_name': 'Connie',
                                       'birth_year': 1945, 'death_year': None}]
        self.assertEqual(self.booksdatasource.authors(sort_by='last_name'),authors_sorted_by_last_name)

    def test_authors_invalid_book_id(self):
        self.assertRaises(ValueError, self.booksdatasource.authors, book_id=3000)


    def test_authors_error_sort_by(self):
        self.assertRaises(ValueError, self.booksdatasource.authors, sort_by='pancakes')

    def test_authors_error_start_year_end_year(self):
        self.assertRaises(ValueError, self.booksdatasource.authors, start_year=3000, end_year=2000)

    def test_authors_error_correct_id_incorrect_start_year(self):
        self.assertRaises(ValueError, self.booksdatasource.authors, book_id = 5, start_year=3000)


if __name__ == '__main__':
    unittest.main()
