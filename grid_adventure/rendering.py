import os
from pathlib import Path
from grid_universe.renderer.texture import TextureMap


# Default asset root directory.
DEFAULT_ASSET_ROOT = os.path.join(Path(__file__).parent.resolve(), "assets")

# Mapping from (appearance name, properties) to texture file/directory names.
TEXTURE_MAP: TextureMap = TextureMap(
    {
        ("human", tuple([])): "human",
        ("human", tuple(["dead"])): "sleeping",
        ("coin", tuple([])): "coin",
        ("gem", tuple(["requirable"])): "gem",
        ("metalbox", tuple([])): "metalbox",
        ("box", tuple(["pushable"])): "box",
        ("robot", tuple([])): "robot",
        ("key", tuple([])): "key",
        ("portal", tuple([])): "portal",
        ("door", tuple(["locked"])): "locked",
        ("door", tuple([])): "opened",
        ("shield", tuple(["immunity"])): "shield",
        ("ghost", tuple(["phasing"])): "ghost",
        ("boots", tuple(["speed"])): "boots",
        ("lava", tuple([])): "lava",
        ("exit", tuple([])): "exit",
        ("wall", tuple([])): "wall",
        ("floor", tuple([])): "floor",
    }
)
