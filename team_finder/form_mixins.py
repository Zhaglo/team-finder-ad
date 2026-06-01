from urllib.parse import urlparse

from django.core.exceptions import ValidationError


class GithubUrlValidatorMixin:
    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')

        if not github_url:
            return github_url

        parsed_url = urlparse(github_url)
        domain = parsed_url.netloc.lower()

        if domain != 'github.com' and not domain.endswith('.github.com'):
            raise ValidationError('Ссылка должна вести на GitHub.')

        return github_url
