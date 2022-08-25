from collections import defaultdict
from typing import Dict, Union
import datetime

LAST_UPDATE: Dict[str, Union[None, datetime.datetime]] = {
    "standard_pages": None,
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
        "presentation_page": <PresentationPage>,
        "work_experience_page": <WorkExperiencePage>,
        ...
    }
    """
    # This cannot be done in the main body of the page, because models
    # are not yet loaded when this page is imported in the settings.
    from home.models import ArtworksPage, PresentationPage, WorkExperiencePage

    standard_pages = defaultdict()

    # Add presentation page
    presentation_page = PresentationPage.objects.filter().first()
    standard_pages["presentation_page"] = presentation_page

    # Add Work Experience page
    work_experience_page = WorkExperiencePage.objects.filter().first()
    standard_pages["work_experience_page"] = work_experience_page

    # Add artworks page
    artworks_page = ArtworksPage.objects.filter().first()
    standard_pages["artworks_page"] = artworks_page

    return dict(standard_pages)


def standard_pages(_):
    if not is_recent("standard_pages"):
        update_last_change("standard_pages")
    return load_standard_pages()
