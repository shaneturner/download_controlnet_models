import os
import requests
from tqdm import tqdm
from urllib.parse import unquote, urlparse

# File URLs for Controlnet Models from Huggingface
file_urls = ['https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge.pth?download=true', 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime.pth?download=true']

# Destination folder where the files will be saved. Replace with another directory if you dont want to use the current directory.
destination_folder = os.getcwd()

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

def sanitize_filename(filename):
    # Check if the filename starts with a single-quote character. Fixed a bug with the get_filename_from_response function. Will be fixed later maybe.
    if filename.startswith("'"):
        # Remove the single-quote character from the beginning
        filename = filename[1:]

    return filename

# Function to get the filename from the server response
def get_filename_from_response(response):
    content_disposition = response.headers.get('content-disposition')
    if content_disposition:
        _, params = content_disposition.split(';', 1)
        for param in params.split(';'):
            if 'filename*' in param:
                _, filename = param.split("'", 1)
                sanitized_filename = sanitize_filename(filename)
                return unquote(sanitized_filename)
            elif 'filename=' in param:
                _, filename = param.split('=', 1)
                sanitized_filename = sanitize_filename(filename)
                return unquote(sanitized_filename)
    return None

def main():
    for url in file_urls:
        # Get the filename from the URL
        remote_filename = os.path.basename(urlparse(url).path)

        # Define the complete path for the local file
        local_file_path = os.path.join(destination_folder, remote_filename)

        # Check if the file with the same name exists locally
        if os.path.isfile(local_file_path):
            # Send a HEAD request to the URL to get remote file info
            with requests.head(url, allow_redirects=True) as response:
                if response.status_code == 200:
                    # Get the remote file size
                    remote_size = int(response.headers.get('content-length', 0))
                    # Get the local file size
                    local_size = os.path.getsize(local_file_path)

                    if remote_size == local_size:
                        print(f'{remote_filename} already exists and is the same size. Skipping. \n')
                        continue  # Skip downloading
                    else:
                        print(f'{remote_filename} exists but has a different size. Downloading...')

        # Send a GET request to the URL and follow redirects
        with requests.get(url, stream=True, allow_redirects=True) as response:
            if response.status_code == 200:
                # Get the filename from the server response
                file_name = get_filename_from_response(response)

                if file_name is not None:
                    # Define the complete path for the file
                    file_path = os.path.join(destination_folder, file_name)

                    # Display file name to download
                    print(f'File:  {file_name}')

                    # Initialize a progress bar
                    total_size = int(response.headers.get('content-length', 0))
                    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

                    # Download and save the file with streaming and progress display
                    with open(file_path, 'wb') as file:
                        for data in response.iter_content(chunk_size=8192):
                            file.write(data)
                            progress_bar.update(len(data))

                    progress_bar.close()
                    print(f'{file_name} downloaded successfully to {destination_folder}\n')
                else:
                    print(f'Failed to extract filename from {url}\n')
            else:
                print(f'Failed to download {url}\n')

    # All files have been checked and downloaded as needed
    print('\nAll files checked and downloaded as needed.\n')


if __name__ == "__main__":
    main()
    
