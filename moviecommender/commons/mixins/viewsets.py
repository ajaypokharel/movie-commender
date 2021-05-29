from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateViewSetMixin(
    mixins.CreateModelMixin,
    GenericViewSet
):
    pass


class RetrieveViewSetMixin(
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    pass


class RetrieveUpdateViewSetMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    pass


class ListRetrieveUpdateViewSetMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    pass


class ListCreateUpdateRetrieveViewSetMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    pass


class ListRetrieveUpdateDestroyViewSetMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass


class UpdateDestroyViewSetMixin(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass


class RetrieveUpdateDestroyViewSetMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass


class CreateRetrieveViewSetMixin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    pass


class ListRetrieveCreateViewSetMixin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    pass


class ListRetrieveCreateDestroyViewSetMixin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass


class RetrieveUpdateDestroyViewSetMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass


class ListRetrieveCreateUpdateDestroyViewSetMixin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass


class ListRetrieveViewSetMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    pass


class ListViewSetMixin(
    mixins.ListModelMixin,
    GenericViewSet
):
    pass


class ListCreateViewSetMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    pass
