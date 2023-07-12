from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    summary = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"Author(name={self.name}, email={self.email})"

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")

    def __str__(self) -> str:
        return f"Blog(title={self.title}, author={self.author}, pub_date={self.pub_date})"

