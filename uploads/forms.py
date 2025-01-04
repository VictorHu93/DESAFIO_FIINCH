from django import forms

class MultiPDFUploadForm(forms.Form):
    arquivo = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True}),  # Usa FileInput padrão
        help_text="Selecione de 1 a 5 arquivos PDF."
    )
