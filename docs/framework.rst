Framework Extensions
====================

.. note::

   The custom step registry described in earlier drafts (``register_function_step``)
   has been removed in v1.0.0. ``dskit.framework`` no longer exists as a public
   submodule. Use ``PreprocessingPipeline`` with the built-in preprocessing
   steps (``fill_missing``, ``cap_outliers``, ``compute_scaling_params``,
   ``apply_scaling``) for standard pipelines. For custom transformations, wrap
   your logic in a sklearn-compatible transformer and pass it directly to your
   own pipeline.