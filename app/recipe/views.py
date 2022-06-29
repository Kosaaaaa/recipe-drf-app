"""
Views for the recipe APIs
"""

from drf_excel.renderers import XLSXRenderer
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import mixins, status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_csv.renderers import CSVRenderer

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """
    View for manage recipe APIs.
    """
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _params_to_ints(qs):
        """
        Convert a list of strings to integers.
        """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """
        Retrieve recipes for authenticated user.
        """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """
        Return the serializer class for request.
        """
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new recipe.
        """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """
        Upload an image to recipe.
        """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class XlsxCsvFileMixin(APIView):
    """
    Mixin which allows to render data using XLSX and CSV renderers.
    """

    filename = 'export'
    renderer_classes = [*api_settings.DEFAULT_RENDERER_CLASSES, CSVRenderer, XLSXRenderer]

    def get_filename(self, request=None):
        """
        Returns a custom filename for the attachment.
        """
        request = request or self.request
        extension = request.query_params.get('format')
        name = request.query_params.get('filename', self.filename)
        return f'{name}.{extension}'

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Return the response with the proper content disposition and the customized
        filename instead of the browser default (or lack thereof).
        """
        response = super().finalize_response(request, response, *args, **kwargs)
        if request.query_params.get('format') in ('xlsx', 'csv'):
            response['Content-Disposition'] = f'attachment; filename={self.get_filename()}'
        return response


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.',
            ),
            OpenApiParameter(
                'format',
                OpenApiTypes.STR, enum=['csv', 'xlsx', 'json'],
                description='Response format.'
            ),
            OpenApiParameter(
                'filename',
                OpenApiTypes.STR,
                description='Filename for attachments.'
            )
        ]
    ),
    destroy=extend_schema(parameters=[OpenApiParameter('format', exclude=True)]),
    update=extend_schema(parameters=[OpenApiParameter('format', exclude=True)]),
    create=extend_schema(parameters=[OpenApiParameter('format', exclude=True)]),
    partial_update=extend_schema(parameters=[OpenApiParameter('format', exclude=True)]),
)
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            XlsxCsvFileMixin,
                            viewsets.GenericViewSet):
    """
    Base ViewSet for recipe attributes.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Create a new model instance with user from request.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Filter queryset to authenticated user.
        """
        assigned_only = bool(int(self.request.query_params.get('assigned_only', 0)))

        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """
    Manage tags in the database.
    """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class IngredientViewSet(BaseRecipeAttrViewSet):
    """
    Manage ingredients in the database.
    """
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
