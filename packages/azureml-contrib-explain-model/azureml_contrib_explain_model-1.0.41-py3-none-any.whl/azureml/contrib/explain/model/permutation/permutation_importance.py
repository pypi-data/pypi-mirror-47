# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the PFIExplainer for computing global explanations on black box models or functions.

The PFIExplainer uses permutation feature importance to compute a score for each column
given a model based on how the output metric varies as each column is randomly permuted.
Although very fast for computing global explanations, PFI does not support local explanations
and can be inaccurate when there are feature interactions.
"""

import numpy as np
import scipy as sp
from sklearn.metrics import mean_absolute_error, explained_variance_score, mean_squared_error, \
    mean_squared_log_error, median_absolute_error, r2_score, average_precision_score, f1_score, \
    fbeta_score, precision_score, recall_score

from azureml.explain.model.common.base_explainer import GlobalExplainer
from azureml.explain.model.common.blackbox_explainer import BlackBoxMixin
from azureml.explain.model.dataset.decorator import add_transformations_to_init, tabular_decorator
from azureml.explain.model.explanation.explanation import _create_raw_feats_global_explanation, \
    _get_raw_explainer_create_explanation_kwargs
from ..explanation.explanation import _create_global_explanation
from azureml.explain.model._internal.constants import ExplainParams, ExplainType
from azureml.explain.model._internal.common import _order_imp
from .metric_constants import MetricConstants, error_metrics
from ..common.progress import get_tqdm

# Although we get a sparse efficiency warning when using csr matrix format for setting the
# values, if we use lil scikit-learn converts the matrix to csr which has much worse performance
import warnings
from scipy.sparse import SparseEfficiencyWarning


class PFIExplainer(GlobalExplainer, BlackBoxMixin):
    """Defines the Permutation Feature Importance Explainer for explaining black box models or functions."""

    @add_transformations_to_init
    def __init__(self, model, is_function=False, metric=None, metric_args=None, is_error_metric=False,
                 explain_subset=None, features=None, classes=None, transformations=None, seed=0,
                 for_classifier_use_predict_proba=False, show_progress=True, **kwargs):
        """Initialize the PFIExplainer.

        :param model: The black box model or function (if is_function is True) to be explained.  Also known
            as the teacher model.
        :type model: model that implements predict or predict_proba or function that accepts a 2d ndarray
        :param is_function: Default set to false, set to True if passing function instead of model.
        :type is_function: bool
        :param metric: The metric name or function to evaluate the permutation.
            Note that if a metric function is provided a higher value must be better.
            Otherwise, take the negative of the function or set is_error_metric to True.
        :type metric: str or function that accepts two arrays, y_true and y_pred.
        :param metric_args: Optional arguments for metric function.
        :type metric_args: dict
        :param is_error_metric: If custom metric function is provided, set to True if a higher
            value of the metric is better.
        :type is_error_metric: bool
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation. For permutation feature importance,
            we can shuffle, score and evaluate on the specified indexes when this parameter is set.
            This argument is not supported when transformations are set.
        :type explain_subset: list[int]
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names as a list of strings. The order of the class names should match
            that of the model output.  Only required if explaining classifier.
        :type classes: list[str]
        :param transformations: List of tuples describing the column name and transformer. When transformations are
            provided, explanations are of the features before the transformation. The format for
            transformations is same as the one here: https://github.com/scikit-learn-contrib/sklearn-pandas.
            If the user is using a transformation that is not in the list of sklearn.preprocessing transformations
            that we support then we cannot take a list of more than one column as input for the transformation.
            A user can use the following sklearn.preprocessing  transformations with a list of columns since these are
            already one to many or one to one: Binarizer, KBinsDiscretizer, KernelCenterer, LabelEncoder,
            MaxAbsScaler, MinMaxScaler, Normalizer, OneHotEncoder, OrdinalEncoder, PowerTransformer,
            QuantileTransformer, RobustScaler, StandardScaler.
            Examples for transformations that work:
            [
                (["col1", "col2"], sklearn_one_hot_encoder),
                (["col3"], None) #col3 passes as is
            ]
            [
                (["col1"], my_own_transformer),
                (["col2"], my_own_transformer),
            ]
            Example of transformations that would raise an error since it cannot be interpreted as one to many:
            [
                (["col1", "col2"], my_own_transformer)
            ]
            This would not work since it is hard to make out whether my_own_transformer gives a many to many or
            one to many mapping when taking a sequence of columns.
        :type transformations: [tuple]
        :param seed: Random number seed for shuffling.
        :type seed: int
        :param for_classifier_use_predict_proba: If specifying a model instead of a function, and the model
            is a classifier, set to True instead of the default False to use predict_proba instead of
            predict when calculating the metric.
        :type for_classifier_use_predict_proba: bool
        :param show_progress: Default to 'True'.  Determines whether to display the explanation status bar
            when using PFIExplainer.
        :type show_progress: bool
        """
        super(PFIExplainer, self).__init__(model, is_function=is_function, **kwargs)
        self._logger.debug('Initializing PFIExplainer')

        if transformations is not None and explain_subset is not None:
            raise ValueError("explain_subset not supported with transformations")

        self.features = features
        self.classes = classes
        self.explain_subset = explain_subset
        self.show_progress = show_progress
        self.seed = seed
        self.metric = metric
        self.metric_args = metric_args
        self.for_classifier_use_predict_proba = for_classifier_use_predict_proba
        self.is_error_metric = is_error_metric
        if self.metric_args is None:
            self.metric_args = {}
        # If no metric specified, pick a default based on whether this is for classification or regression
        if metric is None:
            if self.predict_proba_flag:
                self.metric = f1_score
                self.metric_args = {'average': 'micro'}
            else:
                self.metric = mean_absolute_error
        # If the metric is a string, substitute it with the corresponding evaluation function
        metric_to_func = {MetricConstants.MEAN_ABSOLUTE_ERROR: mean_absolute_error,
                          MetricConstants.EXPLAINED_VARIANCE_SCORE: explained_variance_score,
                          MetricConstants.MEAN_SQUARED_ERROR: mean_squared_error,
                          MetricConstants.MEAN_SQUARED_LOG_ERROR: mean_squared_log_error,
                          MetricConstants.MEDIAN_ABSOLUTE_ERROR: median_absolute_error,
                          MetricConstants.R2_SCORE: r2_score,
                          MetricConstants.AVERAGE_PRECISION_SCORE: average_precision_score,
                          MetricConstants.F1_SCORE: f1_score,
                          MetricConstants.FBETA_SCORE: fbeta_score,
                          MetricConstants.PRECISION_SCORE: precision_score,
                          MetricConstants.RECALL_SCORE: recall_score}
        if metric is str:
            try:
                self.metric = metric_to_func[metric]
                self.is_error_metric = metric in error_metrics
            except:
                raise Exception('Metric \'{}\' not in supported list of metrics, please pass function instead'
                                .format(metric))
        if self.classes is not None and not self.predict_proba_flag:
            if self.model is None:
                error = 'Classes is specified but function was predict, not predict_proba.'
            else:
                error = 'Classes is specified but model does not define predict_proba, only predict.'
            raise ValueError(error)

    def _add_metric(self, predict_function, shuffled_dataset, true_labels,
                    base_metric, global_importance_values, idx):
        """Compute and add the metric to the global importance values array.

        :param predict_function: The prediction function.
        :type predict_function: function
        :param shuffled_dataset: The shuffled dataset to predict on.
        :type shuffled_dataset: scipy.csr or numpy.ndarray
        :param true_labels: The true labels.
        :type true_labels: numpy.ndarray
        :param base_metric: Base metric for unshuffled dataset.
        :type base_metric: float
        :param global_importance_values: Pre-allocated array of global importance values.
        :type global_importance_values: numpy.ndarray
        """
        shuffled_prediction = predict_function(shuffled_dataset)
        if sp.sparse.issparse(shuffled_prediction):
            shuffled_prediction = shuffled_prediction.toarray()
        metric = self.metric(true_labels, shuffled_prediction, **self.metric_args)
        importance_score = base_metric - metric
        # Flip the sign of the metric if this is an error metric
        if self.is_error_metric:
            importance_score *= -1
        global_importance_values[idx] = importance_score

    def _compute_sparse_metric(self, dataset, col_idx, subset_idx, random_indexes, shuffled_dataset,
                               predict_function, true_labels, base_metric, global_importance_values):
        """Shuffle a sparse dataset column and compute the feature importance metric.

        :param dataset: Dataset used as a reference point for getting column indexes per row.
        :type dataset: scipy.csc
        :param col_idx: The column index.
        :type col_idx: int
        :param subset_idx: The subset index.
        :type subset_idx: int
        :param random_indexes: Generated random indexes.
        :type random_indexes: numpy.ndarray
        :param shuffled_dataset: The dataset to shuffle.
        :type shuffled_dataset: scipy.csr
        :param predict_function: The prediction function.
        :type predict_function: function
        :param true_labels: The true labels.
        :type true_labels: numpy.ndarray
        :param base_metric: Base metric for unshuffled dataset.
        :type base_metric: float
        :param global_importance_values: Pre-allocated array of global importance values.
        :type global_importance_values: numpy.ndarray
        """
        # Get non zero column indexes
        indptr = dataset.indptr
        indices = dataset.indices
        col_nz_indices = indices[indptr[col_idx]:indptr[col_idx + 1]]
        # Sparse optimization: If all zeros, skip the column!  Shuffling won't make a difference to metric.
        if col_nz_indices.size == 0:
            return
        data = dataset.data
        # Replace non-zero indexes with shuffled indexes
        col_random_indexes = random_indexes[0:len(col_nz_indices)]
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', SparseEfficiencyWarning)
            # Shuffle the sparse column indexes
            shuffled_dataset[col_random_indexes, col_idx] = shuffled_dataset[col_nz_indices, col_idx]
            # Get set difference and zero-out indexes that had a value but now should be zero
            difference_nz_random = list(set(col_nz_indices).difference(set(col_random_indexes)))
            difference_random_nz = list(set(col_random_indexes).difference(set(col_nz_indices)))
            # Set values that should not be sparse explicitly to zeros
            shuffled_dataset[difference_nz_random, col_idx] = np.zeros((len(difference_nz_random), 1),
                                                                       dtype=data.dtype)
            if self.explain_subset:
                idx = subset_idx
            else:
                idx = col_idx
            self._add_metric(predict_function, shuffled_dataset, true_labels,
                             base_metric, global_importance_values, idx)
            # Restore column back to previous state by undoing shuffle
            shuffled_dataset[col_nz_indices, col_idx] = shuffled_dataset[col_random_indexes, col_idx]
            shuffled_dataset[difference_random_nz, col_idx] = np.zeros((len(difference_random_nz), 1),
                                                                       dtype=data.dtype)

    def _compute_dense_metric(self, dataset, col_idx, subset_idx, random_indexes,
                              predict_function, true_labels, base_metric, global_importance_values):
        """Shuffle a dense dataset column and compute the feature importance metric.

        :param dataset: Dataset used as a reference point for getting column indexes per row.
        :type dataset: numpy.ndarray
        :param col_idx: The column index.
        :type col_idx: int
        :param subset_idx: The subset index.
        :type subset_idx: int
        :param random_indexes: Generated random indexes.
        :type random_indexes: numpy.ndarray
        :param predict_function: The prediction function.
        :type predict_function: function
        :param true_labels: The true labels.
        :type true_labels: numpy.ndarray
        :param base_metric: Base metric for unshuffled dataset.
        :type base_metric: float
        :param global_importance_values: Pre-allocated array of global importance values.
        :type global_importance_values: numpy.ndarray
        """
        # Create a copy of the original dataset
        shuffled_dataset = np.array(dataset, copy=True)
        # Shuffle one of the columns in place
        shuffled_dataset[:, col_idx] = shuffled_dataset[random_indexes, col_idx]
        if self.explain_subset:
            idx = subset_idx
        else:
            idx = col_idx
        self._add_metric(predict_function, shuffled_dataset, true_labels,
                         base_metric, global_importance_values, idx)

    def _get_explain_global_kwargs(self, evaluation_examples, true_labels):
        """Get the kwargs for explain_global to create a global explanation.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which to
            explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param true_labels: An array of true labels used for reference to compute the evaluation metric
            for base case and after each permutation.
        :type true_labels: numpy.array or pandas.DataFrame
        :return: Args for explain_global.
        :rtype: dict
        """
        classification = self.predict_proba_flag
        kwargs = {ExplainParams.METHOD: ExplainType.PFI}
        if classification:
            kwargs[ExplainParams.CLASSES] = self.classes
            kwargs[ExplainParams.MODEL_TASK] = ExplainType.CLASSIFICATION
        else:
            kwargs[ExplainParams.MODEL_TASK] = ExplainType.REGRESSION

        if self.model is not None:
            kwargs[ExplainParams.MODEL_TYPE] = str(type(self.model))
        else:
            kwargs[ExplainParams.MODEL_TYPE] = ExplainType.FUNCTION
        dataset = evaluation_examples.dataset
        # Score the model on the given dataset
        predict_function = self.function
        if self.model is not None and classification and not self.for_classifier_use_predict_proba:
            predict_function = self.model.predict
        prediction = predict_function(dataset)
        # The scikit-learn metrics can't handle sparse arrays
        if sp.sparse.issparse(true_labels):
            true_labels = true_labels.toarray()
        if sp.sparse.issparse(prediction):
            prediction = prediction.toarray()
        # Evaluate the model with given metric on the dataset
        base_metric = self.metric(true_labels, prediction, **self.metric_args)
        # Ensure we get the same results when shuffling
        if self.seed is not None:
            np.random.seed(self.seed)
        if self.explain_subset:
            # When specifying a subset, only shuffle and score on the columns specified
            column_indexes = self.explain_subset
            global_importance_values = np.zeros(len(self.explain_subset))
        else:
            column_indexes = range(dataset.shape[1])
            global_importance_values = np.zeros(dataset.shape[1])
        tqdm = get_tqdm(self._logger, self.show_progress)
        if sp.sparse.issparse(dataset):
            # Create a dataset for shuffling
            # Although lil matrix is better for changing sparsity structure, scikit-learn
            # converts matrixes back to csr for prediction which is much more expensive
            shuffled_dataset = dataset.tocsr(copy=True)
            # Convert to csc format if not already for faster column index access
            if not sp.sparse.isspmatrix_csc(dataset):
                dataset = dataset.tocsc()
            # Get max NNZ across all columns
            dataset_nnz = dataset.getnnz(axis=0)
            maxnnz = max(dataset_nnz)
            column_indexes = np.unique(np.intersect1d(dataset.nonzero()[1], column_indexes))
            # Choose random, shuffled n of k indexes
            random_indexes = np.random.choice(dataset.shape[0], maxnnz, replace=False)
            # Shuffle all sparse columns
            for subset_idx, col_idx in tqdm(enumerate(column_indexes)):
                self._compute_sparse_metric(dataset, col_idx, subset_idx, random_indexes, shuffled_dataset,
                                            predict_function, true_labels, base_metric, global_importance_values)
        else:
            random_indexes = np.random.choice(dataset.shape[0], dataset.shape[0], replace=False)
            for subset_idx, col_idx in tqdm(enumerate(column_indexes)):
                self._compute_dense_metric(dataset, col_idx, subset_idx, random_indexes, predict_function,
                                           true_labels, base_metric, global_importance_values)
        order = _order_imp(global_importance_values)
        kwargs[ExplainParams.EXPECTED_VALUES] = None
        kwargs[ExplainParams.CLASSIFICATION] = classification
        kwargs[ExplainParams.GLOBAL_IMPORTANCE_VALUES] = global_importance_values
        kwargs[ExplainParams.GLOBAL_IMPORTANCE_RANK] = order
        kwargs[ExplainParams.FEATURES] = evaluation_examples.get_features(features=self.features,
                                                                          explain_subset=self.explain_subset)
        return kwargs

    @tabular_decorator
    def explain_global(self, evaluation_examples, true_labels):
        """Globally explains the blackbox model using permutation feature importance.

        Note this will not include per class feature importances or local feature importances.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which to
            explain the model's output through permutation feature importance.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param true_labels: An array of true labels used for reference to compute the evaluation metric
            for base case and after each permutation.
        :type true_labels: numpy.array or pandas.DataFrame
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation.
            If the model is a classifier (has predict_proba), it will have the properties of ClassesMixin.
        :rtype: DynamicGlobalExplanation
        """
        kwargs = self._get_explain_global_kwargs(evaluation_examples, true_labels)

        explanation = _create_global_explanation(**kwargs)

        # if transformations have been passed, then return raw features explanation
        raw_kwargs = _get_raw_explainer_create_explanation_kwargs(kwargs=kwargs)
        return explanation if self._datamapper is None else _create_raw_feats_global_explanation(
            explanation, feature_map=self._datamapper.feature_map, **raw_kwargs)
