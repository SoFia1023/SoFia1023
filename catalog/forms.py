from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'comment']
        widgets = {
            'stars': forms.Select(
                choices=[(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)],  
                attrs={'class': 'form-control'}
            ),
            'comment': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your opinion here...'}
            ),
        }
