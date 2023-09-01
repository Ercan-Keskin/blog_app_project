from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ("name",)
        verbose_name_plural = ("Kategori")

class Blog(models.Model):
    STATUS = (
        ('p', 'PUBLISHED'),
        ('d', 'DRAFT'),
        ('?', 'To_Be_Deleting')
    )
    title = models.CharField(max_length=200, unique=True) #Başlık
    content = models.TextField() # içerik
    image = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog')
    publish_date = models.DateTimeField(auto_now_add=True) #yayın tarihi
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length= 10, blank=True, null=True, default='?')
    
    def __str__ (self):
        return f"{self.title} - Kullanıcı: - {self.user} "
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    time_stamp = models.DateTimeField(auto_now_add=True) # time_stamp zaman damgası olarak çeviriliyor
    content = models.CharField(max_length=200) # İçerik
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_comment")
    
    def __str__(self):
        return  f"{self.content} - {self.user}"
    
    class Meta:
        verbose_name_plural = ("Yorum")
    
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="post_likes")
    likes =  models.BooleanField(default=False)
    
    def __str__(self):
        return  f"{self.blog} - {self.user}"
    
           
    

class PostViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    post_views = models.BooleanField(default=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name= "blog_postviews")
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  f"{self.user} - {self.post_views}-{self.blog}-{self.time_stamp}"
    
    class Meta:  
        verbose_name_plural = ("Gönderi Görünümü")
       
 