from collections import defaultdict
from typing import Dict, Union
import datetime

from home.models import ArticlesPage, HomePage

LAST_UPDATE: Dict[str, Union[None, datetime.datetime]] = {
    "standard_pages": None,
    "footer_data": None,
}


def is_recent(key: str):
    """Check if values for the given key have been updated recently."""
    if not LAST_UPDATE[key]:
        return False
    return (datetime.datetime.now() - LAST_UPDATE[key]).total_seconds() < 60  # type: ignore


def update_last_change(key):
    """Mark key as last updated now."""
    LAST_UPDATE[key] = datetime.datetime.now()


def load_standard_pages():
    """
    Returns context with standard pages such as
    {
        "work_experience_page": <WorkExperiencePage>,
        "artworks_page": <ArtworksPage>,
        ...
    }
    """
    # This cannot be done in the main body of the page, because models
    # are not yet loaded when this page is imported in the settings.
    from home.models import ArtworksPage, WorkExperiencePage

    standard_pages = defaultdict()

    # Add home page
    home_page = HomePage.objects.filter().first()
    standard_pages["home_page"] = home_page

    # Add Work Experience page
    work_experience_page = WorkExperiencePage.objects.filter().first()
    standard_pages["work_experience_page"] = work_experience_page

    # Add artworks page
    artworks_page = ArtworksPage.objects.filter().first()
    standard_pages["artworks_page"] = artworks_page

    # Add articles page
    articles_page = ArticlesPage.objects.filter().first()
    standard_pages["articles_page"] = articles_page

    return dict(standard_pages)


def load_footer_data():
    # This cannot be done in the main body of the page, because models
    # are not yet loaded when this page is imported in the settings.
    from home.models import FriendlySite, ReferenceSite

    footer_data = defaultdict()

    friendly_sites = FriendlySite.objects.filter(display=True)
    footer_data["friendly_sites"] = friendly_sites

    reference_sites = ReferenceSite.objects.filter(display=True)
    footer_data["reference_sites"] = reference_sites

    return dict(footer_data)


def standard_pages(_):
    if not is_recent("standard_pages"):
        update_last_change("standard_pages")
    return load_standard_pages()


def footer_data(_):
    if not is_recent("footer_data"):
        update_last_change("footer_data")
    return load_footer_data()
