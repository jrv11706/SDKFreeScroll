from typing import Any
from mods_base import build_mod, keybind, get_pc, hook

from keybinds import EInputEvent
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct

be_shooting = False

@keybind(identifier="Free-Scroll Fire",
         key= "Eight",
         event_filter=EInputEvent.IE_Pressed)
def fire_keybind_pressed() -> None:
    global be_shooting
    be_shooting = True

@keybind(identifier="Free-Scroll Fire",
         key= "Eight",
         event_filter=EInputEvent.IE_Released)
def fire_keybind_released() -> None:
    global be_shooting
    be_shooting = False

@keybind("Free-Scroll Interact", "Nine")
def fs_interact() -> None:
    pc = get_pc()
    if not pc:
        return

    for i in range(20):
        pc.Use()

@hook("WillowGame.WillowPlayerController:PlayerWalking.PlayerMove")
def actor_tick(
    obj: UObject,
    args: WrappedStruct,
    _ret: Any,
    _func: BoundFunction
) -> None:
    if be_shooting:
        pc = get_pc()
        if not pc:
            return

        pc.StartFire()
        pc.StopFire()

build_mod(
    name="Free-Scroll Keybinds",
    author="piikyu",
    description="Set keybinds to spam inputs!",
    version="0.3",
    keybinds=[
        fire_keybind_pressed,
        fire_keybind_released,
        fs_interact,
    ],
)