import os
import re
import sys


INSTRUCTION_PATTERN = re.compile(
    r'(?P<instruction>\w{3}) (?P<argument>[\+\-]{1}\d+)\n?')


def instruction_acc(runtime, argument):
    return {**runtime, "acc": runtime["acc"] + argument}


def instruction_jmp(runtime, argument):
    return {**runtime, "pointer": runtime["pointer"] + argument}


def instruction_nop(runtime, argument):
    return runtime


INSTRUCTIONS = {
    "acc": instruction_acc,
    "nop": instruction_nop,
    "jmp": instruction_jmp,
}


def parse_program(stream):
    specs = (INSTRUCTION_PATTERN.match(line) for line in stream)
    return [{"instruction": spec.group('instruction'), "argument": int(spec.group('argument'))} for spec in specs]


def run_program(program):
    history = []
    runtime = {"pointer": 0, "acc": 0}

    while runtime["pointer"] < len(program):
        pointer = runtime["pointer"]
        argument = program[pointer]["argument"]
        run_instruction = INSTRUCTIONS[program[pointer]["instruction"]]
        runtime = run_instruction(runtime, argument)
        runtime["pointer"] = pointer + \
            1 if pointer == runtime["pointer"] else runtime["pointer"]

        if runtime["pointer"] in history:
            break

        history.append(pointer)

    return runtime


def swap_at_line(program, line_number):
    swapped = {**program[line_number], "instruction": "nop" if program[line_number]
               ["instruction"] == "jmp" else "jmp"}
    return program[:line_number] + [swapped] + program[line_number + 1:]


program = parse_program(sys.stdin)

print("solution 1:", run_program(program)["acc"])

swappable_lines = (line_number for line_number, spec in enumerate(
    program) if spec["instruction"] in ["nop", "jmp"])
edited_programs = (swap_at_line(program, line_number)
                   for line_number in swappable_lines)
runtimes = (run_program(edited_program) for edited_program in edited_programs)
finished_runtimes = [
    runtime for runtime in runtimes if runtime["pointer"] == len(program)]

print("solution 2:", finished_runtimes[0]["acc"])
