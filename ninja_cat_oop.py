from __future__ import annotations

from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum


class Color(str, Enum):
    RED = "\x1b[1;31m"
    GREEN = "\x1b[1;32m"
    YELLOW = "\x1b[1;33m"
    OFFSET = "\x1b[0m"

    def log(self, txt: str) -> None:
        match self:
            case Color.RED:
                txt = Color.RED + txt + Color.OFFSET
                print(txt)
            case Color.GREEN:
                txt = Color.GREEN + txt + Color.OFFSET
                print(txt)
            case Color.YELLOW:
                txt = Color.YELLOW + txt + Color.OFFSET
                print(txt)
            case _:
                raise Exception("color not found use Colo enum!")


@dataclass(frozen=False)
class PlayerInfo:
    level: int
    coin: float
    gem: float
    health: int

    _converted_coin: float = field(default=0.0, init=False)
    _gem_coin_trade: int = field(default=50, init=False)

    @property
    def is_need_help(self) -> bool:
        if self.health < 20:
            return True
        return False

    @property
    def convert_gem_to_coin(self) -> float:
        return self._converted_coin

    @convert_gem_to_coin.getter
    def convert_gem_to_coin(self) -> float:
        return self._converted_coin

    @convert_gem_to_coin.setter
    def convert_gem_to_coin(self, gem: float) -> None:
        if self.gem < gem:
            Color.RED.log("[ FAILED ]")
            raise Exception("Not Enought gem!")
        self.gem -= gem
        self._converted_coin = gem * self._gem_coin_trade
        self.coin += self._converted_coin


@dataclass(frozen=False)
class ItemInfo:
    price: float
    is_owned: bool
    is_locked: bool
    need_level_to_buy: int
    is_enable: bool
    label: str


# class ItemKind(str, Enum):
#     WEAPONS = "ItemKind@Weapons"
#     SUITS = "ItemKind@Suits"


@dataclass(frozen=True)
class Sword:
    info: ItemInfo
    power: float
    speed: float
    per_attack: float


@dataclass(frozen=True)
class Suit:
    info: ItemInfo
    strong: float


@dataclass(frozen=True)
class NinjaSword(Sword):
    pass


@dataclass(frozen=True)
class SnakeSword(Sword):
    pass


@dataclass(frozen=True)
class NinjaSuit(Suit):
    pass


class Action(ABC):
    @abstractmethod
    def attack(self) -> None:
        """Override"""


@dataclass(frozen=False)
class Cat(Action):
    info: PlayerInfo
    suit: Suit
    weapon: Sword

    def __post_init__(self) -> None:
        # Validation
        if not (
            self.weapon.info.is_owned
            and self.suit.info.is_owned
        ):
            print("Not buy yet!")
            raise Exception("Not buy yet!")

    def attack(self) -> None:
        if self.info.is_need_help:
            Color.YELLOW.log("[ WARN ] Go home!")
        print(f"[ HEALTH {self.info.health}% ]", "attack with", self.sword.info.label, "and", self.suit.info.label)

    @staticmethod
    def owned_items_count(items: dict):
        print('called')
        return len([i for i in items.values() if i.info.is_owned])

    @staticmethod
    def owned_items(items: dict):
        return (i for i in items.values() if i.info.is_owned)

    def toggle_enable_suit(self, suit: Suit) -> None:
        suit.info.is_enable = not suit.info.is_enable
        if suit.info.is_enable:
            self.suit = suit

    def toggle_enable_sword(self, sword: Sword) -> None:
        sword.info.is_enable = not sword.info.is_enable
        if sword.info.is_enable:
            self.sword = sword


@dataclass(frozen=True)
class Shop:
    @staticmethod
    def buy(
        item_info: ItemInfo,
        player: Cat
    ) -> None:
        player_info = player.info

        if item_info.is_owned:
            return
        if item_info.need_level_to_buy <= player_info.level:
            item_info.is_locked = False
        if item_info.is_locked:
            Color.RED.log("[ FAILED ]")
            raise Exception(f"Locked! need level {item_info.need_level_to_buy} and above")
        if item_info.price > player_info.coin:
            Color.RED.log("[ FAILED ]")
            raise Exception(f"Not Enought money")
        player_info.coin -= item_info.price
        item_info.is_owned = True

# Items Store
ITEMS = {
    # Swords
    "ninja_sword": NinjaSword(
        info = ItemInfo(
            price=0,  # original
            is_owned=True,
            is_locked=False,
            need_level_to_buy=0,
            is_enable=True,
            label="ninja_sword"
        ), 
        power = 12,
        speed = 10,
        per_attack = 1000 # 1s
    ),
    "snake_sword": SnakeSword(
        info = ItemInfo(
            price=200_000,
            is_owned=False,
            is_locked=True,
            need_level_to_buy=3,
            is_enable=False,
            label="snake_sword"
        ),
        power = 15,
        speed = 12,
        per_attack = 1000 # 1s
    ),

    # Suits
    "ninja_suit": NinjaSuit(
        info = ItemInfo(
            price=0,  # original
            is_owned=True,
            is_locked=False,
            need_level_to_buy=0,
            is_enable=False,
            label="ninja_suit"
        ),
        strong = 20
    )
}

my_info = PlayerInfo(
    level=5,
    coin=175_000.0,
    gem=500,
    health=100
)

# ----- Objects -----

me = Cat(
    info = my_info,
    weapon = ITEMS["ninja_sword"],
    suit = ITEMS["ninja_suit"]
)

# convert all gem to coin
all_gem = my_info.gem
my_info.convert_gem_to_coin = all_gem

Shop.buy(ITEMS["snake_sword"].info, me)

my_sword = ITEMS["snake_sword"]


me.toggle_enable_sword(my_sword)


print(f"{me.info.coin = }")
print(f"{me.info.gem = }")
# print(f"{me.sword=}")


me.attack()
