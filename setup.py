from setuptools import find_packages, setup


setup(
    name="drl_autonomous_navigation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gymnasium>=0.29",
        "numpy>=1.24",
        "PyYAML>=6.0",
        "stable-baselines3>=2.3",
    ],
)
