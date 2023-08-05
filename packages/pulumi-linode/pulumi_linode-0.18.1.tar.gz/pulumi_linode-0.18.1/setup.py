# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call

class InstallPluginCommand(install):
    def run(self):
        install.run(self)
        check_call(['pulumi', 'plugin', 'install', 'resource', 'linode', 'v0.18.1'])

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pulumi_linode',
      version='0.18.1',
      description='A Pulumi package for creating and managing linode cloud resources.',
      long_description=readme(),
      cmdclass={
          'install': InstallPluginCommand,
      },
      keywords='pulumi linode',
      url='https://pulumi.io',
      project_urls={
          'Repository': 'https://github.com/pulumi/pulumi-linode'
      },
      license='Apache-2.0',
      packages=find_packages(),
      install_requires=[
          'parver>=0.2.1',
          'pulumi>=0.17.12,<0.18.0',
          'semver>=2.8.1'
      ],
      zip_safe=False)
