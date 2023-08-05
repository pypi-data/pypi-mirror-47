"""Definition of the CatTransform."""
import transform as n
from wtrwrks.waterworks.empty import empty
import wtrwrks.tanks.tank_defs as td
import wtrwrks.read_write.tf_features as feat
import numpy as np
import warnings
import tensorflow as tf


class CatTransform(n.Transform):
  """Class used to create mappings from raw categorical to vectorized, normalized data and vice versa.

  Parameters
  ----------
  name : str
    The name of the transform.
  from_file : str
    The path to the saved file to recreate the transform object that was saved to disk.
  save_dict : dict
    The dictionary to recreate the transform object
  index_to_cat_val : list
    The mapping from index number to category value.
  cat_val_to_index : dict
    The mapping from category value to index number.


  Attributes
  ----------
  input_dtype: numpy dtype
    The datatype of the original inputted array.
  input_shape: list of ints
    The shape of the original inputted array.

  """

  attribute_dict = {'norm_mode': None, 'norm_axis': 0, 'ignore_null': False, 'name': '', 'valid_cats': None, 'mean': None, 'std': None, 'dtype': np.float64, 'input_dtype': None, 'index_to_cat_val': None, 'cat_val_to_index': None}

  def __len__(self):
    """Get the length of the vector outputted by the row_to_vector method."""
    assert self.input_dtype is not None, ("Run calc_global_values before attempting to get the length.")
    return len(self.index_to_cat_val)

  def _extract_pour_outputs(self, tap_dict, prefix='', **kwargs):
    """Pull out all the values from tap_dict that cannot be explicitly reconstructed from the transform itself. These are the values that will need to be fed back to the transform into run the tranform in the pump direction.

    Parameters
    ----------
    tap_dict : dict
      The dictionary outputted by the pour (forward) transform.
    prefix : str
      Any additional prefix string/dictionary keys start with. Defaults to no additional prefix.

    Returns
    -------
    dict
      Dictionay of only those tap dict values which are can't be inferred from the Transform itself.

    """
    r_dict = {self._pre(k, prefix): tap_dict[self._pre(k, prefix)] for k in ['one_hots', 'missing_vals', 'indices']}
    return r_dict

  def _extract_pump_outputs(self, funnel_dict, prefix=''):
    """Pull out the original array from the funnel_dict which was produced by running pump.

    Parameters
    ----------
    funnel_dict : dict
      The dictionary outputted by running the transform's pump method. The keys are the names of the funnels and the values are the values of the tubes.
    prefix : str
      Any additional prefix string/dictionary keys start with. Defaults to no additional prefix.

    Returns
    -------
    np.ndarray
      The array reconstructed from the pump method.

    """
    array_key = self._pre('CatToIndex_0/slots/cats', prefix)
    return funnel_dict[array_key]

  def _alter_pour_outputs(self, pour_outputs, prefix=''):
    """Create a list of dictionaries for each example from the outputs of the pour method.

    Parameters
    ----------
    pour_outputs : dict
      The outputs of the _extract_pour_outputs method.
    prefix : str
      Any additional prefix string/dictionary keys start with. Defaults to no additional prefix.

    Returns
    -------
    list of dicts of features
      The example dictionaries which contain tf.train.Features.

    """
    pour_outputs = self._nopre(pour_outputs, prefix)
    # Find the locations of all the missing values. i.e. those that have been
    # replace by the unknown token.
    mask = pour_outputs['indices'] == -1

    # Convert the 1D missing vals array into a full array of the same size as
    # the indices array. This is so it can be easily separated into individual
    # rows that be put into separate examples.
    missing_vals = pour_outputs['missing_vals']
    full_missing_vals = self._full_missing_vals(mask, missing_vals)
    pour_outputs['missing_vals'] = full_missing_vals

    # att_dict = self._nopre(self._get_array_attributes(prefix), prefix)
    #
    # # Create an example dict for each row of indices.
    # num_examples = pour_outputs['indices'].shape[0]
    # example_dicts = []
    # for row_num in xrange(num_examples):
    #   example_dict = {}
    #   for key in pour_outputs:
    #     flat = pour_outputs[key][row_num].flatten()
    #     example_dict[key] = att_dict[key]['feature_func'](flat)
    #
    #   example_dict = self._pre(example_dict, prefix)
    #   example_dicts.append(example_dict)
    pour_outputs = self._pre(pour_outputs, prefix)
    return pour_outputs

  def _get_funnel_dict(self, array=None, prefix=''):
    """Construct a dictionary where the keys are the names of the slots, and the values are either values from the Transform itself, or are taken from the supplied array.

    Parameters
    ----------
    array : np.ndarray
      The inputted array of raw information that is to be fed through the pour method.
    prefix : str
      Any additional prefix string/dictionary keys start with. Defaults to no additional prefix.

    Returns
    -------
    dict
      The dictionary with all funnels filled with values necessary in order to run the pour method.

    """
    funnel_name = self._pre('CatToIndex_0/slots/cats', prefix)
    funnel_dict = {funnel_name: array}

    return funnel_dict

  def _get_tap_dict(self, pour_outputs, prefix=''):
    """Construct a dictionary where the keys are the names of the tubes, and the values are either values from the Transform itself, or are taken from the supplied pour_outputs dictionary.

    Parameters
    ----------
    pour_outputs : dict
      The dictionary of all the values outputted by the pour method.
    prefix : str
      Any additional prefix string/dictionary keys start with. Defaults to no additional prefix.

    Returns
    -------
    The dictionary with all taps filled with values necessary in order to run the pump method.

    """
    pour_outputs = self._nopre(pour_outputs, prefix)
    mvs = -1.0 * np.ones([len(pour_outputs['missing_vals'])])
    dtype = pour_outputs['one_hots'].dtype
    if self.norm_mode == 'mean_std':
      tap_dict = {
        'OneHot_0/tubes/missing_vals': mvs,
        'one_hots': pour_outputs['one_hots'],
        'indices': pour_outputs['indices'],
        'Div_0/tubes/smaller_size_array': self.std,
        'Div_0/tubes/a_is_smaller': False,
        'Div_0/tubes/missing_vals': np.array([], dtype=float),
        'Div_0/tubes/remainder': np.array([], dtype=dtype),
        'Sub_0/tubes/smaller_size_array': self.mean,
        'Sub_0/tubes/a_is_smaller': False,
        'missing_vals': pour_outputs['missing_vals'],
        'CatToIndex_0/tubes/cat_to_index_map': self.cat_val_to_index,
        'CatToIndex_0/tubes/input_dtype': self.input_dtype
      }
    else:
      tap_dict = {
        'OneHot_0/tubes/missing_vals': mvs,
        'one_hots': pour_outputs['one_hots'],
        'indices': pour_outputs['indices'],
        'missing_vals': pour_outputs['missing_vals'],
        'CatToIndex_0/tubes/cat_to_index_map': self.cat_val_to_index,
        'CatToIndex_0/tubes/input_dtype': self.input_dtype
      }
    return self._pre(tap_dict, prefix)

  def _parse_examples(self, arrays_dict, prefix=''):
    """Convert the list of example_dicts into the original outputs that came from the pour method.

    Parameters
    ----------
    example_dicts: list of dicts of arrays
      The example dictionaries which the arrays associated with a single example.
    prefix : str
      Any additional prefix string/dictionary keys start with. Defaults to no additional prefix.

    Returns
    -------
    dict
      The dictionary of all the values outputted by the pour method.

    """
    pour_outputs = {}
    pour_outputs = self._nopre(arrays_dict, prefix)
    
    missing_vals = pour_outputs['missing_vals'][pour_outputs['indices'] == -1]
    pour_outputs['missing_vals'] = missing_vals.tolist()

    pour_outputs = self._pre(pour_outputs, prefix)
    return pour_outputs

  def _setattributes(self, **kwargs):
    """Set the actual attributes of the Transform and do some value checks to make sure they valid inputs.

    Parameters
    ----------
    **kwargs :
      The keyword arguments that set the values of the attributes defined in the attribute_dict.

    """
    super(CatTransform, self)._setattributes(**kwargs)

    if self.norm_mode not in (None, 'mean_std'):
      raise ValueError(self.norm_mode + " not a valid norm mode.")

  def _get_array_attributes(self, prefix=''):
    """Get the dictionary that contain the original shapes of the arrays before being converted into tfrecord examples.

    Parameters
    ----------
    prefix : str
      Any additional prefix string/dictionary keys start with. Defaults to no additional prefix.

    Returns
    -------
    dict
      The dictionary with keys equal to those that are found in the Transform's example dicts and values are the shapes of the arrays of a single example.

    """
    att_dict = {}
    att_dict['missing_vals'] = {
      'shape': list(self.input_shape[1:]),
      'tf_type': feat.select_tf_dtype(self.input_dtype),
      'size': feat.size_from_shape(self.input_shape[1:]),
      'feature_func': feat.select_feature_func(self.input_dtype),
      'np_type': self.input_dtype
    }
    one_hots_shape = list(self.input_shape[1:]) + [len(self.index_to_cat_val)]
    att_dict['one_hots'] = {
      'shape': one_hots_shape,
      'tf_type': feat.select_tf_dtype(self.dtype),
      'size': feat.size_from_shape(one_hots_shape),
      'feature_func': feat.select_feature_func(self.dtype),
      'np_type': self.dtype
    }
    att_dict['indices'] = {
      'shape': list(self.input_shape[1:]),
      'tf_type': tf.int64,
      'size': feat.size_from_shape(self.input_shape[1:]),
      'feature_func': feat._int_feat,
      'np_type': np.int64
    }

    att_dict = self._pre(att_dict, prefix)
    return att_dict

  def calc_global_values(self, array, verbose=True):
    """Calculate all the values of the Transform that are dependent on all the examples of the dataset. (e.g. mean, standard deviation, unique category values, etc.) This method must be run before any actual transformation can be done.

    Parameters
    ----------
    array : np.ndarray
      The entire dataset.
    verbose : bool
      Whether or not to print out warnings.

    """
    # Set the input dtype
    self.input_dtype = array.dtype
    self.input_shape = array.shape

    # Pull out the relevant column

    # Get all the unique category values
    if self.valid_cats is not None:
      uniques = sorted(set(self.valid_cats))
    else:
      uniques = sorted(set(np.unique(array)))

    # If null are to be ignored then remove them.
    if self.ignore_null:
      if None in uniques:
        uniques.remove(None)
      if np.nan in uniques:
        uniques.remove(np.nan)

    # Create the mapping from category values to index in the vector and
    # vice versa
    self.index_to_cat_val = uniques
    self.cat_val_to_index = {}
    for unique_num, unique in enumerate(uniques):
      cat_val = self.index_to_cat_val[unique_num]
      self.cat_val_to_index[cat_val] = unique_num

    if self.norm_mode == 'mean_std':
      if not self.index_to_cat_val:
        raise ValueError("index_to_cat_val has no valid values.")

      # Find all the category values which are not known
      valid_cats = np.isin(array, self.index_to_cat_val)
      array = np.array(array, copy=True)

      # Replace the unknown category values with some default value.
      default_val = self.index_to_cat_val[0]
      if isinstance(default_val, float) and np.isnan(default_val):
        default_val = self.index_to_cat_val[1]
      array[~valid_cats] = default_val

      one_hots = np.zeros(list(array.shape) + [len(uniques)], dtype=np.float64)

      # Convert the category values to indices, using the cat_vat_to_index.
      indices = np.vectorize(self.cat_val_to_index.get)(array)

      # Generate all the indices of the 'indices' array. i.e. one_hot_indices is
      # equal to something like (0, 0...0), (0, 0 ... 1)... (n1, n2... nk).
      # Where n1..nk are the size of each dimension of 'indices'. Then append
      # the corresponding value from 'indices' to get the full location of where
      # a 1 should be in the one_hots array.
      one_hot_indices = np.unravel_index(np.arange(indices.size, dtype=np.int32), indices.shape)
      one_hot_indices = list(one_hot_indices) + [indices.flatten()]

      # Set all the proper locations to 1. And then undo the setting of the
      # not valid categories.
      one_hots[one_hot_indices] = 1
      one_hots[~valid_cats] = 0

      # Get the mean and standard deviation of the one_hots.
      self.mean = np.mean(one_hots, axis=self.norm_axis)
      self.std = np.std(one_hots, axis=self.norm_axis)

      # If there are any standard deviations of 0, replace them with 1's,
      # print out a warning.
      if len(self.std[self.std == 0]):
        zero_std_cat_vals = []
        for index in np.where(self.std == 0.0)[0]:
          zero_std_cat_vals.append(self.index_to_cat_val[index])

        if verbose:
          warnings.warn("WARNING: " + self.name + " has zero-valued stds at " + str(zero_std_cat_vals) + " replacing with 1's")

        self.std[self.std == 0] = 1.0

  def define_waterwork(self, array=empty, return_tubes=None):
    """Get the waterwork that completely describes the pour and pump transformations.

    Parameters
    ----------
    array : np.ndarray or empty
      The array to be transformed.

    Returns
    -------
    Waterwork
      The waterwork with all the tanks (operations) added, and names set.

    """
    # Convert the category values to indices.
    cti, cti_slots = td.cat_to_index(
      array,
      self.cat_val_to_index,
    )
    cti['missing_vals'].set_name('missing_vals')

    # Clone the indices so that a copy of 'indices' can be outputted as a tap.
    cloned, _ = td.clone(cti['target'])
    cloned['a'].set_name('indices')

    # Convert the indices into one-hot vectors.
    one_hots, _ = td.one_hot(cloned['b'], len(self.cat_val_to_index))

    # Normalize the one_hots if the norm_mode is set.
    if self.norm_mode == 'mean_std':
      one_hots, _ = one_hots['target'] - self.mean
      one_hots, _ = one_hots['target'] / self.std

    one_hots['target'].set_name('one_hots')

    if return_tubes is not None:
      ww = one_hots['target'].waterwork
      r_tubes = []
      for r_tube_key in return_tubes:
        r_tubes.append(ww.maybe_get_tube(r_tube_key))
      return r_tubes
