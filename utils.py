import os
import requests
from tqdm import tqdm


def download_file(url: str, save_filename: str) -> None:
    """
    Download a file with a progress bar.

    The progress bar will display the size in binary units (e.g., KiB for kibibytes,
    MiB for mebibytes, GiB for gibibytes, etc.), which are based on powers of 1024.

    Args:
        url: The URL of the data.
        save_filename: The path to save the data.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
        OSError: If there is an issue with writing the file.
    """
    if not os.path.exists(path=save_filename):
        print(f"Downloading: {url} -> {save_filename}")
        try:
            with requests.get(url=url, stream=True) as response:
                response.raise_for_status()
                total_size_in_bytes = int(
                    response.headers.get(key="content-length", default=0)
                )
                print(f"Total size: {total_size_in_bytes:,} bytes")
                block_size = 1024
                progress_bar = tqdm(
                    total=total_size_in_bytes, unit="iB", unit_scale=True
                )
                with open(file=save_filename, mode="wb") as file:
                    for data in response.iter_content(chunk_size=block_size):
                        progress_bar.update(n=len(data))
                        file.write(data)
                progress_bar.close()
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
        except OSError as e:
            print(f"Error writing file: {e}")
        finally:
            if "progress_bar" in locals():
                progress_bar.close()
    else:
        print(f"File already exists: {save_filename}")
