from typing import List

from wecs.core import Component, System, UID, and_filter
from wecs.rooms import RoomPresence


@Component()
class Inventory:
    contents: list


@Component()
class Slots:
    slots: List[str]
    item_types: List[type]
    contents: List[UID]


@Component()
class Takeable:
    pass


@Component()
class TakeAction:
    item: UID


@Component()
class DropAction:
    item: UID


class TakeDropMixin:
    def can_take(self, item, entity):
        # If I have an inventory...
        if not entity.has_component(Inventory):
            print("{} has no inventory.".format(name))
            return False
        inventory = entity.get_component(Inventory).contents

        # ...and I am somewhere...
        if not entity.has_component(RoomPresence):
            print("Can't take objects from the roomless void.")
            return False
        presence = entity.get_component(RoomPresence)

        # ...and there is also an item there...
        if not item._uid in presence.presences:
            print("Item is not in the same room.")
            return False

        # ...that can be taken...
        if not item.has_component(Takeable):
            print("That can't be taken.")
            return False

        # ...then the item can be taken.
        return True

    def can_drop(self, item, entity):
        # If I have an inventory...
        if not entity.has_component(Inventory):
            print("{} has no inventory.".format(name))
            return False
        inventory = entity.get_component(Inventory).contents

        # ...with an item...
        if item._uid not in inventory:
            print("Item is not in inventory anymore.")
            return False

        # ...that can be dropped...
        if not item.has_component(Takeable):
            print("That can't be dropped.")
            return False

        # ...and there is somewhere to drop it into, ...
        if not entity.has_component(RoomPresence):
            print("Can't drop objects into the roomless void.")
            return False

        # ...then drop it like it's hot, drop it like it's hot.
        return True

    def take(self, item, entity):
        item.remove_component(RoomPresence)
        entity.get_component(Inventory).contents.append(item._uid)

    def drop(self, item, entity):
        room = self.world.get_entity(entity.get_component(RoomPresence).room)
        inventory = entity.get_component(Inventory).contents
        idx = inventory.index(item._uid)
        del inventory[idx]
        item.add_component(RoomPresence(room=room._uid, presences=[]))


class TakeOrDrop(TakeDropMixin, System):
    entity_filters = {
        'take': and_filter([TakeAction]),
        'drop': and_filter([DropAction]),
    }

    def update(self, entities_by_filter):
        for entity in entities_by_filter['take']:
            item = self.world.get_entity(entity.get_component(TakeAction).item)
            entity.remove_component(TakeAction)
            if self.can_take(item, entity):
                self.take(item, entity)
        for entity in entities_by_filter['drop']:
            item = self.world.get_entity(entity.get_component(DropAction).item)
            entity.remove_component(DropAction)
            if self.can_drop(item, entity):
                self.drop(item, entity)
