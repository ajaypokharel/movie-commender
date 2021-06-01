from rest_framework import serializers


class MovieRecommendationSerializer(serializers.Serializer):
    movies = serializers.ListField(child=serializers.CharField(max_length=250, allow_null=True, allow_blank=True)
                                   )
    watcher = serializers.CharField(max_length=100)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
