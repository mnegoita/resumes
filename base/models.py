from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User




# Category model ######################################################################################

class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=40, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', 
        blank = True, 
        null = True, 
        related_name = "children", 
        on_delete=models.CASCADE)

    def get_absolute_url(self):
        url = "/categories/{0}/".format(self.slug)
        ctg = self 
        while ctg.parent:
            url = f"{ctg.parent.get_absolute_url()}{self.slug}/"
            ctg = ctg.parent
            return url
        return url

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields = ['author', 'name',],
                name = 'unique_author_name_category'
            ),
            models.UniqueConstraint(
                fields = ['parent', 'slug',],
                name = 'unique_parent_slug_category'
            )
        ]
        

# Tag model ######################################################################################

class Tag(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=40, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()

    def get_absolute_url(self):
        return "/tags/{0}/".format(self.slug)

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = 'Tags'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields = ['author', 'name', 'slug'],
                name = 'tag_unique_author_name_slug'
            )
        ]


