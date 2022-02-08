from get_input import get_input

def reset_times():
    ''' Reset timing lists for download, file reassembly, disk
    write. For computing average times over multiple runs '''

    d_times = []
    f_times = []
    w_times = []

    return d_times, f_times, w_times

def append_times(d_times, f_times, w_times, download_time, file_time, write_time):
    ''' Track timings from individual runs for eventual averaging '''
    
    d_times.append(download_time)
    f_times.append(file_time)
    w_times.append(write_time)

    return d_times, f_times, w_times

def average_times(mode, num_repeats, d_times, f_times, w_times):
    ''' Averaged performance times for a download mode '''

    avg_dlt = sum(d_times)/len(d_times)
    avg_fat = sum(f_times)/len(f_times)
    avg_wrt = sum(w_times)/len(w_times)
    
    print(f'\nIn {mode} mode, averaging over {num_repeats} downloads:')
    print(f'Average download time: {avg_dlt} seconds')
    print(f'Average assemble time: {avg_fat} seconds')
    print(f'Average write time: {avg_wrt} seconds\n')
    return None