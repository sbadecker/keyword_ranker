from setuptools import setup

setup(name='keyword_ranker',
      version='0.1',
      description='Python implementation ranking keywords from a corpus with' +
      ' with respect to other text files using the Rapid Automatic Keyword' +
      ' Exctraction algorithm.',
      url='https://github.com/sbadecker/keyword_ranker',
      author='Stefan Decker',
      author_email='sba.decker@gmail.com',
      license='MIT',
      packages=['keyword_ranker'],
      package_data={'keyword_ranker': ['smartstoplist.txt', 'tests/test_text.txt',
                    'tests/test_kwr.py']},
      install_requires=['nltk', 'six'],
      test_suite='nose.collector',
      tests_require=['nose'],
      keywords='nlp text-mining algorithms',
      zip_safe=False)
