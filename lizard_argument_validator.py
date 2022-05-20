import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Validate the argument of lizard")
parser.add_argument(
    "-language",
    choices=[
        "cpp",
        "java",
        "csharp",
        "javascript",
        "python",
        "objectivec",
        "ttcn",
        "ruby",
        "php",
        "swift",
        "scala",
        "GDScript",
        "go",
        "lua",
        "rust",
        "typescript",
        "None",
    ],
    type=str,
)
parser.add_argument("-verbose", choices=["true", "false"], type=str)
parser.add_argument("-CCN", type=int)
parser.add_argument("-input_file", type=str)
parser.add_argument("-output_file", type=str)
parser.add_argument("-length", type=int)
parser.add_argument("-arguments", type=str)
parser.add_argument("-warnings_only", choices=["true", "false"], type=str)
parser.add_argument("-warning_msvs", choices=["true", "false"], type=str)
parser.add_argument("-ignore_warnings", type=str)
parser.add_argument("-exclude", type=str)
parser.add_argument("-working_threads", type=int)
parser.add_argument("-xml", choices=["true", "false"], type=str)
parser.add_argument("-html", choices=["true", "false"], type=str)
parser.add_argument("-modified", choices=["true", "false"], type=str)
parser.add_argument("-extension", type=str)
parser.add_argument("-sort", type=str)
parser.add_argument("-Threshold", type=str)
parser.add_argument("-whitelist", type=Path)

args = parser.parse_args()

print(args)


def add_double_quotes(x):
    x = str(x)
    return '"' + x + '"'


lizard_args: list = []

if args.language != "None":
    lizard_args.extend(["--language", args.language])

if args.verbose.lower() == "true":
    lizard_args.append("--verbose")

lizard_args.extend(["--CCN", args.CCN])

if args.input_file != "None":
    input_file_path = Path(args.input_file)
    lizard_args.extend(["--input_file", add_double_quotes(input_file_path)])

if args.output_file != "None":
    output_file_path = Path(args.output_file)
    lizard_args.extend(["--output_file", add_double_quotes(output_file_path)])

lizard_args.extend(["--length", args.length])

if args.arguments != "None":
    arguments_int: int = int(args.arguments)
    lizard_args.extend(["--arguments", arguments_int])

if args.warnings_only.lower() == "true":
    lizard_args.append("--warnings_only")

if args.warning_msvs.lower() == "true":
    lizard_args.append("--warning_msvs")

if args.ignore_warnings != "None":
    lizard_args.extend(["--ignore_warnings", add_double_quotes(args.ignore_warnings)])

if args.exclude != "None":
    lizard_args.extend(["--exclude", add_double_quotes(args.exclude)])

lizard_args.extend(["--working_threads", args.working_threads])

if args.xml.lower() == "true":
    lizard_args.append("--xml")

if args.html.lower() == "true":
    lizard_args.append("--html")

if args.extension != "None":
    lizard_args.extend(["--extension", add_double_quotes(args.extension)])

if args.sort != "None":
    lizard_args.extend(["--sort", add_double_quotes(args.sort)])

if args.Threshold != "None":
    lizard_args.extend(["--Threshold", add_double_quotes(args.Threshold)])

if args.whitelist != "None":
    whitelist_path = Path(args.whitelist)
    lizard_args.extend(["--whitelist", add_double_quotes(whitelist_path)])

print(" ".join(map(str, lizard_args)))
