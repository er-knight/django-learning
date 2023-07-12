# following code needs `DJANGO_SETTINGS_MODULE` variable defined

from datetime import date

from django.utils import timezone

from models import Author

a = Author(name="Olivia Martinez", birth_date=date(1989, 6, 7), email="olivia@example.com"); a.save()
a = Author(name="Robert Anderson", birth_date=date(1972, 11, 18), email="robert@example.com"); a.save()
a = Author(name="Sophia Davis", birth_date=date(1998, 12, 5), email="sophia@example.com"); a.save()
a = Author(name="David Wilson", birth_date=date(1982, 7, 25), email="david@example.com"); a.save();
a = Author(name="Emily Thompson", birth_date=date(1995, 3, 10), email="emily@example.com"); a.save();
a = Author(name="Michael Johnson", birth_date=date(1978, 9, 30), email="michael@example.com"); a.save();
a = Author(name="John Smith", birth_date=date(1990, 1, 1), email="john@example.com"); a.save();
a = Author(name="Jane Doe", birth_date=date(1985, 5, 15), email="jane@example.com"); a.save();
a = Author(name="James Harris", birth_date=date(1993, 4, 23), email="james@example.com"); a.save();
a = Author(name="Isabella Young", birth_date=date(1987, 2, 14), email="isabella@example.com"); a.save();
