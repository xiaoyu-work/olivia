## OpenVINO EP

- Check numpy version: `pip install "numpy<2.0"`
- If you saw some error like "no openvino.dll" found, please run `setupvars.ps1` or `setupvars.bat` from `C:\Program Files (x86)\Intel\openvino_2025.1.0`.
- Auto-activate openvino env setup when conda env is initialized: add a new file `<conda_env_path>\etc\conda\activate.d\openvino_vars.ps1`:
    ```
    $OPENVINO_SETUP_SCRIPT_PATH = "C:\Program Files (x86)\Intel\openvino_2025.1.0\setupvars.ps1"
    if (Test-Path $OPENVINO_SETUP_SCRIPT_PATH) {
        . $OPENVINO_SETUP_SCRIPT_PATH
    } else {
        Write-Warning "OpenVINO setupvars.ps1 not found at $OPENVINO_SETUP_SCRIPT_PATH"
    }
    ```

    Conda env will automatically run all ps1 file in activate.d when initialized.