import aiohttp, asyncio, requests
import time, hashlib

from helpers import get_request_ranges

def async_get_sections(url, ranges, filename, fileheader):

    async def get_section(session, url, range, count):
        async with session.get(url, headers=range) as resp:
            section = await resp.read()
            print(f'-- downloaded section {count}: range = {range}')
            return section

    async def get_all_sections():
        async with aiohttp.ClientSession() as session:
            t0_d = time.perf_counter()

            tasks = []
            for count, range in enumerate(ranges):
                tasks.append(asyncio.ensure_future(get_section(session, url, range, count)))

            sections = await asyncio.gather(*tasks)
            print(f'Download time: {time.perf_counter() - t0_d} seconds')
            bytes_data = b''
            for section in sections:
                bytes_data += section
            with open(filename, 'wb') as handle:
                handle.write(bytes_data)
            print(f'Download + save time: {time.perf_counter() - t0_d} seconds')

            # check hashlib algs for etag match; no guarantees
            etag = fileheader['ETag'].strip('"') if fileheader['ETag'][0:2]!='W/' else fileheader['ETag'][2:].strip('"')
            for alg in hashlib.algorithms_guaranteed:
                if alg.startswith('shake_'):
                    etag_length = len(etag)
                    checksum = getattr(hashlib, alg)(bytes_data).hexdigest(etag_length//2)
                else:
                    checksum = getattr(hashlib, alg)(bytes_data).hexdigest()
                if checksum == etag:
                    print('ETags match')
                    break
            print('ETag ?= checksum : no match found')

    asyncio.run(get_all_sections())

if __name__ == "__main__":
    
    #### hardcoded inputs
    url = 'https://raw.githubusercontent.com/msyvr/testfiles/361d77a8bf67c065cac0804edf5f023b8b5ad25a/LeanneAndJohnny2017.mov'
    filename = url.split('/')[-1]
    number_sources = 8

    # individual download section parameters
    file_header = requests.head(url).headers
    request_ranges = get_request_ranges(file_header, number_sources)

    # async download
    async_get_sections(url, request_ranges, filename, file_header)
