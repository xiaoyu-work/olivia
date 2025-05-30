# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
import json
import os

import pytest

from olive.common.utils import retry_func, run_subprocess

from ..utils import get_example_dir


@pytest.fixture(scope="module", autouse=True)
def setup():
    """Setups any state specific to the execution of the given module."""
    os.chdir(get_example_dir("mobilenet/qnn"))

    retry_func(run_subprocess, kwargs={"cmd": "python download_files.py", "check": True})


def test_mobilenet_qnn_ep():
    from olive.workflows import run as olive_run

    with open("mobilenet_qnn_ep.json") as f:
        config = json.load(f)

    # only run optimization here, needs qnn-ep to run evaluation
    del config["evaluators"], config["evaluator"]

    # need to pass [] since the parser reads from sys.argv
    workflow_output = olive_run(config, tempdir=os.environ.get("OLIVE_TEMPDIR", None))

    # make sure it only ran for npu-qnn
    assert len(workflow_output.get_available_devices()) == 1
    assert workflow_output["npu"] is not None
    assert workflow_output["npu"]["QNNExecutionProvider"] is not None
