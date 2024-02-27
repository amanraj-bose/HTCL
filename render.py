import argparse
import os
from styler import Renderer

parser = argparse.ArgumentParser("Render Binary FIle (ext.)")
parser.add_argument("--file", "-f", type=str or os.PathLike)
parser.add_argument("--run", "-r", type=bool, default=True)
args = parser.parse_args()
if os.path.exists(args.file):
    lambda_value = float("0."+str(args.file).split(".")[-1].split("-")[-1])
    render = Renderer(lambda_value)
    if args.run:
        print(render.render(args.file))