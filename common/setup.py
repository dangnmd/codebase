import os
import platform
import sys
from contextlib import contextmanager
from setuptools import setup

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

@contextmanager
def cd(path):
	old_dir = os.getcwd()
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(old_dir)


def _setup():
	with cd(PROJECT_DIR):
		if sys.argv[1] == 'sdist':
			if platform.system().lower() == 'windows':
				print('Only support packaging python common in Linux/macOS so far.', file=sys.stderr)
				sys.exit(-1)

			if os.system('rsync -acz --delete --exclude .git --exclude common --exclude dist . common') != 0:
				print('Failed to create common directory.', file=sys.stderr)
				sys.exit(-1)

		install_requires = []
		for requirement in open(os.path.join('common', 'requirements.txt')).readlines():
			requirement = requirement.strip()
			if requirement and requirement[0] != '#':
				install_requires.append(requirement)

		setup(name='garena-common',
			version='1.0.7',
			author='Garena',
			author_email='linf@garena.com',
			description="Garena Python common libraries.",
			url="http://git.garena.com/core-services/python_common",
			packages=['common'],
			package_data={
				'common': [
					'common/pbdata/*',
					'common/requirements.txt',
					'common/cpplib*'
				],
			},
			include_package_data=True,
			install_requires=install_requires,
		)


if __name__ == '__main__':
	_setup()
