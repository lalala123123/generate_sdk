import sys
import runpy
from enum import Enum
from azureml.pipeline.wrapper import dsl
from azureml.pipeline.wrapper.dsl.module import ModuleExecutor, StringParameter, InputDirectory, OutputDirectory


@dsl.module(
    name='Compare',
)
def compare(
    model1: InputDirectory(description="The first model to compare with"),
    eval_result1: InputDirectory(description="The evaluation result of first model"),
    model2: InputDirectory(description="The second model to compare"),
    eval_result2: InputDirectory(description="The evaluation result of second model"),
    best_model: OutputDirectory(description="The better model among the two"),
    metrics: StringParameter(description="The metrics to select better model"),
):
    sys.argv = [
        'compare.py',
        '--model1', str(model1),
        '--eval_result1', str(eval_result1),
        '--model2', str(model2),
        '--eval_result2', str(eval_result2),
        '--best_model', str(best_model),
        '--metrics', str(metrics),
    ]

    print(' '.join(sys.argv))
    runpy.run_path('compare.py', run_name='__main__')


if __name__ == '__main__':
    ModuleExecutor(compare).execute(sys.argv)
