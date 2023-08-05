from tridesclous import get_dataset
from tridesclous.signalpreprocessor import signalpreprocessor_engines, offline_signal_preprocessor

from tridesclous.signalpreprocessor import HAVE_PYOPENCL

import time

import scipy.signal
import numpy as np

from matplotlib import pyplot




def run_online(engine, sigs, sample_rate, chunksize, **params):
    nb_channel = sigs.shape[1]
    
    # precompute medians and mads
    params2 = dict(params)
    params2['normalize'] = False
    sigs_for_noise = offline_signal_preprocessor(sigs, sample_rate, **params2)
    medians = np.median(sigs_for_noise, axis=0)
    mads = np.median(np.abs(sigs_for_noise-medians),axis=0)*1.4826
    params['signals_medians'] = medians
    params['signals_mads'] = mads

    SignalPreprocessorClass = signalpreprocessor_engines[engine]
    signalpreprocessor = SignalPreprocessorClass(sample_rate, nb_channel, chunksize, sigs.dtype)
    signalpreprocessor.change_params(**params)
    
    nloop = sigs.shape[0]//chunksize
    
    all_online_sigs = []
    t1 = time.perf_counter()
    for i in range(nloop):
        #~ print(i)
        pos = (i+1)*chunksize
        chunk = sigs[pos-chunksize:pos,:]
        pos2, preprocessed_chunk = signalpreprocessor.process_data(pos, chunk)
        if preprocessed_chunk is not None:
            #~ print(preprocessed_chunk)
            all_online_sigs.append(preprocessed_chunk)
    t2 = time.perf_counter()
    print(engine, 'process time', t2-t1)
    online_sig = np.concatenate(all_online_sigs)
    
    
    return online_sig
    
    
    




def test_compare_offline_online_engines():
    #~ HAVE_PYOPENCL = True
    if HAVE_PYOPENCL:
        engines = ['numpy', 'opencl']
        #~ engines = [ 'opencl']
        #~ engines = ['numpy']
    else:
        engines = ['numpy']


    # get sigs
    sigs, sample_rate = get_dataset(name='olfactory_bulb')
    print(sample_rate)
    #~ sigs = np.tile(sigs, (1, 20)) #for testing large channels num
    
    nb_channel = sigs.shape[1]
    print('nb_channel', nb_channel)
    
    #params
    chunksize = 1024
    nloop = sigs.shape[0]//chunksize
    sigs = sigs[:chunksize*nloop]
    
    print('sig duration', sigs.shape[0]/sample_rate)
    
    highpass_freq = 500.
    #~ highpass_freq = 300.
    #~ highpass_freq = 100.
    #~ highpass_freq = None
    lowpass_freq = 4000.
    #~ lowpass_freq = None
    #~ smooth_kernel = True
    smooth_size = 0
    
    
    #~ lostfront_chunksize = int(sample_rate/highpass_freq)*4
    #~ print('lostfront_chunksize', lostfront_chunksize)
    #~ exit()
    
    params = {
                'common_ref_removal' : False,
                'highpass_freq': highpass_freq,
                'lowpass_freq': lowpass_freq,
                'smooth_size':smooth_size,
                'output_dtype': 'float32',
                'normalize' : True,
                'lostfront_chunksize': 150
                }
    
    t1 = time.perf_counter()
    offline_sig = offline_signal_preprocessor(sigs, sample_rate, **params)
    
    t2 = time.perf_counter()
    print('offline', 'process time', t2-t1)
    
    online_sigs = {}
    for engine in engines:
        if engine == 'opencl':
            params['cl_platform_index'] = 0
            params['cl_device_index'] = 0
        online_sigs[engine] = run_online(engine, sigs, sample_rate, chunksize, **params)
    
    # remove border for comparison
    min_size = min([online_sigs[engine].shape[0] for engine in engines]) 
    offline_sig = offline_sig[chunksize:min_size]
    for engine in engines:
        online_sig = online_sigs[engine]
        online_sigs[engine] = online_sig[chunksize:min_size]

    # compare
    for engine in engines:
        print(engine)
        online_sig = online_sigs[engine]
        residual = np.abs(online_sig.astype('float64')-offline_sig.astype('float64'))
        
        print('max residual', np.max(residual))
        print('/', np.mean(np.abs(offline_sig.astype('float64'))))
        residual_normed = residual/np.mean(np.abs(offline_sig.astype('float64')))
        print('max residual_normed', np.max(residual_normed))

        # plot
        # fig, axs = pyplot.subplots(nrows=nb_channel, sharex=True)
        #~ fig, axs = pyplot.subplots(nrows=4, sharex=True)
        # for i in range(nb_channel):
        #~ for i in range(4):
            #~ ax = axs[i]
            #~ ax.plot(residual_normed[:, i], color = 'k')
            #~ ax.plot(residual[:, i], color = 'k')
            #~ ax.plot(offline_sig[:, i], color = 'g')
            #~ ax.plot(online_sig[:, i], color = 'r', ls='--')
            #~ for i in range(nloop):
                #~ ax.axvline(i*chunksize, color='k', alpha=0.4)
        #~ pyplot.show()

        print(np.max(residual_normed))
        #~ print(np.mean(np.abs(offline_sig.astype('float64'))))
        assert np.max(residual_normed)<0.05, 'online differt from offline more than 5%'


