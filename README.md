# Multisouce downloader
Command line script for downloading a file via HTTP protocol from a (or multiple) URL resource(s) in multiple parts.

`Python 3.9.7` + `asyncio` + `aiohttp`

## Use
Clone repo to a local environment.

Check/run `deploy.sh`: get requirements, check inputs (or go with defaults), deploy.

`$python3 multisource_downloader.py`

- default inputs are set to:
    - url to publicly hosted file (~70MB)
    - async multipart download
        - 7 parts
    - download saved to local directory

## Inputs
Core inputs are hardcoded in `main.py` as:

- `mode`
    - the download mode: synchronous (requests) or asynchronous (asyncio + aiohttp)
- `number_sources` 
    - number of sections into which the file should be split (if range downloads are permitted, else will be set to 1)
- `url`
    - demo: identifies a ~70 MB .mov file hosted on github
- `num_repeats`
    - default = 1
    - set > 1 to average downloads for timing averages

## ETag/checksum
The test file has a (weak) ETag.
- validate_etag() cycles through `hashlib` algorithms applied to the final `byte_file`
    - no checksum match identified via hashlib library

TODO
- track down details of github's etag-generation protocol

## Tests
TODO
Current tests not included (patchy) - to be updated.
