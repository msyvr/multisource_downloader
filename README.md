# Multisouce downloader
Command line script for downloading a file via HTTP protocol from a (or multiple) URL resource(s) in multiple parts.

`Python 3.9.7` + `asyncio` + `aiohttp`

## Use
Clone repo to a local environment.

Check/run `run.sh`: get requirements, check inputs (or go with defaults), deploy.

- entry point: `main.py`

- default inputs are set to:
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
Core inputs are hardcoded in `main.py`:

They are:
- `'mode'`
    - the download mode: synchronous (requests) or asynchronous (asyncio + aiohttp)
- `'number_sources'` 
    - number of sections into which the file should be split (if range downloads are permitted)

Additional inputs in `get_inputs.py`:
- `'num_runs'`
    - number of repeat runs: for computing average performance metrics
    - time to download all the file sections
    - time to assemble the file sections
    - time to write the assembled file to disk/local dir
- `'url'`
    - currently, identifies a ~70 MB .mov file hosted on github

## ETag/checksum
The test tile has a (weak) ETag. The checksum is not identifying a match.
- validate_etag() cycles through `hashlib` algorithms applied to the final `byte_file`
    - this may be an error: multiple checksums for partial download may need to be combined
    - !there very well may be a well known solution (did not dig yet) 

## Tests
TODO
Current tests not included (patchy) - to be updated.
