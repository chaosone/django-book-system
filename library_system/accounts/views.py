from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ReaderRegistrationForm
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        form = ReaderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create user profile
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                role='reader',
                phone=form.cleaned_data.get('phone', '')
            )

            login(request, user)
            return redirect('home')
    else:
        form = ReaderRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
