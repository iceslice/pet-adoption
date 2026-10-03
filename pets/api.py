from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import permissions, serializers, viewsets

from .models import AdoptionRequest, Pet
from .services import validate_new_request


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'


class AdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionRequest
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at']

    def validate(self, data):
        if self.instance is None:
            try:
                validate_new_request(self.context['request'].user, data['pet'])
            except DjangoValidationError as e:
                raise serializers.ValidationError(e.messages)
        return data


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filterset_fields = ['animal_type', 'gender', 'location', 'status', 'breed']
    search_fields = ['name', 'breed', 'description']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AdoptionViewSet(viewsets.ModelViewSet):
    serializer_class = AdoptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'head', 'options']

    def get_queryset(self):
        return AdoptionRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
