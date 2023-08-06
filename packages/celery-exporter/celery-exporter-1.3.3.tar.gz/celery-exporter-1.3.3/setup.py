import io

from setuptools import setup

long_description = "See https://github.com/OvalMoney/celery-exporter"
with io.open("README.md", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="celery-exporter",
    description="Prometheus metrics exporter for Celery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.3.3",
    author="Fabio Todaro",
    license="MIT",
    author_email="fbregist@gmail.com",
    url="https://github.com/OvalMoney/celery-exporter",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    packages=["celery_exporter"],
    install_requires=["click>=7" "celery>=4", "prometheus_client>=0.0.20"],
    entry_points={
        "console_scripts": ["celery-exporter = celery_exporter.__main__:main"]
    },
)
