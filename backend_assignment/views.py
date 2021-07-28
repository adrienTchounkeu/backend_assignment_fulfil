from backend_assignment.models import Product, User
from backend_assignment.serializers import ProductSerializer, UserSerializer
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from backend_assignment.signals import s_product_update, s_product_create
from django.core.files.storage import default_storage
from backend_assignment.tasks import compute_data

# Initiate the Socket IO connection
import socketio

async_mode = None

sio = socketio.Server(async_mode='threading', cors_allowed_origins="*")

room = None


@sio.on('connection-bind')
def connection_bind(sid, data):
    print("Connection Initiated ", sid, data)


@sio.on('connect')
def connection_bind(sid, data):
    global room
    room = sid
    print("Socket connected")


@sio.on('disconnect')
def test_disconnect(sid):
    print("Socket disconnected ", sid)


class ListProductView(generics.ListAPIView):
    """
    Handle Story 2 :
    - list of products
    - filter on name, sku and status
    - search on name, sku, description
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'sku', 'status']
    search_fields = ['name', 'sku', 'description']


class DeleteProductsView(APIView):
    """
    Handle Story 3:
    - delete all products in the database
    """

    def delete(self, request, format=None):
        # delete all records
        Product.objects.all().delete()
        return Response("Products successfully deleted", status=status.HTTP_200_OK)


class CreateProductView(APIView):
    """
    Handle rest of Story 4:
    - create a Product
    """
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # user has create webhooks enable ??? If Yes send create_signal
            user = User.objects.get_or_create(name='user')
            if user.create_trigger:
                s_product_create.send(sender=self.__class__, product=serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProductView(APIView):
    """
    Handle rest of Story 4:
    - create a Product
    """

    def put(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response("No product", status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # user has update webhooks enable ??? If Yes send update_signal
            user = User.objects.get_or_create(name='user')
            if user.update_trigger:
                s_product_update.send(sender=self.__class__, product=serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateWebhookView(APIView):
    """
    Handle rest of Story 5:
    - Set Webhook for manual creation and update
    """

    def put(self, request, name, format=None):
        user, _ = User.objects.get_or_create(name=name)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
    """
    Handle 1 : Upload the file, compute and store using Celery
    """

    def post(self, request, format=None):
        print(room)
        file_obj = request.FILES['file']
        file_name = default_storage.save(file_obj.name, file_obj)
        compute_data.delay(default_storage.path(file_name))
        return Response("File Computed And Stored", status=status.HTTP_200_OK)


class EmitView(APIView):
    """
    This View helps to send socket to the client
    """
    def post(self, request, format=None):
        sio.emit('test', request.data, room=room)
        return Response("Good")
