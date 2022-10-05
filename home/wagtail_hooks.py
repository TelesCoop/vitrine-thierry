from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)
from .models import Article, ArticleType, Artwork, FriendlySite, Gallery, ReferenceSite


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
    list_filter = ("galleries",)


class GalleriesAdminGroup(ModelAdminGroup):
    menu_label = "Galeries d'oeuvres"
    menu_order = 401
    menu_icon = "folder-inverse"
    items = (
        GalleryAdmin,
        ArtworkAdmin,
    )


class ArticleTypeAdmin(ModelAdmin):
    model = ArticleType
    menu_label = "Types d'article"
    menu_icon = "folder"
    add_to_settings_menu = False
    search_fields = "name"


class ArticlesAdmin(ModelAdmin):
    model = Article
    menu_label = "Articles"
    menu_icon = "folder"
    add_to_settings_menu = False
    search_fields = "name"


class AriclesAdminGroup(ModelAdminGroup):
    menu_label = "Articles"
    menu_order = 405
    menu_icon = "folder-inverse"
    items = (
        ArticleTypeAdmin,
        ArticlesAdmin,
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
    menu_order = 410
    menu_icon = "folder-inverse"
    items = (
        FriendlySiteAdmin,
        ReferenceSiteAdmin,
    )


modeladmin_register(GalleriesAdminGroup)
modeladmin_register(FooterAdminGroup)
modeladmin_register(AriclesAdminGroup)
