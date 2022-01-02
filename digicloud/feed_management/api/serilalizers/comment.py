from rest_framework.serializers import ModelSerializer
from digicloud.feed_management.models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created', 'updated', 'removed', 'is_active']

    def create(self, validated_data, user=None):
        return Comment.objects.create(feed_item=validated_data['feed_item'],
                                      user=user,
                                      title=validated_data['title'],
                                      description=validated_data['description'])


class UpdatableCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created', 'updated', 'removed', 'is_active', 'user', 'feed_item']

    def create(self, validated_data, user=None):
        return Comment.objects.create(feed_item=validated_data['feed_item'],
                                      user=user,
                                      title=validated_data['title'],
                                      description=validated_data['description'])


class ReadOnlyCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['removed', 'is_active']
