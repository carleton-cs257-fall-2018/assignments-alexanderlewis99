#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 18 September 2018

    For use in some assignments at the beginning of Carleton's
    CS 257 Software Design class, Fall 2018.
'''

import csv
import sys

class BooksDataSource:
    '''
    A BooksDataSource object provides access to data about books and authors.
    The particular form in which the books and authors are stored will
    depend on the context (i.e. on the particular assignment you're
    working on at the time).

    Most of this class's methods return Python lists, dictionaries, or
    strings representing books, authors, and related information.

    An author is represented as a dictionary with the keys
    'id', 'last_name', 'first_name', 'birth_year', and 'death_year'.
    For example, Jane Austen would be represented like this
    (assuming her database-internal ID number is 72):

        {'id': 72, 'last_name': 'Austen', 'first_name': 'Jane',
         'birth_year': 1775, 'death_year': 1817}

    For a living author, the death_year is represented in the author's
    Python dictionary as None.

        {'id': 77, 'last_name': 'Murakami', 'first_name': 'Haruki',
         'birth_year': 1949, 'death_year': None}

    Note that this is a simple-minded representation of a person in
    several ways. For example, how do you represent the birth year
    of Sophocles? What is the last name of Gabriel García Márquez?
    Should we refer to the author of "Tom Sawyer" as Samuel Clemens or
    Mark Twain? Are Voltaire and Molière first names or last names? etc.

    A book is represented as a dictionary with the keys 'id', 'title',
    and 'publication_year'. For example, "Pride and Prejudice"
    (assuming an ID of 132) would look like this:

        {'id': 193, 'title': 'A Wild Sheep Chase', 'publication_year': 1982}

    '''

    def __init__(self, books_filename, authors_filename, books_authors_link_filename):
        ''' Initializes this data source from the three specified  CSV files, whose
            CSV fields are:

                books: ID,title,publication-year
                  e.g. 6,Good Omens,1990
                       41,Middlemarch,1871


                authors: ID,last-name,first-name,birth-year,death-year
                  e.g. 5,Gaiman,Neil,1960,NULL
                       6,Pratchett,Terry,1948,2015
                       22,Eliot,George,1819,1880

                link between books and authors: book_id,author_id
                  e.g. 41,22
                       6,5
                       6,6

                  [that is, book 41 was written by author 22, while book 6
                    was written by both author 5 and author 6]

            Note that NULL is used to represent a non-existent (or rather, future and
            unknown) year in the cases of living authors.

            NOTE TO STUDENTS: I have not specified how you will store the books/authors
            data in a BooksDataSource object. That will be up to you, in Phase 3.
        '''
        self.books_data = []
        self.authors_data = []
        self.maps = []

        books_file = open(books_filename, 'r')
        authors_file = open(authors_filename, 'r')
        books_authors_file = open(books_authors_link_filename, 'r')

        books_reader = csv.reader(books_file)
        authors_reader = csv.reader(authors_file)
        books_authors_reader = csv.reader(books_authors_file)

        for book_line in books_reader:
            book_id = int(book_line[0])
            book_title = book_line[1]
            book_publication_year = int(book_line[2])
            book = {'id': book_id, 'title': book_title, 'publication_year': book_publication_year}
            self.books_data.append(book)
        for author_line in authors_reader:
            author_id = int(author_line[0])
            author_last_name = author_line[1]
            author_first_name = author_line[2]
            author_birth_year = int(author_line[3])
            author_death_year = author_line[4]
            if (author_death_year == 'NULL'):
                author_death_year = None
            else:
                author_death_year = int(author_death_year)
            author = {'id': author_id, 'last_name': author_last_name, 'first_name': author_first_name,
                      'birth_year': author_birth_year, 'death_year': author_death_year}
            self.authors_data.append(author)
        for line in books_authors_reader:
            book_id = int(line[0])
            author_id = int(line[1])
            dic_book_author = {'book_id':book_id, 'author_id':author_id}
            self.maps.append(dic_book_author)

    def book(self, book_id):
        ''' Returns the book with the specified ID. (See the BooksDataSource comment
            for a description of how a book is represented.)

            Raises ValueError if book_id is not a valid book ID.
        '''
        if not (type(book_id) == int and book_id >= 0):
            raise TypeError('Invalid type for book ID.')

        book_to_return = None
        for book in self.books_data:
            if book['id'] == book_id:
                book_to_return = book
        if book_to_return == None:
            raise ValueError('Not a valid book ID:', book_id)
        return book_to_return

    def books(self, *, author_id=None, search_text=None, start_year=None, end_year=None, sort_by='title'):
        ''' Returns a list of all the books in this data source matching all of
            the specified non-None criteria.

                author_id - only returns books by the specified author
                search_text - only returns books whose titles contain (case-insensitively) the search text
                start_year - only returns books published during or after this year
                end_year - only returns books published during or before this year

            Note that parameters with value None do not affect the list of books returned.
            Thus, for example, calling books() with no parameters will return JSON for
            a list of all the books in the data source.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                default -- sorts by (case-insensitive) title, breaking ties with publication_year

            See the BooksDataSource comment for a description of how a book is represented.

            QUESTION: Should Python interfaces specify TypeError?
            Raises TypeError if author_id, start_year, or end_year is non-None but not an integer.
            Raises TypeError if search_text or sort_by is non-None, but not a string.

            QUESTION: How about ValueError? And if so, for which parameters?
            Raises ValueError if author_id is non-None but is not a valid author ID.
        '''
        books_matching_search_query = []
        for book in self.books_data:
            books_matching_search_query.append(book)

        #argument errors

        if(not(author_id is None or (type(author_id)==int and author_id >= 0))
        or not(search_text is None or type(search_text)==str)
        or not(start_year is None or type(start_year)==int)
        or not(end_year is None or type(end_year)==int)):
            raise TypeError('Invalid parameter types')

        if not author_id is None:
            author_ids = []
            for author in self.authors_data:
                author_ids.append(author['id'])
            if not author_id in author_ids:
                raise ValueError("Invalid author_id")

        if not start_year is None and not end_year is None:
            if (start_year > end_year):
                raise ValueError("Invalid start_year and end_year")

        if not sort_by is None and not sort_by.lower() in ('title', 'year'):
            raise ValueError("Invalid sorting method")

        #method begins

        books_matching_search_query = []
        for book_author_pair in self.maps:
            if (book_author_pair['book_id'] = book_id):
                books_matching_search_query.append(author(author_id))

        copy_books_matching_search_query = []
        for i in books_matching_search_query:
            copy_books_matching_search_query.append(i)


        for book in copy_books_matching_search_query:
            book_removed = False
            if not book_removed and not search_text == None:
                if search_text.lower() not in book['title'].lower():
                    books_matching_search_query.remove(book)
                    book_removed = True
            if not book_removed and not start_year == None:
                if book['publication_year'] < start_year:
                    books_matching_search_query.remove(book)
                    book_removed = True
            if not book_removed and not end_year == None:
                if book['publication_year'] > end_year:
                    books_matching_search_query.remove(book)

        if len(books_matching_search_query) == 0:
            raise ValueError('No books found.')
        elif len(books_matching_search_query) == 1:
            books_matching_search_query = books_matching_search_query[0]
        else:
            if sort_by == 'title':
                books_matching_search_query = sorted(books_matching_search_query, key=lambda k: k['title'])
            else:
                books_matching_search_query = sorted(books_matching_search_query, key=lambda k: k['publication_year'])
        return books_matching_search_query

    def author(self, author_id):
        ''' Returns the author with the specified ID. (See the BooksDataSource comment for a
            description of how an author is represented.)

            Raises ValueError if author_id is not a valid author ID.
        '''
        if not (type(author_id) == int and author_id >= 0):
            raise TypeError('Invalid type for author ID.')

        author_to_return = None
        for author in self.authors_data:
            if author['id'] == author_id:
                author_to_return = author
        if author_to_return == None:
            raise ValueError('Not a valid author ID:', author_id)
        return author_to_return

    def authors(self, *, book_id=None, search_text=None, start_year=None, end_year=None, sort_by='birth_year'):
        ''' Returns a list of all the authors in this data source matching all of the
            specified non-None criteria.

                book_id - only returns authors of the specified book
                search_text - only returns authors whose first or last names contain
                    (case-insensitively) the search text
                start_year - only returns authors who were alive during or after
                    the specified year
                end_year - only returns authors who were alive during or before
                    the specified year

            Note that parameters with value None do not affect the list of authors returned.
            Thus, for example, calling authors() with no parameters will return JSON for
            a list of all the authors in the data source.

            The list of authors is sorted in an order depending on the sort_by parameter:

                'birth_year' - sorts by birth_year, breaking ties with (case-insenstive) last_name,
                    then (case-insensitive) first_name
                any other value - sorts by (case-insensitive) last_name, breaking ties with
                    (case-insensitive) first_name, then birth_year

            See the BooksDataSource comment for a description of how an author is represented.
        '''
        authors_matching_search_query = []
        for author in self.authors_data:
            authors_matching_search_query.append(author)

        #checking arguments
        if(not(book_id is None or (type(book_id)==int and book_id >= 0))
        or not(search_text is None or type(search_text)==str)
        or not(start_year is None or type(start_year)==int)
        or not(end_year is None or type(end_year)==int)):
            raise TypeError('Invalid parameter types')

        if not book_id is None:
            book_ids = []
            for book in self.books_data:
                book_ids.append(book['id'])
            if not book_id in book_ids:
                raise ValueError("Invalid book_id")

        if not start_year is None and not end_year is None:
            if (start_year > end_year):
                raise ValueError("Invalid start_year and end_year")

        if not sort_by is None and not sort_by.lower() in ('birth_year', 'last_name'):
            raise ValueError("Invalid sorting method")


        #method begins
        author_ids_removed = []
        author_ids_kept = []
        if not book_id == None:
            for book_author_pair in self.maps:
                author_id_of_selected_pair = book_author_pair['author_id']
                book_id_of_selected_pair = book_author_pair['book_id']
                if (not author_id_of_selected_pair in author_ids_kept
                and not author_id_of_selected_pair in author_ids_removed
                and not book_id_of_selected_pair == book_id):
                    authors_matching_search_query.remove(self.author(author_id_of_selected_pair))
                    author_ids_removed.append(author_id_of_selected_pair)
                else:
                    author_ids_kept.append(author_id_of_selected_pair)

        copy_authors_matching_search_query = []
        for i in authors_matching_search_query:
            copy_authors_matching_search_query.append(i)

        for author in copy_authors_matching_search_query:
            author_removed = False
            if not author_removed and not search_text == None:
                if not (search_text.lower() in author['first_name'].lower(), author['last_name'].lower()):
                    authors_matching_search_query.remove(author)
                    print(author['last_name'], "search_text")
                    author_removed = True
            if not author_removed and not start_year == None:
                if not author['death_year'] is None and author['death_year'] < start_year:
                    authors_matching_search_query.remove(author)
                    print(author['last_name'], "start_year")
                    author_removed = True
            if not author_removed and not end_year == None:
                if author['birth_year'] > end_year:
                    authors_matching_search_query.remove(author)
                    print(author['last_name'], "end_year")
        if len(authors_matching_search_query) == 0:
            raise ValueError('No authors found.')
        elif len(authors_matching_search_query) == 1:
            authors_matching_search_query = authors_matching_search_query[0]
        else:
            if sort_by == 'birth_year':
                authors_matching_search_query = sorted(authors_matching_search_query, key=lambda k: k['birth_year'])
            else:
                authors_matching_search_query = sorted(authors_matching_search_query, key=lambda k: k['last_name'])
        return authors_matching_search_query


    # Note for my students: The following two methods provide no new functionality beyond
    # what the books(...) and authors(...) methods already provide. But they do represent a
    # category of methods known as "convenience methods". That is, they provide very simple
    # interfaces for a couple very common operations.
    #
    # A question for you: do you think it's worth creating and then maintaining these
    # particular convenience methods? Is books_for_author(17) better than books(author_id=17)?

    def books_for_author(self, author_id):
        ''' Returns a list of all the books written by the author with the specified author ID.
            See the BooksDataSource comment for a description of how an book is represented. '''
        return self.books(author_id=author_id)

    def authors_for_book(self, book_id):
        ''' Returns a list of all the authors of the book with the specified book ID.
            See the BooksDataSource comment for a description of how an author is represented. '''
        return self.authors(book_id=book_id)
