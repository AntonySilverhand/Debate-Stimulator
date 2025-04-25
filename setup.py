from setuptools import setup, find_packages

setup(
    name="debate-stimulator",
    version="1.0.0",
    description="British Parliamentary debate practice with AI opponents",
    author="Antony",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "asyncio>=3.4.3",
        "requests>=2.31.0",
        "httpx>=0.24.0",
        "socksio>=1.0.0",
        "pysocks>=1.7.1",
        "sounddevice>=0.4.6",
        "soundfile>=0.12.1",
    ],
    entry_points={
        'console_scripts': [
            'debate-simulator=main:run_debate',
        ],
    },
    python_requires='>=3.9',
)
