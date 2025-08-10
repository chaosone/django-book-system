from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class BorrowingRecord(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')

    class Meta:
        db_table = 'borrowing_record'

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class SystemConfig(models.Model):
    config_key = models.CharField(max_length=50, unique=True)
    config_value = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'system_config'

    def __str__(self):
        return self.config_key
