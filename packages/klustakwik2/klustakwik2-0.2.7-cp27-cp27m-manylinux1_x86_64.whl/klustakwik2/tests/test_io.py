from numpy import *
from klustakwik2 import *
from numpy.testing import assert_raises, assert_array_almost_equal, assert_array_equal
from nose import with_setup
from nose.tools import nottest

from tempfile import mkdtemp
import os
from six.moves import range

@nottest
def generate_simple_test_raw_data():
    # Data as files
    dirname = mkdtemp()
    open(os.path.join(dirname, 'kktest.fet.1'), 'wt').write('''
5
1 3 5 7 11
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
'''.strip())
    open(os.path.join(dirname, 'kktest.fmask.1'), 'wt').write('''
5
1 0.5 0 0 0
0 1 1 0 0
0 1 1 0 0
0 0 0 1 1
'''.strip())

    # Data as arrays
    fet = array([[1,3,5,7,11],
                 [6,7,8,9,10],
                 [11,12,13,14,15],
                 [16,17,18,19,20]], dtype=float)
    fmask = array([[1,0.5,0,0,0],
                   [0,1,1,0,0],
                   [0,1,1,0,0],
                   [0,0,0,1,1]], dtype=float)

    # Normalisation to [0, 1]
    fet = (fet-amin(fet, axis=0))/(amax(fet, axis=0)-amin(fet, axis=0))

    nanmasked_fet = fet.copy()
    nanmasked_fet[fmask>0] = nan

    # Correct computation of the corrected data and correction term
    x = fet
    w = fmask
    nu = nanmean(nanmasked_fet, axis=0)[newaxis, :]
    sigma2 = nanvar(nanmasked_fet, axis=0)[newaxis, :]
    y = w*x+(1-w)*nu
    z = w*x*x+(1-w)*(nu*nu+sigma2)
    correction_terms = z-y*y
    features = y

    return (load_fet_fmask_to_raw(os.path.join(dirname, 'kktest'), 1),
            fet, fmask, features, correction_terms)


@nottest
def generate_simple_test_data():
    data, fet, fmask, features, correction_terms = generate_simple_test_raw_data()
    return data.to_sparse_data()


def test_load_fet_fmask():

    ### PART 1: Check that loading to RawSparseData is correct
    data, fet, fmask, features, correction_terms = generate_simple_test_raw_data()

    nanmasked_fet = fet.copy()
    nanmasked_fet[fmask>0] = nan
    assert_array_almost_equal(data.noise_mean, nanmean(nanmasked_fet, axis=0))
    assert_array_almost_equal(data.noise_variance, nanvar(nanmasked_fet, axis=0))
    assert amin(data.features)==0
    assert amax(data.features)==1
    assert len(data.offsets)==5
    loaded_fet = zeros_like(fet)
    for i in range(4):
        data_u = data.unmasked[data.offsets[i]:data.offsets[i+1]]
        true_u, = fmask[i, :].nonzero()
        assert_array_equal(data_u, true_u)
        data_f = data.features[data.offsets[i]:data.offsets[i+1]]
        true_f = fet[i, data_u]
        assert_array_equal(data_f, true_f)
        data_m = data.masks[data.offsets[i]:data.offsets[i+1]]
        true_m = fmask[i, data_u]
        assert_array_equal(data_m, true_m)

    ### PART 2: Check that converting to SparseData is correct
    data = data.to_sparse_data() # compute unique masks and apply correction terms to data

    assert data.num_spikes==4
    assert data.num_features==5
    assert data.num_masks==3

    for i in range(4):
        data_u = data.unmasked[data.unmasked_start[i]:data.unmasked_end[i]]
        true_u, = fmask[i, :].nonzero()
        assert_array_equal(data_u, true_u)
        data_f = data.features[data.values_start[i]:data.values_end[i]]
        true_f = features[i, data_u]
        assert_array_almost_equal(data_f, true_f)
        data_c = data.correction_terms[data.values_start[i]:data.values_end[i]]
        true_c = correction_terms[i, data_u]
        assert_array_almost_equal(data_c, true_c)
        data_m = data.masks[data.values_start[i]:data.values_end[i]]
        true_m = fmask[i, data_u]
        assert_array_almost_equal(data_m, true_m)


def test_subset_features():
    raw_data, fet, fmask, features, correction_terms = generate_simple_test_raw_data()
    data = raw_data.to_sparse_data()
    for I, sp in [([0], [0]),
                  ([3, 4], [3]),
                  ([1, 2], [0, 1, 2]),
                  ([1, 3, 4], [0, 1, 2, 3]),
                  ]:
        I = array(I, dtype=int)
        subdata, spikes = data.subset_features(I)
        assert_array_equal(spikes, sp)
        U = lambda p: subdata.unmasked[subdata.unmasked_start[p]:subdata.unmasked_end[p]]
        F = lambda p: subdata.features[subdata.values_start[p]:subdata.values_end[p]]
        M = lambda p: subdata.masks[subdata.values_start[p]:subdata.values_end[p]]
        CT = lambda p: subdata.correction_terms[subdata.values_start[p]:subdata.values_end[p]]
        for p in range(len(spikes)):
            assert_array_equal(U(p), (fmask[spikes[p], I]>0).nonzero()[0])
            assert_array_equal(F(p), features[spikes[p], I][fmask[spikes[p], I]>0])
            assert_array_equal(M(p), fmask[spikes[p], I][fmask[spikes[p], I]>0])
            assert_array_equal(CT(p), correction_terms[spikes[p], I][fmask[spikes[p], I]>0])

if __name__=='__main__':
    test_load_fet_fmask()
    test_subset_features()

