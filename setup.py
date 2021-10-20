import setuptools
import os

os.system("pip install azure-ml-component==0.1.0.49823304 --extra-index-url  https://azuremlsdktestpypi.azureedge.net/CLI-SDK-Runners-Validation/49823304/")

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths

extra_files = package_files('generate_sdk/components')
extra_files.append('generate_sdk/assets.yaml')

setuptools.setup(
    name='generate_sdk',
    version='0.0.1',
    author='Example Author',
    author_email='author@example.com',
    description='Component package generated by azure-ml-component. '
                'Learn more on reference doc site: https://aka.ms/azure-ml-component-reference.',
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=['azure-ml-component'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    include_package_data=True,
    data_files=[('.', extra_files)],
)
