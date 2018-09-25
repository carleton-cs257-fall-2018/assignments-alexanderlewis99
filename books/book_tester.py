import booksdatasource
booksdatasource = booksdatasource.BooksDataSource("test_books.csv", "test_authors.csv", "test_books_authors.csv")
print(booksdatasource.books)
print(booksdatasource.authors)
print(booksdatasource.maps)
print(booksdatasource.book(4))
print(booksdatasource.author(4))
print(booksdatasource.books(author_id=3))
print(booksdatasource.authors(end_year=1900))
