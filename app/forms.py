from django import forms
from tinymce.widgets import TinyMCE
from .models import Article, Category, Comment, Tag


class ArticleForm(forms.ModelForm):
    """Form for creating and editing articles with TinyMCE editor"""
    
    content = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text='Full article content'
    )
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
            'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary); min-height: 120px;',
        }),
        help_text='Hold Ctrl/Cmd to select multiple tags'
    )
    
    scheduled_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
            'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
        }),
        help_text='Schedule for future publication (optional)'
    )
    
    class Meta:
        model = Article
        fields = [
            'title',
            'featured_image',
            'excerpt',
            'content',
            'category',
            'tags',
            'article_type',
            'status',
            'is_featured',
            'scheduled_at',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
                'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
                'placeholder': 'Enter article title...'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
                'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
                'placeholder': 'Brief description for article preview...',
                'rows': 3,
                'maxlength': 300
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-500 file:text-white hover:file:bg-green-600',
                'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
                'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
            }),
            'article_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
                'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
                'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded focus:ring-2',
                'style': 'accent-color: var(--brand-secondary);',
            }),
        }


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories"""
    
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
                'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
                'placeholder': 'Category name...'
            }),
        }


class TagForm(forms.ModelForm):
    """Form for creating and editing tags"""
    
    class Meta:
        model = Tag
        fields = ['name', 'is_predefined']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
                'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
                'placeholder': 'Tag name...'
            }),
            'is_predefined': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded focus:ring-2',
                'style': 'accent-color: var(--brand-secondary);',
            }),
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments to articles"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg transition focus:outline-none focus:ring-2',
                'style': 'background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);',
                'placeholder': 'Write a comment...',
                'rows': 3,
                'maxlength': 1000
            }),
        }
    
    def clean_content(self):
        """Validate comment content"""
        content = self.cleaned_data.get('content', '').strip()
        
        if len(content) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        
        if len(content) > 1000:
            raise forms.ValidationError('Comment cannot exceed 1000 characters.')
        
        return content
