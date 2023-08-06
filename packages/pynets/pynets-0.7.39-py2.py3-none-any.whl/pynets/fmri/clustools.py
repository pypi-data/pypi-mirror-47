#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 18:07:34 2017

@author: PSYC-dap3463
Adapted from Cameron Craddock's PyClusterROI and soon to be replaced with a pypi dependency
"""
import nibabel as nib
import numpy as np

# Craddock, R. C.; James, G. A.; Holtzheimer, P. E.; Hu, X. P. & Mayberg, H. S.
# A whole brain fMRI atlas generated via spatially constrained spectral
# clustering Human Brain Mapping, 2012, 33, 1914-1928 doi: 10.1002/hbm.21333.
#
# ARTICLE{Craddock2012,
#   author = {Craddock, R C and James, G A and Holtzheimer, P E and Hu, X P and
#   Mayberg, H S},
#   title = {{A whole brain fMRI atlas generated via spatially constrained
#   spectral clustering}},
#   journal = {Human Brain Mapping},
#   year = {2012},
#   volume = {33},
#   pages = {1914--1928},
#   number = {8},
#   address = {Department of Neuroscience, Baylor College of Medicine, Houston,
#       TX, United States},
#   pmid = {21769991},
# }


# simple function to translate 1D vector coordinates to 3D matrix coordinates for a 3D matrix of size sz
def indx_1dto3d(idx, sz):
    """

    :param idx:
    :param sz:
    :return:
    """
    from scipy import divide, prod
    x = divide(idx, prod(sz[1:3]))
    y = divide(idx-x*prod(sz[1:3]), sz[2])
    z = idx-x*prod(sz[1:3])-y*sz[2]
    return x, y, z


# simple function to translate 3D matrix coordinates to 1D vector coordinates for a 3D matrix of size sz
def indx_3dto1d(idx, sz):
    """

    :param idx:
    :param sz:
    :return:
    """
    from scipy import prod, rank
    if rank(idx) == 1:
        idx1 = idx[0]*prod(sz[1:3])+idx[1]*sz[2]+idx[2]
    else:
        idx1 = idx[:, 0]*prod(sz[1:3])+idx[:, 1]*sz[2]+idx[:, 2]
    return idx1


def make_local_connectivity_scorr(func_file, clust_mask, outfile, thresh):
    """

    :param func_file:
    :param clust_mask:
    :param outfile:
    :param thresh:
    """
    from scipy.sparse import csc_matrix
    from scipy import prod, rank
    neighbors = np.array([[-1, -1, -1], [0, -1, -1], [1, -1, -1],
                           [-1, 0, -1], [0, 0, -1], [1, 0, -1],
                           [-1, 1, -1], [0, 1, -1], [1, 1, -1],
                           [-1, -1, 0], [0, -1, 0], [1, -1, 0],
                           [-1, 0, 0], [0, 0, 0], [1, 0, 0],
                           [-1, 1, 0], [0, 1, 0], [1, 1, 0],
                           [-1, -1, 1], [0, -1, 1], [1, -1, 1],
                           [-1, 0, 1], [0, 0, 1], [1, 0, 1],
                           [-1, 1, 1], [0, 1, 1], [1, 1, 1]])

    # read in the mask
    msk = nib.load(clust_mask)
    msz = msk.shape

    # convert the 3D mask array into a 1D vector
    mskdat = np.reshape(msk.get_data(), prod(msz))

    # determine the 1D coordinates of the non-zero
    # elements of the mask
    iv = np.nonzero(mskdat)[0]

    # read in the fmri data
    # NOTE the format of x,y,z axes and time dimension after reading
    # nb.load('x.nii.gz').shape -> (x,y,z,t)
    nim = nib.load(func_file)
    sz = nim.shape
    print(sz, ' dimensions of the 4D fMRI data')

    # reshape fmri data to a num_voxels x num_timepoints array
    imdat = np.reshape(nim.get_data(), (prod(sz[:3]), sz[3]))

    # mask the datset to only then in-mask voxels
    imdat = imdat[iv, :]
    imdat_sz = imdat.shape

    # zscore fmri time courses, this makes calculation of the
    # correlation coefficient a simple matrix product
    imdat_s = np.tile(np.std(imdat, 1), (imdat_sz[1], 1)).T
    # replace 0 with really large number to avoid div by zero
    imdat_s[imdat_s == 0] = 1000000
    imdat_m = np.tile(np.mean(imdat, 1), (imdat_sz[1], 1)).T
    imdat = (imdat - imdat_m) / imdat_s

    # set values with no variance to zero
    imdat[imdat_s == 0] = 0
    imdat[np.isnan(imdat)] = 0

    # remove voxels with zero variance, do this here
    # so that the mapping will be consistent across
    # subjects
    vndx = np.nonzero(np.var(imdat, 1) != 0)[0]
    iv = iv[vndx]

    m = len(iv)
    print(m, ' # of non-zero valued or non-zero variance voxels in the mask')

    # construct a sparse matrix from the mask
    msk = csc_matrix((vndx + 1, (iv, np.zeros(m))), shape=(prod(msz), 1))

    sparse_i = []
    sparse_j = []
    sparse_w = [[]]

    for i in range(0, m):
        if i % 1000 == 0:
            print('voxel #', i)
        # convert index into 3D and calculate neighbors
        ndx3d = indx_1dto3d(iv[i], sz[:-1]) + neighbors
        # convert resulting 3D indices into 1D
        ndx1d = indx_3dto1d(ndx3d, sz[:-1])
        # convert 1D indices into masked versions
        ondx1d = msk[ndx1d].todense()
        # exclude indices not in the mask
        ndx1d = ndx1d[np.nonzero(ondx1d)[0]]
        ndx1d = ndx1d.flatten()
        ondx1d = np.array(ondx1d[np.nonzero(ondx1d)[0]])
        ondx1d = ondx1d.flatten() - 1
        # keep track of the index corresponding to the "seed"
        nndx = np.nonzero(ndx1d == iv[i])[0]
        # extract the time courses corresponding to the "seed"
        # and 3D neighborhood voxels
        tc = imdat[ondx1d, :]
        # calculate functional connectivity maps for "seed"
        # and 3D neighborhood voxels
        fc = np.dot(tc, imdat.T) / (sz[3] - 1)
        # calculate the spatial correlation between FC maps
        R = np.corrcoef(fc)
        if rank(R) == 0:
            R = np.reshape(R, (1, 1))
        # set NaN values to 0
        R[np.isnan(R)] = 0
        # set values below thresh to 0
        R[R < thresh] = 0
        # keep track of the indices and the correlation weights
        # to construct sparse connectivity matrix
        sparse_i = np.append(sparse_i, ondx1d, 0)
        sparse_j = np.append(sparse_j, (ondx1d[nndx]) * np.ones(len(ondx1d)))
        sparse_w = np.append(sparse_w, R[nndx, :], 1)

    # insure that the weight vector is the correct shape
    sparse_w = np.reshape(sparse_w, prod(np.shape(sparse_w)))

    # concatenate the i, j, and w_ij vectors
    outlist = sparse_i
    outlist = np.append(outlist, sparse_j)
    outlist = np.append(outlist, sparse_w)

    # save the output file to a .NPY file
    np.save(outfile, outlist)

    print('finished ', func_file, ' len ', len(outlist))


def make_local_connectivity_tcorr(func_file, clust_mask, outfile, thresh):
    """

    :param func_file:
    :param clust_mask:
    :param outfile:
    :param thresh:
    """
    from scipy.sparse import csc_matrix
    from scipy import prod, rank
    from itertools import product

    # index array used to calculate 3D neigbors
    neighbors = np.array(sorted(sorted(sorted([list(x) for x in list(set(product({-1, 0, 1}, repeat=3)))],
                                              key=lambda k: (k[0])), key=lambda k: (k[1])), key=lambda k: (k[2])))

    # read in the mask
    msk = nib.load(clust_mask)
    msz = np.shape(msk.get_data())
    msk_data = msk.get_data()
    # convert the 3D mask array into a 1D vector
    mskdat = np.reshape(msk_data, prod(msz))

    # determine the 1D coordinates of the non-zero elements of the mask
    iv = np.nonzero(mskdat)[0]
    m = len(iv)
    print("%s%s%s" % ('\nTotal non-zero voxels in the mask: ', m, '\n'))
    # read in the fmri data
    # NOTE the format of x,y,z axes and time dimension after reading
    nim = nib.load(func_file)
    sz = nim.shape

    # reshape fmri data to a num_voxels x num_timepoints array
    data = nim.get_data()
    imdat = np.reshape(data, (prod(sz[:3]), sz[3]))

    # construct a sparse matrix from the mask
    msk = csc_matrix((list(range(1, m+1)), (iv, np.zeros(m))), shape=(prod(sz[:-1]), 1))
    sparse_i = []
    sparse_j = []
    sparse_w = []

    negcount = 0

    # loop over all of the voxels in the mask
    print('Voxels:')
    for i in range(0, m):
        if i % 1000 == 0:
            print(str(i))
        # calculate the voxels that are in the 3D neighborhood of the center voxel
        ndx3d = indx_1dto3d(iv[i], sz[:-1])+neighbors
        ndx1d = indx_3dto1d(ndx3d, sz[:-1])

        # restrict the neigborhood using the mask
        ondx1d = msk[ndx1d].todense()
        ndx1d = ndx1d[np.nonzero(ondx1d)[0]]
        ndx1d = ndx1d.flatten()
        ondx1d = np.array(ondx1d[np.nonzero(ondx1d)[0]])
        ondx1d = ondx1d.flatten()

        # determine the index of the seed voxel in the neighborhood
        nndx = np.nonzero(ndx1d == iv[i])[0]
        # exctract the timecourses for all of the voxels in the neighborhood
        tc = np.matrix(imdat[ndx1d.astype('int'), :])

        # make sure that the "seed" has variance, if not just skip it
        if np.var(tc[nndx, :]) == 0:
            continue

        # calculate the correlation between all of the voxel TCs
        R = np.corrcoef(tc)
        if rank(R) == 0:
            R = np.reshape(R, (1, 1))

        # extract just the correlations with the seed TC
        R = R[nndx, :].flatten()

        # set NaN values to 0
        R[np.isnan(R)] = 0
        negcount = negcount+sum(R < 0)

        # set values below thresh to 0
        R[R < thresh] = 0

        # determine the non-zero correlations (matrix weights) and add their indices and values to the list
        nzndx = np.nonzero(R)[0]
        if len(nzndx) > 0:
            sparse_i = np.append(sparse_i, ondx1d[nzndx]-1, 0)
            sparse_j = np.append(sparse_j, (ondx1d[nndx]-1)*np.ones(len(nzndx)))
            sparse_w = np.append(sparse_w, R[nzndx], 0)

    # concatenate the i, j and w_ij into a single vector
    outlist = sparse_i
    outlist = np.append(outlist, sparse_j)
    outlist = np.append(outlist, sparse_w)

    # save the output file to a .NPY file
    np.save(outfile, outlist)

    print("%s%s" % ('Finished ', outfile))


def ncut(W, nbEigenValues):
    """

    :param W:
    :param nbEigenValues:
    :return:
    """
    from scipy.sparse.linalg import eigsh
    from scipy.sparse import spdiags
    from numpy.linalg import norm
    # parameters
    offset = 0.5
    maxiterations = 100
    eigsErrorTolerence = 1e-6
    eps = 2.2204e-16

    m = np.shape(W)[1]

    # make sure that W is symmetric, this is a computationally expensive operation, only use for debugging
    # if (W-W.transpose()).sum() != 0:
    #    print "W should be symmetric!"
    #    exit(0)

    # Degrees and regularization
    # S Yu Understanding Popout through Repulsion CVPR 2001
    # Allows negative values as well as improves invertability of d for small numbers i bet that this is what improves the stability of the eigen
    d = abs(W).sum(0)
    dr = 0.5*(d-W.sum(0))
    d = d+offset*2
    dr = dr+offset

    # calculation of the normalized LaPlacian
    W = W+spdiags(dr, [0], m, m, "csc")
    Dinvsqrt = spdiags((1.0/np.sqrt(d+eps)), [0], m, m, "csc")
    P = Dinvsqrt*(W*Dinvsqrt)

    # perform the eigen decomposition
    eigen_val, eigen_vec = eigsh(P, nbEigenValues, maxiter=maxiterations, tol=eigsErrorTolerence, which='LA')

    # sort the eigen_vals so that the first is the largest
    i = np.argsort(-eigen_val)
    eigen_val = eigen_val[i]
    eigen_vec = eigen_vec[:, i]

    # normalize the returned eigenvectors
    eigen_vec = Dinvsqrt*np.matrix(eigen_vec)
    norm_ones = norm(np.ones((m, 1)))
    for i in range(0, np.shape(eigen_vec)[1]):
        eigen_vec[:, i] = (eigen_vec[:, i] / norm(eigen_vec[:, i]))*norm_ones
        if eigen_vec[0, i] != 0:
            eigen_vec[:, i] = -1 * eigen_vec[:, i] * np.sign(eigen_vec[0, i])

    return eigen_val, eigen_vec


def discretisation(eigen_vec):
    """

    :param eigen_vec:
    :return:
    """
    import scipy as sp
    from scipy.sparse import csc_matrix
    from scipy.linalg import LinAlgError, svd
    from scipy import divide
    eps = 2.2204e-16

    # normalize the eigenvectors
    [n, k] = np.shape(eigen_vec)
    vm = np.kron(np.ones((1, k)), np.sqrt(np.multiply(eigen_vec, eigen_vec).sum(1)))
    eigen_vec = divide(eigen_vec, vm)

    svd_restarts = 0
    exitLoop = 0

    # if there is an exception we try to randomize and rerun SVD again and do this 30 times
    while (svd_restarts < 30) and (exitLoop == 0):
        # initialize algorithm with a random ordering of eigenvectors
        c = np.zeros((n, 1))
        R = np.matrix(np.zeros((k, k)))
        R[:, 0] = eigen_vec[int(sp.rand(1)*(n-1)), :].transpose()

        for j in range(1, k):
            c = c+abs(eigen_vec*R[:, j-1])
            R[:, j] = eigen_vec[c.argmin(), :].transpose()

        lastObjectiveValue = 0
        nbIterationsDiscretisation = 0
        nbIterationsDiscretisationMax = 20

        # iteratively rotate the discretised eigenvectors until they are maximally similar to the input eignevectors, this converges when the differences between the current solution and the previous solution differs by less than eps or we have reached the maximum number of itarations
        while exitLoop == 0:
            nbIterationsDiscretisation = nbIterationsDiscretisation + 1

            # rotate the original eigen_vectors
            tDiscrete = eigen_vec*R

            # discretise the result by setting the max of each row=1 and other values to 0
            j = np.reshape(np.asarray(tDiscrete.argmax(1)), n)
            eigenvec_discrete = csc_matrix((np.ones(len(j)), (list(range(0, n)), np.array(j))), shape=(n, k))

            # calculate a rotation to bring the discrete eigenvectors cluster to the original eigenvectors
            tSVD = eigenvec_discrete.transpose()*eigen_vec
            # catch a SVD convergence error and restart
            try:
                [U, S, Vh] = svd(tSVD)
            except LinAlgError:
                # catch exception and go back to the beginning of the loop
                print("SVD did not converge. Randomizing and trying again...")
                break

            # test for convergence
            NcutValue = 2*(n-S.sum())
            if (abs(NcutValue-lastObjectiveValue) < eps) or (nbIterationsDiscretisation > nbIterationsDiscretisationMax):
                exitLoop = 1
            else:
                # otherwise calculate rotation and continue
                lastObjectiveValue = NcutValue
                R = np.matrix(Vh).transpose()*np.matrix(U).transpose()

    if exitLoop == 0:
        raise ValueError("SVD did not converge after 30 retries")
    else:
        return eigenvec_discrete


def binfile_parcellate(infile, outfile, k):
    """

    :param infile:
    :param outfile:
    :param k:
    """
    from scipy.sparse import csc_matrix
    # check how long it takes

    # Read in the file
    if infile.endswith(".npy"):
        print("Reading", infile, "as a npy filetype")
        a = np.load(infile)
    else:
        print("Reading", infile, "as a binary file of doubles")
        fileobj = open(infile, 'rb')
        a = np.fromfile(fileobj)
        fileobj.close()

    # Calculate the number of non-zero weights in the connectivity matrix
    n = len(a)/3

    # Reshape the 1D vector read in from infile in to a 3xN array
    a = np.reshape(a, (3, int(n)))
    m = max(max(a[0, :]), max(a[1, :]))+1

    #Make the sparse matrix, CSC format is supposedly efficient for matrix arithmetic
    W = csc_matrix((a[2, :], (a[0, :], a[1, :])), shape=(int(m), int(m)))

    #We only have to calculate the eigendecomposition of the LaPlacian once, for the largest number of clusters provided. This provides a significant speedup, without any difference to the results.
    [_, eigenvec] = ncut(W, k)

    # Calculate each desired clustering result
    eigk = eigenvec[:, :k]
    eigenvec_discrete = discretisation(eigk)

    # Transform the discretised eigenvectors into a single vector where the value corresponds to the cluster # of the corresponding ROI
    group_img = eigenvec_discrete[:, 0]

    for i in range(1, k):
        group_img = group_img+(i+1)*eigenvec_discrete[:, i]

    # Apply the suffix to the output filename and write out results as a .npy file
    outname = "%s%s%s%s" % (outfile, '_', str(k), '.npy')
    np.save(outname, group_img.todense())


def make_image_from_bin_renum(image, binfile, mask):
    """

    :param image:
    :param binfile:
    :param mask:
    """
    # read in the mask
    nim = nib.load(mask)

    # read in the binary data
    if binfile.endswith(".npy"):
        print("Reading", binfile, "as a npy filetype")
        a = np.load(binfile)
    else:
        print("Reading", binfile, "as a binary file of doubles")
        a = np.fromfile(binfile)

    unique_a = list(set(a.flatten()))
    unique_a.sort()

    # renumber clusters to make the contiguous
    b = np.zeros((len(a), 1))
    for i in range(0, len(unique_a)):
        b[a == unique_a[i]] = i+1

    imdat = nim.get_data()
    # map the binary data to mask
    imdat[imdat > 0] = 1
    imdat[imdat > 0] = np.short(b[0:int(np.sum(imdat))].flatten())

    # write out the image as nifti
    nim_out = nib.Nifti1Image(imdat, nim.get_affine(), nim.get_header())
    #nim_out.set_data_dtype('int16')
    nim_out.to_filename(image)


def nil_parcellate(func_file, clust_mask, k, clust_type, ID, dir_path, uatlas_select):
    """

    :param func_file:
    :param clust_mask:
    :param k:
    :param clust_type:
    :param ID:
    :param dir_path:
    :param uatlas_select:
    :return:
    """
    import time
    import nibabel as nib
    from nilearn.regions import Parcellations
    from nilearn.regions import connected_label_regions
    detrending = True

    start = time.time()
    func_img = nib.load(func_file)
    mask_img = nib.load(clust_mask)
    clust_est = Parcellations(method=clust_type, detrend=detrending, n_parcels=int(k),
                              mask=mask_img)
    clust_est.fit(func_img)
    region_labels = connected_label_regions(clust_est.labels_img_)
    nib.save(region_labels, uatlas_select)
    print("%s%s%s" % (clust_type, k, " clusters: %.2fs" % (time.time() - start)))
    return


def individual_tcorr_clustering(func_file, clust_mask, ID, k, clust_type, thresh=0.5):
    """

    :param func_file:
    :param clust_mask:
    :param ID:
    :param k:
    :param clust_type:
    :param thresh:
    :return:
    """
    import os
    from pynets import utils
    from pynets.fmri import clustools

    nilearn_clust_list = ['kmeans', 'ward', 'complete', 'average']

    mask_name = os.path.basename(clust_mask).split('.nii.gz')[0]
    atlas_select = "%s%s%s%s%s" % (mask_name, '_', clust_type, '_k', str(k))
    print("%s%s%s%s%s%s%s" % ('\nCreating atlas using ', clust_type, ' at cluster level ', str(k),
                              ' for ', str(atlas_select), '...\n'))
    dir_path = utils.do_dir_path(atlas_select, func_file)
    uatlas_select = "%s%s%s%s%s%s%s%s" % (dir_path, '/', mask_name, '_', clust_type, '_k', str(k), '.nii.gz')

    if clust_type in nilearn_clust_list:
        clustools.nil_parcellate(func_file, clust_mask, k, clust_type, ID, dir_path, uatlas_select)
    elif clust_type == 'ncut':
        working_dir = "%s%s%s" % (os.path.dirname(func_file), '/', atlas_select)
        outfile = "%s%s%s%s" % (working_dir, '/rm_tcorr_conn_', str(ID), '.npy')
        outfile_parc = "%s%s%s" % (working_dir, '/rm_tcorr_indiv_cluster_', str(ID))
        binfile = "%s%s%s%s%s%s" % (working_dir, '/rm_tcorr_indiv_cluster_', str(ID), '_', str(k), '.npy')
        clustools.make_local_connectivity_tcorr(func_file, clust_mask, outfile, thresh)
        clustools.binfile_parcellate(outfile, outfile_parc, int(k))
        clustools.make_image_from_bin_renum(uatlas_select, binfile, clust_mask)

    clustering = True
    return uatlas_select, atlas_select, clustering, clust_mask, k, clust_type
