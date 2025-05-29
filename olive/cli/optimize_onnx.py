# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
import subprocess
from argparse import ArgumentParser
from copy import deepcopy

from olive.cli.base import (
    BaseOliveCLICommand,
    add_input_model_options,
    add_logging_options,
    add_remote_options,
    add_save_config_file_options,
    add_shared_cache_options,
    get_input_model_config,
    update_remote_options,
    update_shared_cache_options,
)
from olive.common.utils import set_nested_dict_value


class OptimizeOnnxGraphCommand(BaseOliveCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        sub_parser = parser.add_parser("optimize-onnx-graph", help="Optimize ONNX graph.")

        # model options
        add_input_model_options(
            sub_parser, enable_hf=True, enable_hf_adapter=True, enable_pt=True, default_output_path="onnx-model"
        )

        # remote options
        add_remote_options(sub_parser)
        add_logging_options(sub_parser)
        add_save_config_file_options(sub_parser)
        add_shared_cache_options(sub_parser)
        sub_parser.set_defaults(func=OptimizeOnnxGraphCommand)

    def run(self):
        self._install_packages("onnxscript", "onnxoptimizer")
        self._run_workflow()

    def _install_packages(self, *packages):
        cmd = ["pip", "install", "--upgrade", *packages]
        print(f"Installing packages: {cmd}")
        subprocess.check_call(cmd)

    def _get_run_config(self, tempdir: str) -> dict:
        config = deepcopy(TEMPLATE)

        input_model_config = get_input_model_config(self.args)
        assert input_model_config["type"].lower() == "onnxmodel", "Only ONNX model is supported for optimization."

        to_replace = [
            ("input_model", input_model_config),
            ("output_dir", self.args.output_path),
            ("log_severity_level", self.args.log_level),
        ]

        for keys, value in to_replace:
            if value is None:
                continue
            set_nested_dict_value(config, keys, value)
        update_remote_options(config, self.args, "optimize-onnx-graph", tempdir)
        update_shared_cache_options(config, self.args)

        return config


TEMPLATE = {
    "systems": {
        "local_system": {
            "type": "LocalSystem",
            "accelerators": [{"device": "cpu", "execution_providers": ["CPUExecutionProvider"]}],
        }
    },
    "passes": {
        "o": {
            "type": "OnnxPeepholeOptimizer",
        }
    },
    "host": "local_system",
    "target": "local_system",
    "no_artifacts": True,
}
