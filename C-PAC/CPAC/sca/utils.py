# Import packages
import os
import sys
import re
import commands
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util


def compute_fisher_z_score(correlation_file, timeseries_one_d):

    """
    Computes the fisher z transform of the input correlation map
    If the correlation map contains data for multiple ROIs then 
    the function returns z score for each ROI as a seperate nifti 
    file


    Parameters
    ----------
    correlation_file: string
        Input correlations file

    Returns
    -------
    out_file : list (nifti files)
        list of z_scores for mask or ROI
    """

    import nibabel as nb
    import numpy as np
    import os

    roi_numbers = []
    if '#' in open(timeseries_one_d, 'r').readline().rstrip('\r\n'):
        roi_numbers = open(timeseries_one_d, 'r').readline().rstrip('\r\n').replace('#', '').split('\t')

    corr_img = nb.load(correlation_file)
    corr_data = corr_img.get_data()

    hdr = corr_img.get_header()

    corr_data = np.log((1 + corr_data) / (1 - corr_data)) / 2.0

    dims = corr_data.shape

    out_file = []

    if len(dims) == 5 or len(roi_numbers) > 0:

        if len(dims) == 5:
            x, y, z, one, roi_number = dims
            corr_data = np.reshape(corr_data, (x * y * z, roi_number), order='F')

        for i in range(0, len(roi_numbers)):

            sub_data = corr_data
            if len(dims) == 5:
                sub_data = np.reshape(corr_data[:, i], (x, y, z), order='F')

            sub_img = nb.Nifti1Image(sub_data, header=corr_img.get_header(), affine=corr_img.get_affine())
            sub_z_score_file = os.path.join(os.getcwd(), 'z_score_ROI_number_%s.nii.gz' % (roi_numbers[i]))
            sub_img.to_filename(sub_z_score_file)
            out_file.append(sub_z_score_file)

    else:
        z_score_img = nb.Nifti1Image(corr_data, header=hdr, affine=corr_img.get_affine())
        z_score_file = os.path.join(os.getcwd(), 'z_score.nii.gz')
        z_score_img.to_filename(z_score_file)
        out_file.append(z_score_file)

    return out_file


def check_ts(in_file):
    import numpy as np
    try:
        timepoints, rois = np.loadtxt(in_file).shape
    except ValueError:
        timepoints = np.loadtxt(in_file).shape[0]
        rois = 1	
    if rois > timepoints:
        message = ('\n\n\n****The number of timepoints (' + str(timepoints)
                   + ') is smaller than the number of ROIs to run ('
                   + str(rois) + ') - therefore the GLM is'
                   + ' underspecified and can\'t run.****\n\n\n')
        print(message)
        raise Exception(message)
    else:
        return in_file


def map_to_roi(timeseries, maps):
    """
    Renames the outputs of the temporal multiple regression workflow for sca 
    according to the header information of the timeseries.txt file that was 
    passed
    
    NOTE: This is only run if the temporal regression is run as part of sca
          (which = 'RT') when calling the temporal regression workflow.
          If you run the temporal regression workflow manually, don\'t set 
          (which = 'RT') unless you provide a timeseries.txt file with a header
          containing the names of the timeseries


    Parameters
    ----------

    timeseries: string
        Input timeseries.txt file
        
    maps: List (nifti files)
        List of output files generated by the temporal regression workflow if
        (which == 'RT')
    

    Returns
    -------

    labels : List (strings)
        List of names that the output files should be renamed to
        
    maps: List (nifti files)
        List of output files generated by the temporal regression workflow if
        (which == 'RT')
    """
    import numpy as np
    from nipype import logging
    logger = logging.getLogger('nipype.workflow')
    testMat = np.loadtxt(timeseries)
    timepoints, rois = testMat.shape

    if rois > timepoints:
        logger.warn('The number of timepoints is smaller than the number '
                        'of ROIs to run - therefore the GLM is '
                        'underspecified and can\'t run.')

    # pull in the ROI labels from the header of the extracted timeseries
    # CSV file
    with open(timeseries, "r") as f:
        roi_file_lines = f.read().splitlines()

    roi_err = "\n\n[!] The output of 3dROIstats, used in extracting " \
              "the timeseries, was not in the expected format.\n\nROI " \
              "output file: {0}\n\n".format(timeseries)

    for line in roi_file_lines:
        if "Mean_" in line:
            try:
                roi_list = line.split("\t")
                # clear out any blank strings/non ROI labels in the list
                roi_list = [x for x in roi_list if "Mean" in x]
                # rename labels
                roi_list = \
                    [x.replace("Mean",
                               "sca_tempreg_z_maps_roi").replace(" ", "")
                     for x in roi_list]
            except:
                raise Exception(roi_err)
            break
    else:
        raise Exception(roi_err)

    new_labels = []
    for roi_label in roi_list:
        new_labels.append(os.path.join(os.getcwd(), roi_label))

    numMaps = len(maps)
    maps.sort()

    # if not numMaps / 2 == rois:
    #     raise Exception('You specified {0} timeseries but only {1} spatial '
    #                     'maps were generated'.format(str(rois),
    #                                                  str(numMaps/2)))

    maps = maps[:rois]

    return roi_list, maps
