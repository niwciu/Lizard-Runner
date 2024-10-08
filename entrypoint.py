import argparse
import subprocess
import sys
import os
import os.path
from pathlib import Path

print("::group::ValidateArguments")

parser = argparse.ArgumentParser(description="Validate the argument of lizard")
parser.add_argument("path", type=str)
parser.add_argument("cli_output_file", type=Path)
parser.add_argument("timeout", type=int)
parser.add_argument("language", type=str)
parser.add_argument("verbose", choices=["true", "false"], type=str)
parser.add_argument("CCN", type=int)
parser.add_argument("input_file", type=str)
parser.add_argument("output_file", type=str)
parser.add_argument("length", type=int)
parser.add_argument("arguments", type=int)
parser.add_argument("warnings_only", choices=["true", "false"], type=str)
parser.add_argument("warning_msvs", choices=["true", "false"], type=str)
parser.add_argument("ignore_warnings", type=int)
parser.add_argument("exclude", type=str)
parser.add_argument("working_threads", type=int)
parser.add_argument("xml", choices=["true", "false"], type=str)
parser.add_argument("html", choices=["true", "false"], type=str)
parser.add_argument("modified", choices=["true", "false"], type=str)
parser.add_argument("extension", type=str)
parser.add_argument("sort", type=str)
parser.add_argument("Threshold", type=str)
parser.add_argument("whitelist", type=Path)
parser.add_argument("optional_args", type=str)

args = parser.parse_args()


def surround_double_quotes(x: str):
    return '"' + str(x) + '"'


def is_safe_path(path):
    return os.path.isabs(path) and not os.path.islink(path) and '..' not in path

def set_action_output(output_name, value) :
    output_path = os.getenv('GITHUB_OUTPUT')

    if output_path:
        if is_safe_path(output_path):
            try:
                with open(output_path, "a") as f:
                    print("{0}={1}".format(output_name,value), file=f)
            except OSError as e:
                print("::set-output name={0}::{1}".format(output_name, value))
        else:
            print("::set-output name={0}::{1}".format(output_name, value))
    else:
        print("::set-output name={0}::{1}".format(output_name, value))

lizard_args: list = ["lizard"]

language_list: list = [
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
]
lizard_paths: list = []
if args.path != "":
    args_paths: list = args.path.split()
    for path in args_paths:
        lizard_paths.append(Path(path))

if args.language != "":
    args_languages: list = args.language.split()
    for language in args_languages:
        if language in language_list:
            lizard_args.extend(["--language", language])
        else:
            raise ValueError("Not present in the list of available languages.")


if args.verbose.lower() == "true":
    lizard_args.append("--verbose")

lizard_args.extend(["--CCN", args.CCN])

if args.input_file != "":
    input_file_path = Path(args.input_file)
    lizard_args.append("-f" + surround_double_quotes(input_file_path))

output_file_flag = False
if args.output_file != "":
    output_file_path = Path(args.output_file)
    lizard_args.append("-o" + surround_double_quotes(output_file_path))
    output_file_flag = True

lizard_args.extend(["--length", args.length])

if args.arguments != "":
    arguments_int: int = int(args.arguments)
    lizard_args.extend(["--arguments", arguments_int])

if args.warnings_only.lower() == "true":
    lizard_args.append("--warnings_only")

if args.warning_msvs.lower() == "true":
    lizard_args.append("--warning_msvs")

lizard_args.extend(["--ignore_warnings", args.ignore_warnings])

if args.exclude != "":
    args_exclude: list = args.exclude.split()
    for exclude in args_exclude:
        lizard_args.append("-x" + surround_double_quotes(exclude))

lizard_args.extend(["--working_threads", args.working_threads])

if args.xml.lower() == "true":
    lizard_args.append("--xml")

if args.html.lower() == "true":
    lizard_args.append("--html")

if args.extension != "":
    lizard_args.append(["-E" + surround_double_quotes(args.extension)])

if args.sort != "":
    lizard_args.extend(["--sort", args.sort])


if args.Threshold != "":
    args_threshold: list = args.Threshold.split()
    for threshold in args_threshold:
        lizard_args.append("-T" + surround_double_quotes(threshold))

if args.whitelist != "":
    whitelist_path = Path(args.whitelist)
    lizard_args.append("-W" + surround_double_quotes(whitelist_path))

if args.optional_args != "":
    lizard_args.append(args.optional_args)
lizard_args.extend(lizard_paths)

command = list(map(str, lizard_args))

print("\033[32m" + "Succes Validation" + "\033[0m")

print("::group::RunningLizard")
print(" ".join(command))

result = subprocess.run(
    [" ".join(command)],
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    timeout=args.timeout,
)
print(result.stdout)
print(result.stderr)

with open(args.cli_output_file, mode="w") as f:
    f.write(result.stdout)

set_action_output("cli_output_path",str(args.cli_output_file))

if output_file_flag:
    set_action_output("result_output_path",str(output_file_path))

sys.exit(result.returncode)
