from d3m.metadata import base as meta_base
from d3m.metadata import pipeline as meta_pipeline

import sri.pipelines.datasets as datasets
from sri.pipelines.base import BasePipeline
from sri.psl.general_relational_dataset import GeneralRelationalDataset

# These datasets are irregular.
SKIP_DATASETS = {
    # https://gitlab.datadrivendiscovery.org/MIT-LL/d3m_data_supply/issues/105
    '1491_one_hundred_plants_margin_clust',
    # https://gitlab.datadrivendiscovery.org/MIT-LL/d3m_data_supply/issues/104
    'DS01876',
    # Two target columns.
    'uu2_gp_hyperparameter_estimation',
    'uu2_gp_hyperparameter_estimation_v2',
    'LL1_penn_fudan_pedestrian',
}

class GeneralRelationalDatasetPipeline(BasePipeline):
    def __init__(self):
        super().__init__(set(datasets.get_dataset_names()) - SKIP_DATASETS, True)

    def _gen_pipeline(self):
        pipeline = meta_pipeline.Pipeline()
        pipeline.add_input(name = 'inputs')

        step_0 = meta_pipeline.PrimitiveStep(primitive_description = GeneralRelationalDataset.metadata.query())
        step_0.add_argument(
                name = 'inputs',
                argument_type = meta_base.ArgumentType.CONTAINER,
                data_reference = 'inputs.0'
        )
        step_0.add_output('produce')
        pipeline.add_step(step_0)

        # Adding output step to the pipeline
        pipeline.add_output(name = 'results', data_reference = 'steps.0.produce')

        return pipeline
