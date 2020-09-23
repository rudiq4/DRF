from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Movie, MovieShots, Category, Actor, Genre, RatingStar, Rating, Review


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Опис", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)  # interesting


class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 1  # Количество дополн. полей
    readonly_fields = ('name', 'email')


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Зображення'  # interesting


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    filter_horizontal = ('directors', 'actors', 'genres')  # interesting
    list_filter = ('category',)
    search_fields = ('title',)
    inlines = [MovieShotsInLine, ReviewInLine]  # interesting
    save_on_top = True  # interesting
    save_as = True  # interesting
    list_editable = ('draft',)
    readonly_fields = ('get_image',)
    form = MovieAdminForm
    actions = ['publish', 'unpublish', 'pinokio']
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster", "get_image")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="200" height="300"')

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запис було оновлено'
        else:
            message_bit = f'{row_update} записів було оновлено'
        self.message_user(request, f'{message_bit}')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запис було оновлено'
        else:
            message_bit = f'{row_update} записів було оновлено'
        self.message_user(request, f'{message_bit}')

    def pinokio(self, request, queryset):  # my
        return self.message_user(request, 'Попавсь на копкан єбучий')

    get_image.short_description = 'Постер'  # interesting

    publish.short_description = 'Опублікувати'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Зняти з публікації'
    unpublish.allowed_permissions = ('change',)

    pinokio.short_description = 'Затралірувати лалку'
    pinokio.allowed_permissions = ('change',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'movie', 'parent', 'id')
    readonly_fields = ('name', 'email')  # interesting


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Зображення'  # interesting


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "movie", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Зображення'  # interesting


admin.site.register(RatingStar)
admin.site.site_title = "R-CRM"
admin.site.site_header = "R-CRM"
