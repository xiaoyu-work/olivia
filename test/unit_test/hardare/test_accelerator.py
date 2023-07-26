# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
import pytest

from olive.hardware.accelerator import AcceleratorLookup


class TestAcceleratorLookup:
    @pytest.mark.parametrize(
        "execution_providers_test",
        [
            (["CPUExecutionProvider"], None),
            (["CUDAExecutionProvider"], ["gpu"]),
            (["DmlExecutionProvider", "CUDAExecutionProvider"], ["gpu"]),
            (["QNNExecutionProvider", "CUDAExecutionProvider"], ["npu", "gpu"]),
        ],
    )
    def test_infer_accelerators_from_execution_provider(self, execution_providers_test):
        execution_providers, expected_accelerators = execution_providers_test
        actual_rls = AcceleratorLookup.infer_accelerators_from_execution_provider(execution_providers)
        assert actual_rls == expected_accelerators