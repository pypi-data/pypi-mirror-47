# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the TreeExplainer for returning explanations for tree-based models."""

import numpy as np

from ..common.structured_model_explainer import PureStructuredModelExplainer
from ..common.explanation_utils import _get_dense_examples, _convert_to_list
from ..common.aggregate import global_aggregator, init_aggregator_decorator
from ..common.explanation_utils import _scale_tree_shap
from ..dataset.decorator import tabular_decorator
from ..explanation.explanation import _create_local_explanation
from .kwargs_utils import _get_explain_global_kwargs
from azureml.explain.model._internal.constants import ExplainParams, Attributes, ExplainType, \
    ShapValuesOutput

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    import shap


@global_aggregator
class TreeExplainer(PureStructuredModelExplainer):
    """Defines the TreeExplainer for returning explanations for tree-based models."""

    @init_aggregator_decorator
    def __init__(self, model, explain_subset=None, features=None, classes=None,
                 shap_values_output=ShapValuesOutput.DEFAULT, **kwargs):
        """Initialize the TreeExplainer.

        :param model: The tree model to explain.
        :type model: lightgbm, xgboost or scikit-learn tree model
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation. The subset can be the top-k features
            from the model summary.
        :type explain_subset: list[int]
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names as a list of strings. The order of the class names should match
            that of the model output.  Only required if explaining classifier.
        :type classes: list[str]
        :param shap_values_output: The type of the output when using TreeExplainer.
            Currently only types 'default' and 'probability' are supported.  If 'probability'
            is specified, then we approximately scale the raw log-odds values from the TreeExplainer
            to probabilities.
        :type shap_values_output: azureml.explain.model._internal.constants.ShapValuesOutput
        """
        super(TreeExplainer, self).__init__(model, **kwargs)
        self._logger.debug('Initializing TreeExplainer')
        self.explainer = shap.TreeExplainer(self.model)
        self.explain_subset = explain_subset
        self.features = features
        self.classes = classes
        self._shap_values_output = shap_values_output

    @tabular_decorator
    def explain_global(self, evaluation_examples, sampling_policy=None, include_local=True):
        """Explain the model globally by aggregating local explanations to global.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
            SamplingPolicy for more information.
        :type sampling_policy: SamplingPolicy
        :param include_local: Include the local explanations in the returned global explanation.
            If include_local is False, will stream the local explanations to aggregate to global.
        :type include_local: bool
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation which also has the properties
            of LocalExplanation and ExpectedValuesMixin. If the model is a classifier, it will have the properties of
            PerClassMixin.
        :rtype: DynamicGlobalExplanation
        """
        kwargs = _get_explain_global_kwargs(sampling_policy, ExplainType.SHAP_TREE, include_local)
        return self._explain_global(evaluation_examples, **kwargs)

    def _get_explain_local_kwargs(self, evaluation_examples):
        """Get the kwargs for explain_local to create a local explanation.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: Args for explain_local.
        :rtype: dict
        """
        self._logger.debug('Explaining tree model')
        kwargs = {ExplainParams.METHOD: ExplainType.SHAP_TREE}
        if self.classes is not None:
            kwargs[ExplainParams.CLASSES] = self.classes
        kwargs[ExplainParams.FEATURES] = evaluation_examples.get_features(features=self.features)
        evaluation_examples = evaluation_examples.dataset

        # for now convert evaluation examples to dense format if they are sparse
        # until TreeExplainer sparse support is added
        shap_values = self.explainer.shap_values(_get_dense_examples(evaluation_examples))
        expected_values = None
        if hasattr(self.explainer, Attributes.EXPECTED_VALUE):
            self._logger.debug('Expected values available on explainer')
            expected_values = np.array(self.explainer.expected_value)
        classification = isinstance(shap_values, list)
        if classification and self._shap_values_output == ShapValuesOutput.PROBABILITY:
            # Re-scale shap values to probabilities for classification case
            shap_values = _scale_tree_shap(shap_values, expected_values, self.model.predict_proba(evaluation_examples))
        # Reformat shap values result if explain_subset specified
        if self.explain_subset:
            self._logger.debug('Getting subset of shap_values')
            if classification:
                for i in range(shap_values.shape[0]):
                    shap_values[i] = shap_values[i][:, self.explain_subset]
            else:
                shap_values = shap_values[:, self.explain_subset]
        local_importance_values = _convert_to_list(shap_values)
        if classification:
            kwargs[ExplainParams.MODEL_TASK] = ExplainType.CLASSIFICATION
        else:
            kwargs[ExplainParams.MODEL_TASK] = ExplainType.REGRESSION
        kwargs[ExplainParams.MODEL_TYPE] = str(type(self.model))
        kwargs[ExplainParams.LOCAL_IMPORTANCE_VALUES] = np.array(local_importance_values)
        kwargs[ExplainParams.EXPECTED_VALUES] = expected_values
        kwargs[ExplainParams.CLASSIFICATION] = classification
        return kwargs

    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Explain the model by using shap's tree explainer.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: DatasetWrapper
        :return: A model explanation object. It is guaranteed to be a LocalExplanation which also has the properties
            of ExpectedValuesMixin. If the model is a classfier, it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        kwargs = self._get_explain_local_kwargs(evaluation_examples)
        return _create_local_explanation(**kwargs)
