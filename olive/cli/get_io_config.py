# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
from argparse import ArgumentParser

from olive.cli.base import BaseOliveCLICommand
from olive.model.handler.hf import HfModelHandler


class GetIoConfigCommand(BaseOliveCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        sub_parser = parser.add_parser("io", help="Get IO config for a Huggingface model.")

        # model options
        sub_parser.add_argument("-m", type=str, help="Huggingface model name")
        sub_parser.add_argument("-t", "--task", type=str, help="Task for which the huggingface model is used.")

        sub_parser.set_defaults(func=GetIoConfigCommand)

    def run(self):
        model_handler = HfModelHandler(model_path=self.args.m, task=self.args.task)
        io_config = model_handler.io_config
        dummy_inputs = model_handler.get_dummy_inputs()

        input_names = io_config["input_names"]
        input_shapes = []
        for input_name in input_names:
            input_shapes.append(list(dummy_inputs[input_name].shape))
        io_config["input_shapes"] = input_shapes

        print(f"model: {self.args.m} task: {self.args.task} has IO config: {io_config}")
