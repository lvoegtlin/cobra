from setuptools import setup, find_packages

setup(name='pocr',
      version='0.1.2',
      description='A tool to create and maintain your python projects',
      url='https://github.com/lvoegtlin/pocr',
      author='Lars Voegtlin',
      author_email='lars.voegtlin@unifr.ch',
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['pocr=pocr.controller:entry_point'],
      },
      include_package_data=True,
      package_data={'': ['*.yml']},
      install_requires=['keyring==19.0.1', 'pyyaml==5.1.2', 'PyInquirer==1.0.3', 'prompt_toolkit==1.0.14',
                        'pygithub==1.43.6', 'gitpython==3.0.3', 'tabulate==0.8.5', 'setuptools'],
      python_requires='>=3',
      zip_safe=False)
