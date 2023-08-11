# import sys
import open3d as o3d
import numpy as np
from numpy.typing import NDArray
from PIL import Image
import click
from pathlib import Path


def get_uv(vertex_colors: NDArray, colors: int):
    xsize = colors
    xstep = 1 / xsize

    ysize = colors**2
    ystep = 1 / ysize

    uvs = vertex_colors * (xsize - 1)

    x = uvs[:, 0]
    z = uvs[:, 2].round() * xsize
    y = z + uvs[:, 1]

    uvs = np.column_stack((x, y)).astype(np.float64)
    uvs /= [xsize, xsize**2]

    uvs[:, 1] = (1 - ystep) - uvs[:, 1]
    uvs += [xstep / 2, ystep / 2]

    return np.clip(uvs, 0, 1)


@click.command()
@click.argument("in_mesh", type=click.Path(exists=True, dir_okay=True, path_type=Path), required=True)
@click.argument("out_mesh", type=click.Path(path_type=Path), required=True)
@click.argument("out_texture", type=click.Path(path_type=Path), required=True)
@click.option("--colors", type=int, default=64)
def main(in_mesh: Path, out_mesh: Path, out_texture: Path, colors: int):
    in_mesh_str = str(in_mesh.resolve())

    print(f"loading {in_mesh_str}")
    mesh = o3d.io.read_triangle_mesh(in_mesh_str)

    print("calculating uv")
    vertex_colors = np.asarray(mesh.vertex_colors)
    triangles = np.asarray(mesh.triangles)

    vertex_colors = vertex_colors[triangles]
    vertex_colors = np.average(vertex_colors, axis=1)
    # colors = colors[:, 0]

    uvs = get_uv(vertex_colors, colors)
    uvs = np.repeat(uvs, repeats=3, axis=0)

    mesh.triangle_uvs = o3d.utility.Vector2dVector(uvs)

    # create palette
    z, y, x = np.mgrid[0:colors, 0:colors, 0:colors]
    palette3d = np.stack((x, y, z), axis=-1) / (colors - 1)
    palette2d = palette3d.reshape(colors**2, colors, 3)

    palette_png = (palette2d * 255).astype(np.ubyte)

    out_texture_str = str(out_texture.resolve())
    print(f"saving palette to {out_texture_str}")
    im = Image.fromarray(palette_png, "RGB")
    im.save(out_texture_str)

    out_mesh_str = str(out_mesh.resolve())
    print(f"saving mesh to {out_mesh_str}")
    o3d.io.write_triangle_mesh(out_mesh_str, mesh)

    print("done")


if __name__ == "__main__":
    main()
