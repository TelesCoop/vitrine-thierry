from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)
from .models import Artwork, Gallery


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


class GelleriesAdminGroup(ModelAdminGroup):
    menu_label = "Galeries d'oeuvres"
    menu_order = 401
    menu_icon = "folder-inverse"
    items = (
        GalleryAdmin,
        ArtworkAdmin,
    )


modeladmin_register(GelleriesAdminGroup)
