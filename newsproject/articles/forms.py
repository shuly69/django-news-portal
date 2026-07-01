"""
Forms for creating and editing articles.

ArticleForm excludes the 'author' field because it is always set
programmatically in the view (form.instance.author = request.user).
Exposing it in the form would be a security issue.
"""

from django import forms

from .models import Article, Category, SubCategory


class ArticleForm(forms.ModelForm):
    """Form used for both article creation and editing."""

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Enter article title"}
        )
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "style": "display:none",
                "accept": "image/*",
                "id": "imageUpload",
            }
        ),
    )
    excerpt = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "textarea-el rich-text-editor",
                "placeholder": "Enter a brief summary of the article",
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"id": "quill-container"})
    )
    meta_description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-textarea",
                "id": "metaDescription",
                "placeholder": "Enter meta description for SEO",
                "rows": 3,
            }
        ),
    )
    meta_keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "id": "metaKeywords",
                "placeholder": "Enter meta keywords for SEO",
            }
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-select", "id": "articleCategory", "required": True}
        ),
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={"class": "form-select", "id": "articleSubCategory"}
        ),
    )
    status = forms.ChoiceField(
        choices=Article.Status.choices,
        widget=forms.Select(attrs={"class": "form-select", "id": "articleStatus"}),
    )

    class Meta:
        model = Article
        # 'author' is intentionally excluded – set in the view from request.user.
        fields = [
            "title",
            "image",
            "excerpt",
            "content",
            "meta_description",
            "meta_keywords",
            "category",
            "subcategory",
            "status",
        ]
