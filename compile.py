from styler import Renderer
import argparse as args
import os, time

parser = args.ArgumentParser("Renderer", description="""It Compiles the `.term` file into binary and give his respective output.The Important Tags, must understand the tags,
\n> uline : Underline any text
\n> t : tab space
\n> it : italic font
\n> bold : Bolder Font 
\n> dim : Dimmer Font 
\n> g : Normal Font or For special notation
\n> highlight=<color> : Highlight the text and choose your color which is green, blue, cyan, red and magenta but default it is YELLOW 
\n> Font Colors : red, cyan, blue, green and magenta color has use for Font Colors.""", add_help=True)
parser.add_argument("--file", "-f", type=str, help="Input File Path")
parser.add_argument("--out", "-o", type=bool, default=True)
parser.add_argument("--lambda", "-l", type=float, default=0.2)
parser.add_argument("--compile", "-c", type=bool, default=True)
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')

arg = parser.parse_args()
valuepoints = (dict(arg._get_kwargs()))


if valuepoints["lambda"] < 1 or valuepoints["lambda"] > 0:lambda_value = valuepoints["lambda"]
else: raise ValueError("Value must be in range of (0, 1].")

render = Renderer(lambda_value)

if not os.path.isfile(valuepoints["file"]) or not os.path.exists(valuepoints["file"]):
    raise FileNotFoundError("The File path doesnot exists.")

if valuepoints["compile"]:
    render.compiler(valuepoints["file"])
else:print("")
time.sleep(1/2)    
if valuepoints["out"]:
    print(render.render(valuepoints["file"].split(".")[-2]+f".bt-{valuepoints['lambda']}"))
else:print("")