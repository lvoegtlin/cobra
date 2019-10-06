from setuptools import setup, find_packages

setup(name='pocr',
      version='0.1',
      description='A tool to create and maintain your python projects',
      url='https://github.com/lvoegtlin/pocr',
      author='Lars Voegtlin',
      author_email='lars.voegtlin@unifr.ch',
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['pocr=pocr.controller:entry_point'],
      },
      install_requires=['keyring==19.0.1', 'pyyaml==5.1.2', 'PyInquirer==1.0.3', 'prompt_toolkit==1.0.14',
                        'pygithub==1.43.8', 'gitpython==3.0.3'],
      python_requires='>=3',
      zip_safe=False)
