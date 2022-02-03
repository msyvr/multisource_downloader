# Multisouce downloader
Command line script for downloading a file via HTTP protocol from a (or multiple) URL resource(s) in multiple parts.

Python
    - 'async' mode: asyncio + aiohttp
    - 'sync' mode: requests

## Use
Clone repo to your local environment.
Check/run run.sh for requirements and how to launch downloads.
- entry point is main.py
- default inputs are:
    - url to publicly hosted file (~70MB)
    - download file in 7 sections
    - two sequential (whole) file downloads: 
        - 1x sync multipart download
        - 1x async multipart download
    - terminal output: 
        - basic timing reporting at the end of each download
        - informational print statements during execution
    - downloads saved to local directory
        - filename has sync/async signifier

## Inputs
Core inputs are hardcoded in main.py after if __name__ == "__main__"... 

They are:
- 'mode'
    - the download mode: synchronous (requests) or asynchronous (asyncio + aiohttp)
- 'number_sources' 
    - number of sections into which the file should be split (if range downloads are permitted)

Additional inputs in get_inputs.py:
- 'num_runs'
    - number of repeat runs: for computing average performance metrics
    - time to download all the file sections
    - time to assemble the file sections
    - time to write the assembled file to disk/local dir
- 'url'
    - currently, identifies a ~70 MB .mov file hosted on github

## ETag/checksum
The test tile has a (weak) ETag. The checksum is not identifying a match.
- validate_etag() cycles through hashlib algorithms applied to the final byte_file
    - this may be an error: multiple checksums for partial download may need to be combined
    - !there very well may be a well known solution (did not dig yet) 

## Tests
TODO