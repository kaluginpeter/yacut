from string import ascii_letters, digits


def validate_short_url(url):
    return (
        all(char in ascii_letters + digits for char in url)
        and len(url) <= 16
    )
