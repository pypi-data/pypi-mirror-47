from setuptools import setup

setup(
    name='django-rest-easy',
    packages=['rest_easy'],
    version='1.0.3',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    install_requires=[
        'django>=1.8.0',
        'djangorestframework>=3.0.0',
        'setuptools>=36.0.1',
        'six',
    ],
    description='django-rest-easy is an extension to DRF providing QOL improvements to serializers and views.',
    long_description='django-rest-easy enables:\n'
                     ' * versioning serializers by model and schema,\n'
                     ' * creating views and viewsets using model and schema,\n'
                     ' * serializer override for a particular DRF verb, like create or update,\n'
                     ' * scoping views\' querysets and viewsets by url kwargs or request object parameters.',
    author='Krzysztof Bujniewicz',
    author_email='racech@gmail.com',
    url='https://github.com/bujniewicz/django-rest-easy',
    keywords=['django', 'DRF', 'rest framework', 'serializers', 'viewsets'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
