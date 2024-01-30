from ctypes import byref, c_long

from arepy.asset_store import AssetStore
from arepy.ecs.systems import System
from sdl2 import (SDL_Color, SDL_CreateTextureFromSurface, SDL_DestroyTexture,
                  SDL_FreeSurface, SDL_QueryTexture, SDL_Rect,
                  SDL_RenderCopyEx)
from sdl2.ext import Renderer
from sdl2.sdlttf import TTF_RenderText_Blended

from ..camera import Camera
from ..components import TextLabel


class RenderTextSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self.require_component(TextLabel)

    def update(
        self, renderer: Renderer, asset_store: AssetStore, camera: Camera
    ) -> None:
        for entity in self.get_system_entities():
            text_label = entity.get_component(TextLabel)
            if not text_label.draw:
                continue

            font = asset_store.get_font(text_label.font_id)
            surface = TTF_RenderText_Blended(
                font,
                text_label.text.encode("utf-8"),
                SDL_Color(
                    r=text_label.color[0],
                    g=text_label.color[1],
                    b=text_label.color[2],
                    a=255,
                ),
            )
            texture = SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
            SDL_FreeSurface(surface)
            w = c_long(0)
            h = c_long(0)
            SDL_QueryTexture(texture, None, None, byref(w), byref(h))
            dst_rect = SDL_Rect(
                x=int(
                    text_label.position[0] - camera.position[0]
                    if text_label.is_fixed
                    else text_label.position[0]
                ),
                y=int(
                    text_label.position[1] - camera.position[1]
                    if text_label.is_fixed
                    else text_label.position[1]
                ),
                w=w.value,
                h=h.value,
            )
            SDL_RenderCopyEx(
                renderer.sdlrenderer,
                texture,
                None,
                byref(dst_rect),
                0,
                None,
                0,
            )
