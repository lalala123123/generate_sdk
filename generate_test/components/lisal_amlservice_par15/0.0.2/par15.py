import sys
import shutil
from pathlib import Path

from azureml.pipeline.wrapper import dsl
from azureml.pipeline.wrapper.dsl.module import ModuleExecutor, InputDirectory, OutputDirectory


@dsl.module(
    name="par15",
    job_type='parallel',
    parallel_inputs=[InputDirectory(name='Input Files')],
)
def par15(
        output_dir: OutputDirectory(),
        side_input: InputDirectory() = '.',
        param0: str = 'abc',
        param1: int = 10,
):
    for k, v in locals().items():
        print(f"{k}: {v}")
    print(f"This is an parallel module, please load and initialize your model here.\n")

    def run(files):
        print("Run batch, batch size =", len(files))
        results = []
        for f in files:
            print("Copying file %r to output %r" % (f, output_dir))
            target_file = str(Path(output_dir) / Path(f).name)
            shutil.copyfile(f, target_file)
            results.append(target_file)
        return results
    return run


# This main code is only used for local debugging, will never be reached in AzureML when it is a parallel module.
# See https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-parallel-run-step#write-your-inference-script
if __name__ == '__main__':
    ModuleExecutor(par15).execute(sys.argv)
