import json
import subprocess
from collections.abc import Iterable
from typing import Literal


class BrightDataScraper:
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key

    def scrape_channels(
        self,
        channel_urls: Iterable[str],
        num_of_posts: int,
        start_date: str,
        end_date: str,
        order_by: str,
        country: str,
    ) -> None | dict:
        dataset_id = 'gd_lk56epmy2i5g7lzu0k'
        endpoint = f'https://api.brightdata.com/datasets/v3/trigger?dataset_id={dataset_id}&include_errors=true&type=discover_new&discover_by=url'

        payload = [
            {
                'url': url,
                'num_of_posts': num_of_posts,
                'start_date': start_date,
                'end_date': end_date,
                'order_by': order_by,
                'country': country,
            }
            for url in channel_urls
        ]

        # Define the curl command
        command = [
            'curl',
            '-H',
            f'Authorization: Bearer {self.__api_key}',
            '-H',
            'Content-Type: application/json',
            '-d',
            json.dumps(payload),  # Convert payload to JSON string
            endpoint,
        ]

        # Execute the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=False)

        # Check if the command was successful
        if result.returncode == 0:
            try:
                # Parse and return the JSON response
                return json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                print('Failed to parse JSON response.')
                return None
        else:
            # Print and return the error if the command fails
            print(f'Error: {result.stderr}')
            return None

    def get_progress(self, snapshot_id: str) -> None | dict:
        command = [
            'curl',
            '-H',
            f'Authorization: Bearer {self.__api_key}',
            f'https://api.brightdata.com/datasets/v3/progress/{snapshot_id}',
        ]

        result = subprocess.run(command, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            return json.loads(result.stdout.strip())

        print(f'Error: {result.stderr}')
        return None

    def get_output(
        self,
        snapshot_id: str,
        *,
        output_format: Literal['json', 'jsonl'] = 'jsonl',
    ) -> None | list[dict]:
        command = [
            "curl",
            "-H", f"Authorization: Bearer {self.__api_key}",
            f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format={output_format}"
        ]

        result = subprocess.run(command, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            json_lines = result.stdout.strip().split("\n")
            return [json.loads(line) for line in json_lines]

        print(f"Error: {result.stderr}")
        return None
