import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TradeGate",                     # This is the name of the package
    version="0.0.4",                        # The initial release version
    author="Rustin Soraki",                     # Full name of the author
    description="A Trading Gateway",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=("Test, binance_f",)),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["TradeGates", "Utils"],             # Name of the python package
    package_dir={'TradeGates':'TradeGates', 'Utils':'Utils'},     # Directory of the source code of the package
    install_requires=['binance-connector', 'requests', 'apscheduler', 'websocket-client', 'urllib3', 'tzlocal<3.0']                     # Install other dependencies if any
)