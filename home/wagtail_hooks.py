from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)
from .models import Artwork, FriendlySite, Gallery, ReferenceSite


class GalleryAdmin(ModelAdmin):
    model = Gallery
    menu_label = "Galeries"
    menu_icon = "folder"
    add_to_settings_menu = False
    search_fields = "name"


class ArtworkAdmin(ModelAdmin):
    model = Artwork
    menu_label = "Oeuvres"
    menu_icon = "folder"
    add_to_settings_menu = False
    search_fields = "name"


class GalleriesAdminGroup(ModelAdminGroup):
    menu_label = "Galeries d'oeuvres"
    menu_order = 401
    menu_icon = "folder-inverse"
    items = (
        GalleryAdmin,
        ArtworkAdmin,
    )


class FriendlySiteAdmin(ModelAdmin):
    model = FriendlySite
    menu_label = "Sites amis"
    menu_icon = "folder"
    add_to_settings_menu = False
    search_fields = "name"


class ReferenceSiteAdmin(ModelAdmin):
    model = ReferenceSite
    menu_label = "Sites références"
    menu_icon = "folder"
    add_to_settings_menu = False
    search_fields = "name"


class FooterAdminGroup(ModelAdminGroup):
    menu_label = "Bas de page"
    menu_order = 402
    menu_icon = "folder-inverse"
    items = (
        FriendlySiteAdmin,
        ReferenceSiteAdmin,
    )


modeladmin_register(GalleriesAdminGroup)
modeladmin_register(FooterAdminGroup)
