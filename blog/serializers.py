from rest_framework import serializers

from .models import Category, Blog , Comment , Likes , PostViews

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta :
            model = Category
            fields = (
                'id', 
                'name',
            )
        
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # User Bilgisinin görüntülenmebilmesi için eklenmiştir.
    user_id = serializers.IntegerField(read_only =True) 
    blog= serializers.StringRelatedField() # Hangi bloğun bilgisibi görebilmek için eklenmiştir
    blog_id = serializers.IntegerField()
    
    class Meta :
        model = Comment
        fields = (
            'id',
            'user',
            'user_id',
            'time_stamp',
            'content',
            'blog',
            'blog_id',
        )
    def create(self,validate_date):
        validate_date['user_id']= self.context['request'].user.id
        instance = Comment.objects.create(**validate_date)
        return instance
            
 
class LikesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(read_only = True)
    blog_id = serializers.IntegerField()
    class Meta :
        model = Likes
        fields = (
            'id',
            'user_id',
            'user',
            'blog_id',
            "likes",
            
        )
    def create(self,validate_date):
        validate_date['user_id']= self.context["request"].user.id
        instance = Likes.objects.create(**validate_date)
        return instance
        
class PostViewsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(read_only =True)
    blog= serializers.StringRelatedField()
    blog_id = serializers.IntegerField()
   
    class Meta:
        model = PostViews
        fields = (
            'id',
            'user',
            "user_id",    
            "blog", 
            "blog_id",
            "post_views",)
        
    def create(self,validate_date):
        validate_date["user_id"]= self.context["request"].user.id
        instance = PostViews.objects.create(**validate_date)
        return instance
        
class BlogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(read_only= True)
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    comments = CommentSerializer(many = True, read_only = True)
    likes =  LikesSerializer(many = True, read_only = True) 
    likes_toplam = serializers.SerializerMethodField() 
    post_views_toplam = serializers.SerializerMethodField()
    comment_toplam = serializers.SerializerMethodField()
    class Meta :
        model = Blog
        fields = (
            'id',
            'title',
            'content',
            'image',
            'category',
            'category_id',
            'publish_date',
            'user',
            'user_id',
            'status',
            'comments', 
            'likes',
            'likes_toplam',
            'post_views_toplam',
            'comment_toplam',
            
        )
        
    def create(self,validate_date):
        validate_date["user_id"]= self.context["request"].user.id
        instance = Blog.objects.create(**validate_date)
        return instance
    
    # Kaçtane  yorum yapıldığını hesaplayan kod:
    def get_comment_toplam(self, obj):
        return Comment.objects.filter(blog=obj.id).count()
    
    # Kaçtane like olduğunu hesaplayan kod:
    
    def get_likes_toplam(self, obj):
        return Likes.objects.filter(likes=True, blog_id=obj.id).count()
    
    
    #  Blogları görüntüleyenlein sayısını hesaplayan kod:
 
    def get_post_views_toplam(self, obj):
            return PostViews.objects.filter(post_views = True , blog_id=obj.id).count()
        
        
class UserBlogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(read_only= True)
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    comments = CommentSerializer(many = True, read_only = True)
    likes_toplam = serializers.SerializerMethodField() 
    post_views_toplam = serializers.SerializerMethodField()
    comment_toplam = serializers.SerializerMethodField()
    
    class Meta :
        model = Blog
        fields = (
            'id',
            'title',
            'content',
            'image',
            'category',
            'category_id',
            'publish_date',
            'user',
            'user_id',
            'comments',
            'status', 
            'likes_toplam',
            'post_views_toplam',
            'comment_toplam',
            
        )
        
    def create(self,validate_date):
        validate_date["user_id"]= self.context["request"].user.id
        instance = Blog.objects.create(**validate_date)
        return instance
    
    # Kaçtane  yorum yapıldığını hesaplayan kod:
    def get_comment_toplam(self, obj):
        return Comment.objects.filter(blog=obj.id).count()
    
    # Kaçtane like olduğunu hesaplayan kod:
    
    def get_likes_toplam(self, obj):
        return Likes.objects.filter(likes=True, blog_id=obj.id).count()
    
    
    #  Blogları görüntüleyenlein sayısını hesaplayan kod:
 
    def get_post_views_toplam(self, obj):
        return PostViews.objects.filter(post_views = True , blog_id=obj.id).count()



    

