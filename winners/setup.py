from setuptools import setup, find_packages

setup(
    name="fraud_detection",
    version="1.0.0",
    description="Financial fraud detection OpenEnv environment",
    packages=find_packages(),
    install_requires=[
        "gymnasium",
        "pydantic>=2.0",
        "openai",
        "numpy",
        "python-dotenv",
        "openenv>=0.1.0",
    ],
    python_requires=">=3.8",
    package_data={
        "fraud_detection": ["db/*.db"],
    },
    include_package_data=True,
)
