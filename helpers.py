def get_request_ranges(header, number_sources):
    '''Ranges formatted for range request headers.
    Files that don't accept range requests are downloaded in one shot.'''

    n_sections, bytes_each = size_sections(header, number_sources)
    print(f'\
        Download: {n_sections} sections, {bytes_each} bytes each.')   
    start_bytes = [(bytes_each * i) for i in range(n_sections)]
    range_strings = [f"bytes={start_byte}-{start_byte + bytes_each - 1}" 
        for start_byte in start_bytes]
    header_pairs = (("Range", range) for range in range_strings)    
    return [dict([pair]) for pair in header_pairs]

def size_sections(header: str, number_sources: int):
    ''' Establish the byte size per section '''   
    n_sections = number_sections_permitted(header, number_sources)   
    if header['Content-Length']:
        # ceiling division (round up)
        return n_sections, -(-int(header['Content-Length']) // n_sections)
    else:
        print('! File size unknown on initiating download')
        if 'Accept-Ranges' not in header or \
            header['Accept-Ranges'] == 'none':
            # TODO ? unknown content length + no partial downloads: 
            # try: A. set to inf (download will stop at eof (exceptions?))
            # OR B. stream/chunk
            pass
        return n_sections, 10*(2**12) # 2**12 ~= 1 MB

def number_sections_permitted(header, number_sources: int):
    ''' Verify that the file can be requested in ranges/sections '''   
    if 'Accept-Ranges' not in header or \
        header['Accept-Ranges'] == 'none':
        print('File cannot be split. Single-source download starting.')
        return 1
    else:
        return number_sources



