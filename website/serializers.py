from rest_framework import serializers
from .models import SolicitudContacto


class SolicitudContactoSerializer(serializers.ModelSerializer):
    fecha_envio = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = SolicitudContacto
        fields = [
            'id',
            'nombre',
            'email',
            'mensaje',
            'categoria',
            'fecha_envio',
            'leida',
        ]


class RecetaExternaSerializer(serializers.Serializer):
    idMeal = serializers.CharField()
    strMeal = serializers.CharField()
    strMealThumb = serializers.URLField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'id': data['idMeal'],
            'nombre': data['strMeal'],
            'imagen': data['strMealThumb'],
            'url_receta': f"https://www.themealdb.com/meal/{data['idMeal']}",
        }