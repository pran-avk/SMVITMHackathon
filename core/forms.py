"""
Authentication Forms for Museum Staff
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.models import MuseumStaff, Museum, Artwork, Artist, ArtworkTranslation


class MuseumRegistrationForm(forms.ModelForm):
    """Form for creating a new museum"""
    class Meta:
        model = Museum
        fields = ['name', 'description', 'location', 'contact_email', 'website', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Museum Name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Brief description of your museum'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City, Country'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'contact@museum.com'}),
            'website': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://museum.com'}),
        }


class StaffRegistrationForm(UserCreationForm):
    """Form for creating museum staff account"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your@email.com'})
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1234567890'})
    )
    
    class Meta:
        model = MuseumStaff
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Choose a username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm Password'})


class StaffLoginForm(AuthenticationForm):
    """Form for staff login"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'})
    )


class ArtworkUploadForm(forms.ModelForm):
    """Form for uploading artifacts with GPS location capture"""
    
    # Hidden fields for GPS coordinates (captured by JavaScript)
    latitude = forms.DecimalField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude = forms.DecimalField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    # Artist selection or creation
    artist_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Artist Name (optional)',
            'list': 'artists-list'
        })
    )
    
    class Meta:
        model = Artwork
        fields = [
            'title', 'description', 'category', 'year_created',
            'medium', 'dimensions', 'gallery_location', 'room_number',
            'image', 'audio_narration', 'historical_context',
            'latitude', 'longitude', 'geofence_radius_meters', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Artifact Name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 6, 'placeholder': 'Detailed description for AR display'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'year_created': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Year'}),
            'medium': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Oil on canvas'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 100x80 cm'}),
            'gallery_location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Gallery/Hall Name'}),
            'room_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Room Number'}),
            'historical_context': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Historical background'}),
            'geofence_radius_meters': forms.NumberInput(attrs={'class': 'form-input', 'value': 100}),
            'tags': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tags (comma-separated)'}),
        }
        
    def clean_tags(self):
        """Convert comma-separated tags to list"""
        tags_str = self.cleaned_data.get('tags', '')
        if isinstance(tags_str, str):
            return [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return tags_str


class ArtworkTranslationForm(forms.ModelForm):
    """Form for adding translations to existing artworks"""
    
    class Meta:
        model = ArtworkTranslation
        fields = ['language', 'title', 'description', 'historical_context', 'audio_narration']
        widgets = {
            'language': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Translated Title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 6}),
            'historical_context': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
        }
