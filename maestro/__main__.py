"""Command line interface implementation for module."""

import argparse
import json
from typing import Any, Dict

from maestro.workflow import Workflow
from maestro.workflow.formatter import ExecutionLogFormatter


def init_parser() -> argparse.ArgumentParser:
    """Initialize parser for the CLI."""
    parser = argparse.ArgumentParser(
        usage="python -m maestro [WORKFLOW_PATH]",
        description="Command line interface to execute Maestro workflows.",
    )
    parser.add_argument(
        "workflow_path", type=str, action='store', help="path to workflow file"
    )
    return parser


def get_workflow_json(workflow_path: str) -> Dict[str, Any]:
    """Get workflow JSON specification from a file path."""
    with open(workflow_path, "r", encoding="utf-8") as file_descriptor:
        return json.load(file_descriptor)


def command_line_interface() -> None:
    """Execute the command line interface script for the Maestro library."""
    args = init_parser().parse_args()

    workflow_spec = get_workflow_json(args.workflow_path)
    workflow = Workflow.from_dict(workflow_spec)
    outputs = workflow.execute()

    print(ExecutionLogFormatter(
        workflow_name=workflow.name,
        workflow_inputs=workflow.inputs,
        execution_context=workflow.last_execution,
        execution_outputs=outputs
    ).format())


if __name__ == "__main__":
    command_line_interface()
