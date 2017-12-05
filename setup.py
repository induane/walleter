from setuptools import setup, find_packages


TESTS_REQUIRE = []
INSTALL_REQUIRES = ['boltons', 'coinkit', 'requests', 'six', 'log_color']


setup(
    name="walleter",
    version='0.0.1',
    packages=find_packages('src'),
    package_dir={"": "src"},
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    entry_points={
        "console_scripts": ["walleter = walleter.entry_point:main"]
    },
)
