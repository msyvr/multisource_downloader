def reset_times():
    ''' Reset timing lists for download, file reassembly, disk
    write. For computing average times over multiple runs '''

    d_times = []
    f_times = []
    w_times = []

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