# Maestro

Maestro is a simple orchestration tool implemented with pure Python (and only
standard libraries). It executes a series of steps defined in a workflow specification
(a JSON file).

## File specification

DAGs can be defined as a JSON file with four main fields:

```json
{
    "name": "...",
    "inputs": {"..."},
    "steps": ["..."],
    "outputs": {"..."}
}
```

All of them are relatively self-explanatory: you must define the workflow's name, its
inputs (as key/value pairs, so they can be referenced later), its steps, and its outputs
(which are also named, for easier comprehension).

Steps inside the `"steps"` array must be defined with the following specification:

```json
{
    "name": "...",
    "type": "...",
    "path": "...",
    "depends_on": ["..."],
    "inputs": {"..."},
    "outputs": ["..."]
}
```

The `"type"` field informs which kind of step it is, while the `"path"` field is used by
the orchestrator to resolve the executable's location. The `"depends_on"` field is optional
and, if passed, will be used to block the step's execution while the required steps are
not yet complete.

You can pass an entity's input/output to another step using the reference format
`{{ <entity name>.<inputs/outputs>.<variable name> }}`. For instance, the following
spec will use the value of `"x"` specified in the workflow `my_workflow` inputs:

```json
{
    "inputs": {
        "x": "{{ my_workflow.inputs.x }}"
    },
}
```

This means that names should be unique across an entire specification, so that reference
variables can be correctly resolved. Also, if a step requires an output of another step,
you **must** explictly define the `"depends_on"` field.

Currently the only supported step type is `python_step`. In this type, the `"path"` field
must be a fully qualified Python function path. For instance, the function `pow()` present
in Python's `math` module would be called with `math.pow`. The inputs are passed as
sequential arguments for the function. If you want to use user-defined functions, you must
organize your project as a Python module and execute Maestro outside of it (as you can see
in the [Examples](#examples) section).

## Installation

There is no package specification for the project (i.e. you can't install it using pip),
but since Maestro is implemented using only standard libraries, you can "install" it by
adding the `maestro/` directory to a directory present in your Python PATH.

Maestro was developed and tested in Python 3.8.

## Usage

To run the orchestrator, you must execute its main module while passing the path (absolute
or relative) to a JSON file containing the workflow specification:

```bash
python -m maestro [WORKFLOW_PATH]
```

## Examples

Inside the `examples/` directory you can find examples of workflow definitions alongside
user-defined code that is used inside these workflows. It is recommended to run these
examples at the repository's root, not only because this way the `maestro` library will
be resolved, but the `examples` library as well.

For instance, if you run `python -m maestro examples/workflows/compute_sum_of_squares.json`
you'll get the following output:

```
===========================================
     Workflow "compute_sum_of_squares"
===========================================

Inputs:
    - x: 4
    - y: 3

Steps:
    - square_x: SUCCESSFUL
    - square_y: SUCCESSFUL
    - sum_squares: SUCCESSFUL

Outputs:
    - sum_of_squares: 25
```
