from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Follow, User, Group


'''
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', )
        model = User '''


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username',
                                          default=serializers.CurrentUserDefault())
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False)

    class Meta:
        fields = '__all__'
        model = Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True,
                                          default=serializers.CurrentUserDefault())
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        read_only_fields = ('author',)
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username',
                                        default=serializers.CurrentUserDefault())
    # было read_only=True вместо queryset
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    def validate_following(self, following):
        if self.context.get('request').user == following:
            raise serializers.ValidationError
        return following

    class Meta:
        model = Follow
        exclude = ('id',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]
