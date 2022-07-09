from django.template.defaulttags import register


@register.simple_tag()
def artwork_page_url(artworks_page, artwork):
    url = artworks_page.url + artworks_page.reverse_subpage(
        "artwork",
        args=(str(artwork.slug),),
    )
    return url
