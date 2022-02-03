#! main.py

import requests, asyncio, aiohttp, hashlib, time
from get_input import get_input
from timing import reset_times, average_times

def multisource_download(mode: str, url : str, number_sources : int):
    '''
    Download url resource in multiple sections 
    (potentially distributed among multiple servers).

    mode: 
        'sync' = sequential section downloads
        'async' = asynchronous, using asyncio + aiohttp

    url:
        resource url on public server

    number_sources: 
        number of sections to download separately
    '''

    fname = url.split('/')[-1]

    head = requests.head(url)
    file_header = head.headers

    # parameters for sectioning the file for partial downloads
    n_sections = number_sections(file_header, number_sources)
    bytes_each = size_sections(file_header, n_sections)

    print(f'\
        Download: {n_sections} sections, {bytes_each} bytes each.')

    # Range request headers (files that don't accept
    # range requests have been assigned n_sections = 1)
    start_bytes = [(bytes_each * i) for i in range(n_sections)]
    range_strings = \
        [f"bytes={start_byte}-{start_byte + bytes_each - 1}" for \
            start_byte in start_bytes]
    header_pairs = (("Range", range) for range in range_strings)
    headers = [dict([pair]) for pair in header_pairs]

    # download file sections    
    file_sections, dl_time = get_sections(mode, url, headers)
        
    # assemble file parts into a single byte file
    byte_file, file_time = assemble_byte_file(file_sections)

    # if ETag, try to validate # TODO
    if 'ETag' in file_header:
        print('File has ETag')
        validate_etag(file_header, byte_file)

    # write byte file to disk at local_dir/fname
    file_name, write_time = save_file(mode, fname, byte_file)
    
    return file_name, dl_time, file_time, write_time

def number_sections(header, number_sources : int):
    ''' Verify that the file can be requested in ranges/sections '''

    if 'Accept-Ranges' not in header or \
        header['Accept-Ranges'] == 'none':
        print('File cannot be split. Single-source download starting.')
        return 1
    else:
        return number_sources

def size_sections(header, number_sections : int):
    ''' Establish the byte size per section '''

    if header['Content-Length']:
        return -(-int(header['Content-Length']) // number_sections)
    else:
        print('! File size unknown on initiating download')
        if 'Accept-Ranges' not in header or \
            header['Accept-Ranges'] == 'none':
            # TODO ? unknown content length and no partial downloads: 
            # try: A. set to inf (download will stop at eof (exceptions?))
            # OR B. stream/chunk
            pass
        else:
            return 10*(2**12) # 2**12 ~= 1 MB

def get_sections(mode : str, url : str, headers):
    ''' Download sections '''

    dl_t0 = time.time()
    if len(headers) == 1:
        p = []
        response = requests.get(url)
        p.append(response.content)
    else:
        if mode == 'sync':
            p = []    
            for header in headers:
                response = requests.get(url, headers=header)
                p.append(response.content)
        elif mode == 'async':
            p = []
            async def async_downloads():
                ''' Download sections asynchronously '''
                async with aiohttp.ClientSession() as session:
                    tasks = get_tasks(session, url, headers)
                    responses = await asyncio.gather(*tasks) 
                    for response in responses:
                        p.append(await response.read())
            asyncio.run(async_downloads())
    dl_time = (time.time() - dl_t0)
    return p, dl_time

def get_tasks(session, url, headers):
    ''' Create task lisk for async execution \
        with aiohttp.ClientSession '''

    tasks = []
    for header in headers:
        tasks.append(asyncio.create_task(session.get(url,\
            headers=header, ssl=False)))
    return tasks

def assemble_byte_file(file_sections : list):
    ''' Reassemble file sections into a (byte) file '''

    file_t0 = time.time()
    byte_file = b''
    for section in file_sections: byte_file += section
    file_time = (time.time() - file_t0)

    return byte_file, file_time

def validate_etag(header, byte_file : bytes):
    ''' Compare the file header ETag with known ETag algorithms \
        applied to the downloaded (byte) file to validate '''

    etag = header['ETag'][1:-1] if header['ETag'][0:1]!=['W/'] \
            else header['ETag'][3:-1]
    print(f'ETag from file header: {etag}')
    # TODO ? multipart download calc
    for alg in hashlib.algorithms_guaranteed:
        if alg.startswith('shake_'):
            continue
        checksum = getattr(hashlib, alg)(byte_file).hexdigest()
        #print(f'Checksum: {alg}: {checksum}')
        if checksum == etag:
            print('ETags match:')
            print(alg, checksum.digest(), etag)
            break
    print('ETag ?= checksum : no match found')
    return 

def save_file(mode : str, fname : str, byte_data : bytes):
    ''' Save file (reassembled from sections) to disk '''

    w_t0 = time.time()
    n = fname.split('.')
    file_name = n[0] + '_' + mode + '.' + n[-1]
    with open(file_name, 'wb') as handle:
        handle.write(byte_data)
    write_time = time.time() - w_t0

    return file_name, write_time




if __name__ == "__main__":

    number_sources = 7
    # to compare timing: modes = ['sync', 'async']
    modes = ['sync', 'async']
    url, num_repeats = get_input()
    
    for mode in modes:
        d_times, f_times, w_times = reset_times()
        # loop for performance testing (averages)
        # num_repeats = 1 by default
        for i in range(num_repeats):

            fname, download_time, file_time, write_time = \
                multisource_download(mode, url, number_sources)

            d_times.append(download_time)
            f_times.append(file_time)
            w_times.append(write_time)
        average_times(mode, num_repeats, d_times, f_times, w_times)
        print(f'\n Downloaded file saved to local directory as {fname}\n')