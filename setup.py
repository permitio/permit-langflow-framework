from setuptools import setup, find_namespace_packages

setup(
    name='permit-components',
    version='0.1.0',
    packages=find_namespace_packages(include=['base.*', 'components.*']),
    install_requires=[
        'requests>=2.32.3',
        'python-jwt==4.1.0', 
        'permit>=2.7.2,<3.0.0',
        'langflow==1.1.4.post1',
        'cryptography>=42.0.5',
    ],
    author='Ekekenta Clinton',
    author_email='zionekekenta@gmail.com',
    description='Permit.io authentication components for Langflow',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/permitio/permit-components',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)