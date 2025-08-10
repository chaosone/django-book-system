from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from books.models import Book
from .models import BorrowingRecord, SystemConfig
from accounts.decorators import role_required

def can_borrow_book(user, book):
    """Check if a user can borrow a book."""
    # Check user status
    if not hasattr(user, 'userprofile') or user.userprofile.status != 'active':
        return False, "User account is not active."

    # Check book status
    if book.status != 'in_library':
        return False, "Book is not available."

    # Check borrowing limit
    try:
        max_borrows = int(SystemConfig.objects.get(config_key='max_borrow_limit').config_value)
    except (SystemConfig.DoesNotExist, ValueError):
        max_borrows = 5 # Default value

    current_borrows = BorrowingRecord.objects.filter(user=user, status='borrowed').count()

    if current_borrows >= max_borrows:
        return False, "User has reached the maximum borrowing limit."

    # Check for overdue books
    overdue_books = BorrowingRecord.objects.filter(
        user=user,
        status='borrowed',
        due_date__lt=timezone.now()
    ).exists()

    if overdue_books:
        return False, "User has overdue books."

    return True, ""

@role_required(roles=['librarian'])
@transaction.atomic
def borrow_book_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')

        try:
            user = User.objects.get(id=user_id)
            book = Book.objects.select_for_update().get(id=book_id)

            can_borrow, reason = can_borrow_book(user, book)
            if not can_borrow:
                messages.error(request, f'Cannot borrow this book: {reason}')
                return redirect('borrow_book')

            # Get borrowing duration from config
            try:
                borrow_days = int(SystemConfig.objects.get(config_key='borrow_duration_days').config_value)
            except (SystemConfig.DoesNotExist, ValueError):
                borrow_days = 30 # Default value

            due_date = timezone.now() + timedelta(days=borrow_days)
            BorrowingRecord.objects.create(
                user=user,
                book=book,
                due_date=due_date
            )

            book.status = 'on_loan'
            book.save()

            messages.success(request, 'Book borrowed successfully.')

        except (User.DoesNotExist, Book.DoesNotExist):
            messages.error(request, 'User or book does not exist.')

        return redirect('borrow_book')

    return render(request, 'borrowing/borrow_book.html')
