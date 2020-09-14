from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics  # contains filters so spec categories belong to spec users
from rest_framework import viewsets
from rest_framework.exceptions import (
    ValidationError, PermissionDenied
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.api.models import Category, Note
from apps.api.serializers import CategorySerializer, NoteSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    # means user must be logged in to system to create a category
    permission_classes = (IsAuthenticated,)
    # convert data back and forth
    serializer_class = CategorySerializer

    # serializer_class.is_valid(raise_exception=True, )
    def get_queryset(self):
        queryset = Category.objects.all().filter(
            owner=self.request.user     # owner=self.request.user: filter by user name
        )
        return queryset

    def create(self, request, *args, **kwargs):
        # check if the category already exists for the current logged in user
        category = Category.objects.filter(
            title=request.data.get('title'),
            owner=request.user
        )
        if category:
            msg = 'A category with that name already exists'
            raise ValidationError(msg)
        # create comes from ModelViewSet
        # need to overwrite the create method that comes from ModelViewSet
        return super().create(request)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):  # perform destroy asks before deleting
        # get category from URL
        category = Category.objects.get(pk=self.kwargs["pk"])
        # if category doesn't belong to owner, then user is not allowed to delete category
        if not request.user == category.owner:
            # raise an error message
            raise PermissionDenied("You cannot delete this category")
        super().destroy(request, *args, **kwargs)
        return Response(
            {
                'message': f'{category} has been deleted',
                'status': status.HTTP_200_OK
            }
        )


# allows us to create a list at the same time (don't need list, retrieve, patch, update, etc. methods)
class CategoryNotes(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        # category_pk from URL
        # check if pk is in URL
        if self.kwargs.get("category_pk"):
            # if it is in URL, get the key (particular category)
            category = Category.objects.get(pk=self.kwargs["category_pk"])
            queryset = Note.objects.filter(
                owner=self.request.user,
                category=category,
            )
            return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # when creating, it's called. save the information
        # self.request.user: get the user (in this case, get the owner)


class SingleCategoryNote(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        # if id for category & id for note from URL both match database entries
        if self.kwargs.get("category_pk") and self.kwargs.get("pk"):
            category = Category.objects.get(pk=self.kwargs["category_pk"])
            queryset = Note.objects.filter(
                pk=self.kwargs["pk"],
                owner=self.request.user,
                category=category
            )
            return queryset


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.all().filter(
            owner=self.request.user
        )
        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied(
                "Only logged in users with accounts can create a note"
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        note = Note.objects.get(pk=self.kwargs["pk"])
        if not request.user == note.owner:
            raise PermissionDenied(
                "You have no permissions to edit this note"
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        note = Note.objects.get(pk=self.kwargs["pk"])
        if not request.user == note.owner:
            raise PermissionDenied(
                "You have no permissions to delete this note"
            )
        super().destroy(request, *args, **kwargs)
        return Response(
            {
                "message": f'{note} has been deleted',
                "status": status.HTTP_200_OK
            }
        )

