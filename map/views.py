import logging

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.db import transaction

from game.utils import load_class
from map.models import Map, Cell
from inventory.models import Slot, SeedItem

logger = logging.getLogger(__name__)


@api_view(['POST'])
def seeding(request):
    # take cell_id, and slot_id from resuest
    user = request.user
    cell_id = request.POST.get('cell_id')
    slot_id = request.POST.get('slot_id')
    if not cell_id or not slot_id:
        return Response('Required data not fullfilled.', status=400)

    try:
        cell = Cell.objects.get(id=cell_id, user=user)
        slot = Slot.objects.get(id=slot_id, user=user)
    except (Cell.DoesNotExist, Slot.DoesNotExist):
        return Response('Cell or Slot not found error.', status=400)

    if not isinstance(slot.item, SeedItem):
        return Response('Selected item is not a seed type.', status=400)

    if cell.is_blank_cell():
        return Response('Selected cell is not blank', status=400)

    with transaction.atomic():
        cell.crop = slot.item.crop_species.create_crop()
        cell.save()
        slot.item.delete()
        logger.info(f'Seeding success! {cell.crop.crop_species.name} at '
                    f'({cell.position_x}, {cell.position_y})')

    return Response({"status": "Success!"})


@api_view(['POST'])
def harvest(request):
    # take cell_id from resuest
    user = request.user
    cell_id = request.POST.get('cell_id')
    if not cell_id:
        return Response('Required data not fullfilled.', status=400)

    try:
        cell = Cell.objects.get(id=cell_id, user=user)
    except (Cell.DoesNotExist, Slot.DoesNotExist):
        return Response('Cell or Slot not found error.', status=400)

    if not cell.is_availbe_for_harvest():
        return Response('Cell cannot be harvested.', status=400)

    with transaction.atomic():
        item_list = cell.crop.get_harvest_reward()
        inventory = user.inventory
        inventory.insert_item(item_list)

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