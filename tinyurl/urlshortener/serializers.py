from rest_framework import serializers

from . models import UrlShortener


class UrlShortenerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UrlShortener
        fields = ['original_url', 'shorten_url', 'created']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        urlsh = UrlShortener.objects.filter(original_url=validated_data['original_url']).first()
        if not urlsh:
            entry = dict(original_url=validated_data['original_url'])
            urlsh = UrlShortener.objects.create(**entry)
        urlsh.set_shorten_url()
        return urlsh

    #def update(self, instance, validated_data):
        #return UrlShortener.objects.filter(original_url=validated_data['original_url']).first()
        #"""
        #Update and return an existing `Snippet` instance, given the validated data.
        #"""
        #instance.title = validated_data.get('title', instance.title)
        #instance.code = validated_data.get('code', instance.code)
        #instance.linenos = validated_data.get('linenos', instance.linenos)
        #instance.language = validated_data.get('language', instance.language)
        #instance.style = validated_data.get('style', instance.style)
        #instance.save()
        #return instance
