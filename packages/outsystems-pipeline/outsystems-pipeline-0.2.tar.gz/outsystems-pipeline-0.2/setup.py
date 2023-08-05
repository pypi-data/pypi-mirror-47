from distutils.core import setup

NAME = 'outsystems-pipeline'
DESCRIPTION = 'Python pipeline to enable continuous testing using OutSystems.'
AUTHOR = u'João Furtado, Miguel Afonso, Rui Mendes'
EMAIL = u'joao.furtado@outsystems.com, miguel.afonso@outsystems.com, rui.mendes@outsystems.com'
URL = 'https://github.com/OutSystems/outsystems-pipeline'
KEYWORDS = [
    '',
]
PACKAGES = [
    'outsystems',
    'outsystems.bdd_framework',
    'outsystems.cicd_probe',
    'outsystems.exceptions',
    'outsystems.file_helpers',
    'outsystems.lifetime',
    'outsystems.pipeline',
    'outsystems.vars'
]

REQUIREMENTS = [
  'python-dateutil',
  'requests',
  'xunitparser',
  'unittest-xml-reporting'
]

if __name__ == '__main__':  # Do not run setup() when we import this module.
    setup(
        name=NAME,
        version='0.2',
        description=DESCRIPTION,
        keywords=' '.join(KEYWORDS),
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        packages=PACKAGES,
        install_requires=REQUIREMENTS
    )