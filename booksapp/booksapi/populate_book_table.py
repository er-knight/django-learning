# following code needs `DJANGO_SETTINGS_MODULE` variable defined

from datetime import date

from django.utils import timezone

from models import Book, Author

b = Book(title="The Great Gatsby", author=Author.objects.get(name__exact="John Smith"), publication_date=date(2022, 5, 20), price=29.99); b.save();
b = Book(title="Pride and Prejudice", author=Author.objects.get(name__exact="Jane Doe"), publication_date=date(2021, 8, 10), price=24.99); b.save();
b = Book(title="The Catcher in the Rye", author=Author.objects.get(name__exact="Michael Johnson"), publication_date=date(2023, 2, 15), price=19.99); b.save();
b = Book(title="To Kill a Mockingbird", author=Author.objects.get(name__exact="Emily Thompson"), publication_date=date(2020, 10, 5), price=27.99); b.save();
b = Book(title="1984", author=Author.objects.get(name__exact="David Wilson"), publication_date=date(2024, 3, 8), price=32.99); b.save();
b = Book(title="The Hobbit", author=Author.objects.get(name__exact="Sophia Davis"), publication_date=date(2022, 7, 12), price=22.99); b.save();
b = Book(title="The Lord of the Rings", author=Author.objects.get(name__exact="Robert Anderson"), publication_date=date(2021, 4, 30), price=39.99); b.save();
b = Book(title="Harry Potter and the Sorcerer's Stone", author=Author.objects.get(name__exact="Olivia Martinez"), publication_date=date(2023, 11, 25), price=28.99); b.save();
b = Book(title="The Great Expectations", author=Author.objects.get(name__exact="James Harris"), publication_date=date(2022, 6, 18), price=26.99); b.save();
b = Book(title="Romeo and Juliet", author=Author.objects.get(name__exact="Isabella Young"), publication_date=date(2023, 1, 7), price=23.99); b.save();
b = Book(title="To the Lighthouse", author=Author.objects.get(name__exact="John Smith"), publication_date=date(2021, 9, 14), price=21.99); b.save();
b = Book(title="Jane Eyre", author=Author.objects.get(name__exact="Jane Doe"), publication_date=date(2024, 5, 28), price=25.99); b.save();
b = Book(title="The Adventures of Huckleberry Finn", author=Author.objects.get(name__exact="Michael Johnson"), publication_date=date(2022, 2, 9), price=17.99); b.save();
b = Book(title="The War and Peace", author=Author.objects.get(name__exact="Emily Thompson"), publication_date=date(2023, 10, 2), price=33.99); b.save();
b = Book(title="Animal Farm", author=Author.objects.get(name__exact="David Wilson"), publication_date=date(2021, 7, 16), price=20.99); b.save();
b = Book(title="The Alchemist", author=Author.objects.get(name__exact="Sophia Davis"), publication_date=date(2024, 4, 21), price=29.99); b.save();
b = Book(title="Crime and Punishment", author=Author.objects.get(name__exact="Robert Anderson"), publication_date=date(2022, 11, 10), price=31.99); b.save();
b = Book(title="The Chronicles of Narnia", author=Author.objects.get(name__exact="Olivia Martinez"), publication_date=date(2021, 8, 6), price=26.99); b.save();
b = Book(title="The Odyssey", author=Author.objects.get(name__exact="James Harris"), publication_date=date(2023, 3, 19), price=24.99); b.save();
b = Book(title="Wuthering Heights", author=Author.objects.get(name__exact="Isabella Young"), publication_date=date(2022, 12, 12), price=27.99); b.save();


















