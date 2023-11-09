# Download control net models for automatic1111 ( a1111 ) controlnet extension
This script reads a list of file urls from the model_urls.txt file; then downloads them if they don't exist or are a different size.

## Steps

1. Place `dl_models.py` and `model_urls.txt` into the controlnet models directory
2. From your a1111 base directory this is often found in [base_directory]/extensions/sd-webui-controlnet/models
3. Run the script from the models directory with `python dl_models.py`

## Notes
This script requires the **tqdm** and **urllib** packages
You can install it with `pip install tqdm urllib`. You may want to use your venv if needed as this might already contain some of these packages.
