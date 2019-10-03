from setuptools import setup

setup(name='pocr',
      version='0.1',
      description='A tool to create and maintain your python projects',
      url='https://github.com/lvoegtlin/pocr',
      author='Lars Voegtlin',
      author_email='lars.voegtlin@unifr.ch',
      license='MIT',
      packages=['pocr'],
      entry_points={
          'console_scripts': ['pocr=pocr.runMe:entry_point'],
      },
      install_requires=['keyring==19.1.0', 'pyyaml==5.1.2', 'PyInquirer==1.0.3', 'prompt_toolkit==1.0.14'],
      zip_safe=False)
