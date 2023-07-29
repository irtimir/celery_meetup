from time import sleep

from django import forms

from mail.models import Letter


class FeedbackForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={"rows": 5})
    )

    def send_email(self):
        message = self.cleaned_data["message"]
        Letter.objects.create(
            subject="Your Feedback",
            message=f"\t{message}\n\nThank you!",
            from_email="support@example.com",
            recipient=self.cleaned_data["email"],
        )
