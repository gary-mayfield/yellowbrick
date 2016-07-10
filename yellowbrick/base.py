# yellowbrick.base
# Abstract base classes and interface for Yellowbrick.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Jun 03 10:20:59 2016 -0700
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: base.py [] benjamin@bengfort.com $

"""
Abstract base classes and interface for Yellowbrick.
"""

import matplotlib.pyplot as plt

from .exceptions import YellowbrickTypeError
from .utils import get_model_name, isestimator
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cross_validation import cross_val_predict as cvp

##########################################################################
## Base class hierarhcy
##########################################################################

class BaseVisualization(object):
    """
    The root of the visual object hierarchy that defines how yellowbrick
    creates, stores, and renders visual artifacts using matplotlib.
    """

    def render(self):
        """
        Render is the primary entry point for producing the visualization.
        """
        raise NotImplementedError(
            "All visualizations must specify their own render methodology"
        )


class FeatureVisualization(BaseVisualization, BaseEstimator, TransformerMixin):
    """
    A feature visualization class accepts as input a DataFrame or Numpy array to its :py:meth:`.fit` method
    in order to investigate features individually or together.

    FeatureVisualization is itself a transformer so that it can be used in
    a Scikit-Learn Pipeline to perform automatic visual analysis during build.
    """

    # TODO: should we add __init__ to the interface?

    def fit(self, X, y=None, **kwargs):
        """
        This FeatureVisualization subclass' :py:meth:`.fit` method which to extends scikit-learn's :py:meth:`sklearn.base.TransformerMixin.fit_transform` paradigm.

        :param X: Full dataframe or array (without targets if sending supervised data)
        :type X: :py:class:`pandas.DataFrame` or :py:class:`numpy.Array`
        :param y: Target feature(s)
        :type y: :py:class:`pandas.Series` or :py:class:`numpy.Array` depending on type of X
        :param kwargs:
        :return:
        :rtype:
        """
        pass

    def transform(self, X):
        """
        This FeatureVisualization subclass' :py:meth:`.transform` method which to extends scikit-learn's :py:meth:`sklearn.base.TransformerMixin.fit_transform` paradigm.


        :param X:
        :return:
        """
        pass

    def render(self, *args, **kwargs):
        """
        A feature visualization renders data.

        Each individual subclass determines what arguments it needs to
        render the feature visualization.

        """
        raise NotImplementedError(
            "Please specify how to render the feature visualization"
        )


class ModelVisualization(BaseVisualization, BaseEstimator):
    """
    A model visualization class should accept as input a Scikit-Learn estimator(s)
    and is itself an estimator (to be included in a Pipeline) in order to
    visualize the efficacy of a particular fitted model.
    """

    #TODO: should we add __init__ to the interface?

    def fit(self, X, y=None, **kwargs):
        pass

    def predict(self, X):
        pass

    def render(self, model=None):
        """
        A model visualization renders a model
        """
        raise NotImplementedError(
            "Please specify how to render the model visualization"
        )


class MultiModelMixin(object):
    """
    Does predict for each of the models and generates subplots.
    """

    def __init__(self, models, **kwargs):
        # Ensure models is a collection, if it's a single estimator then we
        # wrap it in a list so that the API doesn't break during render.
        if isestimator(models):
            models = [models]

        # Keep track of the models
        self.models = models
        self.names  = kwargs.pop('names', list(map(get_model_name, models)))

    def generate_subplots(self):
        """
        Generates the subplots for the number of given models.
        """
        _, axes = plt.subplots(len(self.models), sharex=True, sharey=True)
        return axes

    def predict(self, X, y):
        """
        Returns a generator containing the predictions for each of the
        internal models (using cross_val_predict and a CV=12).
        """
        for model in self.models:
            yield cvp(model, X, y, cv=12)
