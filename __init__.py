from typing import Any
from mods_base import build_mod, keybind, get_pc, hook

from keybinds import EInputEvent
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct

be_shooting = False
be_interacting = False

@keybind(identifier="Free-Scroll Fire: On Press",
         key="Eight",
         event_filter=EInputEvent.IE_Pressed,
        )
def fire_keybind_pressed() -> None:
    '''Triggered when the key is pressed down. Sets a global variable to indicate that spam shooting should be attempted.'''
    global be_shooting
    be_shooting = True

@keybind(identifier="Free-Scroll Fire: On Release",
         key="Eight",
         event_filter=EInputEvent.IE_Released,
        )
def fire_keybind_released() -> None:
    '''Triggered when the key is released. Sets a global variable to indicate that spam shooting should not occur.'''
    global be_shooting
    be_shooting = False


@keybind(identifier="Free-Scroll Interact: On Press", 
         key="Nine",
         event_filter=EInputEvent.IE_Pressed,
        )
def interact_keybind_pressed() -> None:
    '''Triggered when the key is pressed down. Sets a global variable to indicate that spam interact should be attempted.'''
    global be_interacting
    be_interacting = True

@keybind(identifier="Free-Scroll Interact: On Release", 
         key="Nine",
         event_filter=EInputEvent.IE_Released,
        )
def interact_keybind_released() -> None:
    '''Triggered when the key is released. Sets a global variable to indicate that spam interacting should not occur.'''
    global be_interacting
    be_interacting = False


@hook("WillowGame.WillowPlayerController:PlayerTick")
def actor_tick(
    obj: UObject,
    args: WrappedStruct,
    _ret: Any,
    _func: BoundFunction
) -> None:
    '''Hooked into the PlayerTick function such that it should be executed every frame that the player exists, should translate pretty well to when the player can be doing things.'''    
    global be_interacting, be_shooting
    
    pc = get_pc()
    if not pc:
        return
    if not pc.Pawn:
        return

    if pc.Pawn.bViewingThirdPersonMenu:
        # Solves most cases of being stuck entering menus
        be_interacting = False

    if pc.Pawn.IsInjured():
        # Prevents picking up while in FFYL
        be_interacting = False

    if pc.Pawn.bInjuredDeadCameraActive:
        # Prevents shooting while dying (ragdoll)
        return

    if pc.Pawn.IsInjured() and not pc.Pawn.bInjuredIsCameraAnimPlaying:
        # Prevents shooting while transitioning into FFYL
        return
    
    if be_shooting:
        pc.StartFire()
        pc.StopFire()

    if be_interacting:
        pc.Use()
        pc.PickupSomething(0)

build_mod(
    name="Free-Scroll Keybinds",
    author="piikyu",
    description="Set keybinds to spam inputs!",
    version="0.4",
    keybinds=[
        fire_keybind_pressed,
        fire_keybind_released,
        interact_keybind_pressed,
        interact_keybind_released
    ],
)