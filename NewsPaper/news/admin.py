from django.contrib import admin
from .models import Post,Author,Category,PostCategory
class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.get_fields()[3:9]]
    list_filter = ('category', 'created_at_date', 'post_author')

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Author)
