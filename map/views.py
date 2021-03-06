import logging

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.db import transaction
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, mixins, status, filters

from game.utils import load_class
from game.models import CropSpecies
from map.models import Map, Cell
from inventory.models import Slot
from item.models import Item, SEED
from map.serializers.serializers import CellSerializer

logger = logging.getLogger(__name__)


class CellViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  mixins.ListModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    # TODO: This view set should only return those cells belong to the user
    queryset = Cell.objects.all().order_by('id')
    serializer_class = CellSerializer


@parser_classes(JSONParser)
@api_view(['POST'])
def seeding(request):
    # take cell_id, and slot_id from resuest
    user = request.user
    # params = request.POST.copy()
    print(f'user: {user}, params: {request.data}')
    cell_id = request.data.get('cell_id')
    slot_id = request.data.get('slot_id')
    print(f'cell_id: {cell_id}, slot_id: {slot_id}')
    if not cell_id or not slot_id:
        return Response('Required data not fullfilled.', status=400)

    try:
        cell = Cell.objects.get(id=cell_id, map__user=user)
        slot = Slot.objects.get(id=slot_id, inventory__user=user)
    except (Cell.DoesNotExist, Slot.DoesNotExist):
        return Response('Cell or Slot not found error.', status=400)

    if slot.item.type != SEED:
        print(f'slot.item: {slot.item}')
        return Response('Selected item is not a seed type.', status=400)

    if not cell.is_blank_cell():
        return Response('Selected cell is not blank', status=400)

    with transaction.atomic():
        cell.crop = CropSpecies.objects.get(code=slot.item.values['crop_species']).create_crop()
        cell.save()
        slot.item.delete()
        logger.info(f'Seeding success! {cell.crop.crop_species.name} at '
                    f'({cell.position_x}, {cell.position_y})')

    return Response({"status": "Success!"})


@api_view(['POST'])
def gathering(request):
    # take cell_id from request
    user = request.user
    cell_id = request.data.get('cell_id')
    if not cell_id:
        return Response('Required data not fullfilled.', status=400)

    try:
        cell = Cell.objects.get(id=cell_id, map__user=user)
    except (Cell.DoesNotExist, Slot.DoesNotExist):
        return Response('Cell or Slot not found error.', status=400)

    if not cell.is_availbe_for_harvest():
        return Response('Cell cannot be harvested.', status=400)

    with transaction.atomic():
        item_list = cell.crop.get_harvest_reward()
        inventory = user.inventory
        if not inventory.insert_item_list(item_list):
            raise Exception
        print(f'cell: {cell}')
        cell.crop.delete()

        # except Exception as e:
        #     return Response('Unkown error occured when get the reward.', status=400)

    return Response({"status": "Success!"})


@api_view(['POST'])
def uproot(request):
    # take cell_id from resuest
    # TODO: remove the crop
    user = request.user

    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})