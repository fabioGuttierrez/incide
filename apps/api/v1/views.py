from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.catalog.models import Rubric
from apps.engine.analyzer import analyze_rubric, search_rubrics
from apps.workspace.models import Favorite, QueryLog

from .serializers import (
    RubricListSerializer,
    IncidenceResultSerializer,
    FavoriteSerializer,
    QueryLogSerializer,
)


# ─────────────────────────────────────────
# BUSCA
# ─────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def search_view(request):
    """
    GET /api/v1/search/?q=hora+extra

    Busca rubricas pelo nome e retorna lista com incidências resumidas.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response({'results': [], 'count': 0})

    rubrics = search_rubrics(query)
    serializer = RubricListSerializer(rubrics, many=True)

    # Loga a busca se usuário autenticado
    if request.user.is_authenticated and query:
        QueryLog.objects.create(
            user=request.user,
            search_term=query,
            session_key=request.session.session_key or '',
        )

    return Response({'results': serializer.data, 'count': len(serializer.data)})


# ─────────────────────────────────────────
# DETALHE DA RUBRICA (ENGINE)
# ─────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def rubric_detail_view(request, pk):
    """
    GET /api/v1/rubrics/<pk>/

    Retorna a análise completa de uma rubrica via decision engine.
    Aceita contexto via query params: ?regime_tributario=simples
    """
    context = None
    allowed_context_keys = {'regime_tributario', 'tipo_empresa'}
    context_params = {
        k: v for k, v in request.query_params.items()
        if k in allowed_context_keys
    }
    if context_params:
        context = context_params

    try:
        result = analyze_rubric(rubric_id=pk, context=context)
    except Rubric.DoesNotExist:
        return Response(
            {'detail': 'Rubrica não encontrada ou não publicada.'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception:
        return Response(
            {'detail': 'Incidência não cadastrada para esta rubrica.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Registra a consulta no log
    if request.user.is_authenticated:
        rubric = Rubric.objects.get(pk=pk)
        QueryLog.objects.create(
            user=request.user,
            rubric=rubric,
            session_key=request.session.session_key or '',
        )

    serializer = IncidenceResultSerializer(result)
    return Response(serializer.data)


# ─────────────────────────────────────────
# FAVORITOS
# ─────────────────────────────────────────

class FavoriteListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/favorites/   → lista favoritos do usuário
    POST /api/v1/favorites/   → adiciona favorito
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('rubric')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDestroyView(generics.DestroyAPIView):
    """
    DELETE /api/v1/favorites/<pk>/  → remove favorito
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


# ─────────────────────────────────────────
# HISTÓRICO
# ─────────────────────────────────────────

class HistoryListView(generics.ListAPIView):
    """
    GET /api/v1/history/  → últimas consultas do usuário
    """
    serializer_class = QueryLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            QueryLog.objects.filter(user=self.request.user)
            .select_related('rubric')
            .order_by('-created_at')[:50]
        )
