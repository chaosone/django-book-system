from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'book_category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Book(models.Model):
    STATUS_CHOICES = [
        ('in_library', 'In Library'),
        ('on_loan', 'On Loan'),
        ('reserved', 'Reserved'),
        ('lost', 'Lost'),
    ]

    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_library')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'book_info'

    def __str__(self):
        return self.title
