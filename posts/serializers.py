from unicodedata import name
from rest_framework import serializers

class PostsSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    post_title = serializers.CharField()
    post_body = serializers.CharField()
    total_number_of_comments = serializers.CharField()

class CommentsSerializer(serializers.Serializer):
    postId = serializers.IntegerField()
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    body = serializers.CharField()
