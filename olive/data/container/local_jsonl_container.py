# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

from typing import ClassVar

from olive.data.constants import DataComponentType, DataContainerType
from olive.data.container.data_container import DataContainer
from olive.data.registry import Registry


@Registry.register(DataContainerType.DATA_CONTAINER)
class LocalJsonlContainer(DataContainer):
    """A data container for local JSONL files.

    This container is designed to load data from local JSON files without requiring
    a data_name parameter, unlike the HuggingfaceContainer.

    Example usage:
        local_json_config = DataConfig(
            name="my_local_data",
            type="LocalJsonContainer",
            load_dataset_config=DataComponentConfig(
                type="local_json_dataset",
                params={
                    "data_files": ["path/to/file1.json", "path/to/file2.json"],
                    "split": None,  # optional
                }
            ),
            pre_process_data_config=DataComponentConfig(
                type="huggingface_pre_process",
                params={
                    "text_cols": "text",
                    "max_seq_len": 1024,
                    "add_special_tokens": False,
                    "max_samples": 256
                }
            ),
            dataloader_config=DataComponentConfig(
                type="default_dataloader",
                params={
                    "batch_size": 1
                }
            )
        )
    """

    default_components_type: ClassVar[dict] = {
        DataComponentType.LOAD_DATASET.value: "local_jsonl_dataset",
        DataComponentType.PRE_PROCESS_DATA.value: "huggingface_pre_process",
    }
    
    # Task-specific component mappings, similar to HuggingfaceContainer
    task_type_components_map: ClassVar[dict] = {
        "text-generation": {
            DataComponentType.PRE_PROCESS_DATA.value: "text_generation_huggingface_pre_process",
        },
        "ner": {
            DataComponentType.PRE_PROCESS_DATA.value: "ner_huggingface_preprocess",
        },
        "audio-classification": {
            DataComponentType.PRE_PROCESS_DATA.value: "audio_classification_pre_process",
        },
    } 