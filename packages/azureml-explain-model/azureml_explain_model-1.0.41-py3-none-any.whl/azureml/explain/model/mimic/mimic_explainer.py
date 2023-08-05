# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the Mimic Explainer for computing explanations on black box models or functions.

The mimic explainer trains an explainable model to reproduce the output of the given black box model.
The explainable model is called a surrogate model and the black box model is called a teacher model.
Once trained to reproduce the output of the teacher model, the surrogate model's explanation can
be used to explain the teacher model.
"""

import numpy as np

from azureml.explain.model._internal.common import _order_imp

from ..common.blackbox_explainer import BlackBoxExplainer
from ..common.explanation_utils import _generate_augmented_data

from .model_distill import model_distill
from .models import LGBMExplainableModel
from ..explanation.explanation import _create_local_explanation, _create_global_explanation, \
    _aggregate_global_from_local_explanation, _aggregate_streamed_local_explanations, \
    _create_raw_feats_global_explanation, _create_raw_feats_local_explanation, \
    _get_raw_explainer_create_explanation_kwargs
from ..dataset.decorator import tabular_decorator, init_tabular_decorator, add_transformations_to_init, \
    add_transformations_to_explain
from ..dataset.dataset_wrapper import DatasetWrapper
from azureml.explain.model._internal.constants import ExplainParams, ExplainType, ModelTask, \
    ShapValuesOutput, LoggingNamespace, MimicSerializationConstants, ExplainableModelType, LightGBMParams
import logging
import json

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    from shap.common import DenseData


class MimicExplainer(BlackBoxExplainer):
    """Defines the Mimic Explainer for explaining black box models or functions."""

    @add_transformations_to_init
    @init_tabular_decorator
    def __init__(self, model, initialization_examples, explainable_model, explainable_model_args={},
                 is_function=False, augment_data=True, max_num_of_augmentations=10, explain_subset=None,
                 features=None, classes=None, transformations=None, shap_values_output=ShapValuesOutput.DEFAULT,
                 categorical_features=[], **kwargs):
        """Initialize the MimicExplainer.

        :param model: The black box model or function (if is_function is True) to be explained.  Also known
            as the teacher model.
        :type model: model that implements predict or predict_proba or function that accepts a 2d ndarray
        :param initialization_examples: A matrix of feature vector examples (# examples x # features) for
            initializing the explainer.
        :type initialization_examples: numpy.array or pandas.DataFrame or iml.datatypes.DenseData or
            scipy.sparse.csr_matrix
        :param explainable_model: The uninitialized surrogate model used to explain the black box model.
            Also known as the student model.
        :type explainable_model: BaseExplainableModel
        :param explainable_model_args: An optional map of arguments to pass to the explainable model
            for initialization.
        :type explainable_model_args: dict
        :param is_function: Default set to false, set to True if passing function instead of model.
        :type is_function: bool
        :param augment_data: If true, oversamples the initialization examples to improve surrogate
            model accuracy to fit teacher model.  Useful for high-dimensional data where
            the number of rows is less than the number of columns.
        :type augment_data: bool
        :param max_num_of_augmentations: max number of times we can increase the input data size.
        :type max_num_of_augmentations: int
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation. Note for mimic explainer this will
            not affect the execution time of getting the global explanation. This argument is not supported when
            transformations are set.
        :type explain_subset: list[int]
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names as a list of strings. The order of the class names should match
            that of the model output.  Only required if explaining classifier.
        :type classes: list[str]
        :param transformations: List of tuples describing the column name and transformer. When transformations are
        provided, explanations are of the features before the transformation. The format for
        transformations is same as the one here: https://github.com/scikit-learn-contrib/sklearn-pandas.
        If the user is using a transformation that is not in the list of sklearn.preprocessing transformations that
        we support then we cannot take a list of more than one column as input for the transformation.
        A user can use the following sklearn.preprocessing  transformations with a list of columns since these are
        already one to many or one to one: Binarizer, KBinsDiscretizer, KernelCenterer, LabelEncoder, MaxAbsScaler,
        MinMaxScaler, Normalizer, OneHotEncoder, OrdinalEncoder, PowerTransformer, QuantileTransformer, RobustScaler,
        StandardScaler.
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
        This would not work since it is hard to make out whether my_own_transformer gives a many to many or one to many
        mapping when taking a sequence of columns.
        :type transformations: [tuple]
        :param shap_values_output: The shap values output from the explainer.  Only applies to
            tree-based models that are in terms of raw feature values instead of probabilities.
            Can be default, probability or teacher_probability. If probability or teacher_probability
            are specified, we approximate the feature importance values as probabilities instead
            of using the default values. If teacher probability is specified, we use the probabilities
            from the teacher model as opposed to the surrogate model.
        :type shap_values_output: azureml.explain.model._internal.constants.ShapValuesOutput
        :param categorical_features: Categorical feature names or indexes.
            If names are passed, they will be converted into indexes first.
        :type categorical_features: Union[list[str], list[int]]
        """
        super(MimicExplainer, self).__init__(model, is_function=is_function, **kwargs)
        self._logger.debug('Initializing MimicExplainer')

        if transformations is not None and explain_subset is not None:
            raise ValueError("explain_subset not supported with transformations")

        # Get the feature names from the initialization examples
        self.features = initialization_examples.get_features(features=features)

        # If categorical_features is a list of string column names instead of indexes, make sure to convert to indexes
        if not all(isinstance(categorical_feature, int) for categorical_feature in categorical_features):
            categorical_features = initialization_examples.get_column_indexes(self.features, categorical_features)

        # If model is a linear model or isn't able to handle categoricals, one-hot-encode categoricals
        is_tree_model = explainable_model.explainable_model_type == ExplainableModelType.TREE_EXPLAINABLE_MODEL_TYPE
        if is_tree_model and self._supports_categoricals(explainable_model):
            # Index the categorical string columns for training data
            self._column_indexer = initialization_examples.string_index(columns=categorical_features)
            self._one_hot_encoder = None
            explainable_model_args[LightGBMParams.CATEGORICAL_FEATURE] = categorical_features
        else:
            # One-hot-encode categoricals for models that don't support categoricals natively
            self._column_indexer = initialization_examples.string_index(columns=categorical_features)
            self._one_hot_encoder = initialization_examples.one_hot_encode(columns=categorical_features)

        # Note: Keeping this field as None for backwards compatibility as of April 16, 2019 (to be removed)
        # Although it seems it is needed for LinearExplainer when creating scoring model
        self.initialization_examples = None
        self.classes = classes
        self.explain_subset = explain_subset
        self._shap_values_output = shap_values_output
        # Train the mimic model on the given model
        training_data = initialization_examples.dataset
        if isinstance(training_data, DenseData):
            training_data = training_data.data

        # augment the data if necessary
        if augment_data:
            training_data = _generate_augmented_data(training_data,
                                                     max_num_of_augmentations=max_num_of_augmentations)
        explainable_model_args[ExplainParams.CLASSIFICATION] = self.predict_proba_flag
        if self._supports_shap_values_output(explainable_model):
            explainable_model_args[ExplainParams.SHAP_VALUES_OUTPUT] = shap_values_output
        else:
            self.initialization_examples = initialization_examples
        self.surrogate_model = model_distill(self.function, explainable_model, training_data,
                                             explainable_model_args)

    def _supports_categoricals(self, explainable_model):
        return issubclass(explainable_model, LGBMExplainableModel)

    def _supports_shap_values_output(self, explainable_model):
        return issubclass(explainable_model, LGBMExplainableModel)

    def _get_explain_global_kwargs(self, evaluation_examples=None, include_local=True):
        """Get the kwargs for explain_global to create a global explanation.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which to
            explain the model's output.  If specified, computes feature importances through aggregation.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param include_local: Include the local explanations in the returned global explanation.
            If evaluation examples are specified and include_local is False, will stream the local
            explanations to aggregate to global.
        :type include_local: bool
        :return: Args for explain_global.
        :rtype: dict
        """
        classification = self.predict_proba_flag
        kwargs = {ExplainParams.METHOD: ExplainType.MIMIC}
        if classification:
            kwargs[ExplainParams.CLASSES] = self.classes
        if evaluation_examples is not None:
            # Aggregate local explanation to global, either through computing the local
            # explanation and then aggregating or streaming the local explanation to global
            if include_local:
                # Get local explanation
                local_explanation = self.explain_local(evaluation_examples)
                kwargs[ExplainParams.LOCAL_EXPLANATION] = local_explanation
            else:
                if classification:
                    model_task = ModelTask.Classification
                else:
                    model_task = ModelTask.Regression
                if not isinstance(evaluation_examples, DatasetWrapper):
                    self._logger.debug('Eval examples not wrapped, wrapping')
                    evaluation_examples = DatasetWrapper(evaluation_examples)
                kwargs = _aggregate_streamed_local_explanations(self, evaluation_examples, model_task,
                                                                self.features, **kwargs)
            return kwargs
        global_importance_values = self.surrogate_model.explain_global()
        order = _order_imp(global_importance_values)
        if classification:
            kwargs[ExplainParams.MODEL_TASK] = ExplainType.CLASSIFICATION
        else:
            kwargs[ExplainParams.MODEL_TASK] = ExplainType.REGRESSION
        if self.model is not None:
            kwargs[ExplainParams.MODEL_TYPE] = str(type(self.model))
        else:
            kwargs[ExplainParams.MODEL_TYPE] = ExplainType.FUNCTION
        kwargs[ExplainParams.EXPECTED_VALUES] = None
        kwargs[ExplainParams.CLASSIFICATION] = classification
        kwargs[ExplainParams.GLOBAL_IMPORTANCE_VALUES] = global_importance_values
        kwargs[ExplainParams.GLOBAL_IMPORTANCE_RANK] = order
        kwargs[ExplainParams.FEATURES] = self.features
        return kwargs

    def explain_global(self, evaluation_examples=None, include_local=True):
        """Globally explains the blackbox model using the surrogate model.

        If evaluation_examples are unspecified, retrieves global feature importances from explainable
        surrogate model.  Note this will not include per class feature importances.  If evaluation_examples
        are specified, aggregates local explanations to global from the given evaluation_examples - which
        computes both global and per class feature importances.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which to
            explain the model's output.  If specified, computes feature importances through aggregation.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param include_local: Include the local explanations in the returned global explanation.
            If evaluation examples are specified and include_local is False, will stream the local
            explanations to aggregate to global.
        :type include_local: bool
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation. If evaluation_examples are
            passed in, it will also have the properties of a LocalExplanation. If the model is a classifier (has
            predict_proba), it will have the properties of ClassesMixin, and if evaluation_examples were passed in it
            will also have the properties of PerClassMixin.
        :rtype: DynamicGlobalExplanation
        """
        kwargs = self._get_explain_global_kwargs(evaluation_examples=evaluation_examples, include_local=include_local)
        if evaluation_examples is not None and include_local:
            return _aggregate_global_from_local_explanation(**kwargs)

        explanation = _create_global_explanation(**kwargs)

        # if transformations have been passed, then return raw features explanation
        raw_kwargs = _get_raw_explainer_create_explanation_kwargs(kwargs=kwargs)
        return explanation if self._datamapper is None else _create_raw_feats_global_explanation(
            explanation, feature_map=self._datamapper.feature_map, **raw_kwargs)

    def _get_explain_local_kwargs(self, evaluation_examples):
        """Get the kwargs for explain_local to create a local explanation.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: Args for explain_local.
        :rtype: dict
        """
        if self._column_indexer:
            evaluation_examples.apply_indexer(self._column_indexer, bucket_unknown=True)
        if self._one_hot_encoder:
            evaluation_examples.apply_one_hot_encoder(self._one_hot_encoder)
        dataset = evaluation_examples.dataset
        kwargs = {}
        if self._shap_values_output == ShapValuesOutput.TEACHER_PROBABILITY:
            # Outputting shap values in terms of the probabilities of the teacher model
            kwargs[ExplainParams.PROBABILITIES] = self.function(dataset)
        local_importance_values = self.surrogate_model.explain_local(dataset, **kwargs)
        classification = self.predict_proba_flag
        if classification:
            if self.surrogate_model.multiclass:
                # For multiclass case, convert to array
                local_importance_values = np.array(local_importance_values)
            else:
                # TODO: Eventually move this back inside the surrogate model
                # If binary case, we need to reformat the data to have importances per class
                # and convert the expected values back to the original domain
                local_importance_values = np.stack((-local_importance_values, local_importance_values))
        expected_values = self.surrogate_model.expected_values
        kwargs = {ExplainParams.METHOD: ExplainType.MIMIC}
        kwargs[ExplainParams.FEATURES] = self.features
        if classification:
            kwargs[ExplainParams.CLASSES] = self.classes
        # Reformat local_importance_values result if explain_subset specified
        if self.explain_subset:
            self._logger.debug('Getting subset of local_importance_values')
            if classification:
                local_importance_values = local_importance_values[:, :, self.explain_subset]
            else:
                local_importance_values = local_importance_values[:, self.explain_subset]
        if classification:
            kwargs[ExplainParams.MODEL_TASK] = ExplainType.CLASSIFICATION
        else:
            kwargs[ExplainParams.MODEL_TASK] = ExplainType.REGRESSION
        if self.model is not None:
            kwargs[ExplainParams.MODEL_TYPE] = str(type(self.model))
        else:
            kwargs[ExplainParams.MODEL_TYPE] = ExplainType.FUNCTION
        kwargs[ExplainParams.LOCAL_IMPORTANCE_VALUES] = local_importance_values
        kwargs[ExplainParams.EXPECTED_VALUES] = np.array(expected_values)
        kwargs[ExplainParams.CLASSIFICATION] = classification
        return kwargs

    @add_transformations_to_explain
    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Locally explains the blackbox model using the surrogate model.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: A model explanation object. It is guaranteed to be a LocalExplanation. If the model is a classifier,
            it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        kwargs = self._get_explain_local_kwargs(evaluation_examples)
        explanation = _create_local_explanation(**kwargs)

        # if transformations have been passed, then return raw features explanation
        raw_kwargs = _get_raw_explainer_create_explanation_kwargs(kwargs=kwargs)

        return explanation if self._datamapper is None else _create_raw_feats_local_explanation(
            explanation, feature_map=self._datamapper.feature_map, **raw_kwargs)

    def _save(self):
        """Return a string dictionary representation of the mimic explainer.

        Currently only supported scenario is Mimic Explainer with LightGBM surrogate model.

        :return: A serialized dictionary representation of the mimic explainer.
        :rtype: dict
        """
        properties = {}
        # save all of the properties
        for key, value in self.__dict__.items():
            if key in MimicSerializationConstants.nonify_properties:
                properties[key] = None
            elif key in MimicSerializationConstants.save_properties:
                properties[key] = value._save()
            else:
                properties[key] = json.dumps(value)
        # return a dictionary of strings
        return properties

    @staticmethod
    def _load(model, properties):
        """Load a MimicExplainer from the given properties.

        Currently only supported scenario is Mimic Explainer with LightGBM surrogate model.

        :param model: The serialized ONNX model with a scikit-learn like API.
        :type model: ONNX model.
        :param properties: A serialized dictionary representation of the mimic explainer.
        :type properties: dict
        :return: The deserialized MimicExplainer.
        :rtype: azureml.explain.model.mimic.MimicExplainer
        """
        # create the MimicExplainer without any properties using the __new__ function, similar to pickle
        mimic = MimicExplainer.__new__(MimicExplainer)
        # load all of the properties
        for key, value in properties.items():
            # Regenerate the properties on the fly
            if key in MimicSerializationConstants.nonify_properties:
                if key == MimicSerializationConstants.MODEL:
                    mimic.__dict__[key] = model
                elif key == MimicSerializationConstants.LOGGER:
                    parent = logging.getLogger(LoggingNamespace.AZUREML)
                    mimic_identity = json.loads(properties[MimicSerializationConstants.IDENTITY])
                    mimic.__dict__[key] = parent.getChild(mimic_identity)
                elif key == MimicSerializationConstants.INITIALIZATION_EXAMPLES:
                    mimic.__dict__[key] = None
                elif key == MimicSerializationConstants.FUNCTION:
                    # TODO add third case if is_function was passed to mimic explainer
                    if json.loads(properties[MimicSerializationConstants.PREDICT_PROBA_FLAG]):
                        mimic.__dict__[key] = model.predict_proba
                    else:
                        mimic.__dict__[key] = model.predict
                else:
                    raise Exception("Unknown nonify key on deserialize in MimicExplainer: {}".format(key))
            elif key in MimicSerializationConstants.save_properties:
                mimic.__dict__[key] = LGBMExplainableModel._load(value)
            elif key in MimicSerializationConstants.enum_properties:
                # NOTE: If more enums added in future, will need to handle this differently
                mimic.__dict__[key] = ShapValuesOutput(json.loads(value))
            else:
                mimic.__dict__[key] = json.loads(value)
        return mimic