def explore_lostfront_chunksize():

    sigs, sample_rate = get_dataset(name='olfactory_bulb')
    chunksize = 1024
    nloop = sigs.shape[0]//chunksize
    sigs = sigs[:chunksize*nloop]
    
    params = {
                'common_ref_removal' : False,
                'highpass_freq': 300.,
                'lowpass_freq': 4000.,
                'smooth_size':0,
                'output_dtype': 'float32',
                'normalize' : True,
                #~ 'lostfront_chunksize': 150
                }
    
    offline_sig = offline_signal_preprocessor(sigs, sample_rate, **params)
    
    lostfront_chunksizes = [ int(sample_rate/params['highpass_freq'])*i for i in range(1, 5)]
    
    online_sigs = {}
    for lostfront_chunksize in lostfront_chunksizes:
        print('lostfront_chunksize', lostfront_chunksize)
        params['lostfront_chunksize'] = lostfront_chunksize
        online_sigs[lostfront_chunksize] = run_online('numpy', sigs, sample_rate, chunksize, **params)


    # remove border for comparison
    min_size = min([online_sigs[lostfront_chunksize].shape[0] for lostfront_chunksize in lostfront_chunksizes]) 
    offline_sig = offline_sig[chunksize:min_size]
    for lostfront_chunksize in lostfront_chunksizes:
        online_sig = online_sigs[lostfront_chunksize]
        online_sigs[lostfront_chunksize] = online_sig[chunksize:min_size]


    for lostfront_chunksize in lostfront_chunksizes:
        print('lostfront_chunksize', lostfront_chunksize)
        
        online_sig = online_sigs[lostfront_chunksize]
        residual = np.abs(online_sig.astype('float64')-offline_sig.astype('float64'))
        
        residual_normed = residual/np.mean(np.abs(offline_sig.astype('float64')))
        print('   max residual_normed', np.max(residual_normed))



        
    

def test_auto_lostfront_chunksize():
    sigs, sample_rate = get_dataset(name='olfactory_bulb')

    sigs, sample_rate = get_dataset(name='olfactory_bulb')
    chunksize = 1024
    nloop = sigs.shape[0]//chunksize
    sigs = sigs[:chunksize*nloop]
    
    params = {
                'common_ref_removal' : False,
                'highpass_freq': 300.,
                'lowpass_freq': 4000.,
                'smooth_size':0,
                'output_dtype': 'float32',
                'normalize' : True,
                'lostfront_chunksize': None,
                }
    
    offline_sig = offline_signal_preprocessor(sigs, sample_rate, **params)
    
    online_sig = run_online('numpy', sigs, sample_rate, chunksize, **params)
    min_size = online_sig.shape[0]
    offline_sig = offline_sig[chunksize:min_size]
    online_sig = online_sig[chunksize:min_size]
    
    residual = np.abs(online_sig.astype('float64')-offline_sig.astype('float64'))
    
    residual_normed = residual/np.mean(np.abs(offline_sig.astype('float64')))
    print('   max residual_normed', np.max(residual_normed))
    
    
    
    # remove border for comparison


def test_smooth_with_filtfilt():
    sigs = np.zeros((100, 1), 'float32')
    #~ sigs[49] = 6
    sigs[50] = 1
    #~ sigs[51] = 5
    #~ sigs += np.random.randn(*sigs.shape)
    
    # smooth with box kernel
    box_size = 3
    kernel = np.ones(box_size)/box_size
    kernel = kernel[:, None]
    sigs_smooth =  scipy.signal.fftconvolve(sigs,kernel,'same')

    # smooth with filter
    #~ coeff = np.array([1/3, 1/3, 1/3, 1,0,0], dtype='float32')
    #~ coeff = np.array([0.5, 0.25, 0.25, 1,0,0], dtype='float32')
    #~ coeff = np.array([0.8, 0.1, 0.1, 1,0,0], dtype='float32')
    b0 = (1./3.)**.5
    b1 = (1-b0)
    b2 =0.
    #~ b2 = (1-b0)/2.
    #~ b0 = .4
    #~ b1 = 0.6
    #~ b2 = 0.
    coeff = np.array([[b0, b1, b2, 1,0,0]], dtype='float32')
    print(coeff)
    coeff = np.tile(coeff, (5, 1))
    sigs_smooth2 = scipy.signal.sosfiltfilt(coeff, sigs, axis=0)
    
    # smooth with LP filter
    coeff = scipy.signal.iirfilter(5, 0.3, analog=False,
                                    btype = 'lowpass', ftype = 'butter', output = 'sos')
    sigs_smooth3 = scipy.signal.sosfiltfilt(coeff, sigs, axis=0)
    
    
    if __name__ == '__main__':
        print(sigs_smooth2.sum())
        print(sigs_smooth2[40:60])
        fig, ax = pyplot.subplots()
        ax.plot(sigs, color='b', label='sig')
        ax.plot(sigs_smooth, color='g', label='box smooth')
        ax.plot(sigs_smooth2, color='r', label='filfilt smooth')
        ax.plot(sigs_smooth3, color='m', label='lp filter')
        
        ax.legend()
        
        pyplot.show()

    
    


    
if __name__ == '__main__':
    test_compare_offline_online_engines()
    #~ test_smooth_with_filtfilt()
    
    #~ explore_lostfront_chunksize()
    
    #~ test_auto_lostfront_chunksize()

