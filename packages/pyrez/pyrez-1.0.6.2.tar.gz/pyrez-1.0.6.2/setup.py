﻿#https://realpython.com/pipenv-guide/
import os
import sys
from subprocess import call
try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from distutils.core import setup, find_packages, Command

if sys.argv[-1] == "publish":#"setup.py publish" shortcut.
    call("{} python setup.py sdist bdist_wheel".format(sys.executable), shell=False)
    call("{} twine upload dist/*".format(sys.executable), shell=False)
    sys.exit()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))) # allow setup.py to be run from any path
HERE = os.path.abspath(os.path.dirname(__file__))

def __getGithub(_end=None, _user="luissilva1044894"):
    return "https://github.com/{}/{}{}".format(_user, NAME, "/{}".format(_end) if _end else '')
def __readFile(fileName):
    with open(os.path.join(HERE, fileName), 'r', encoding="utf-8") as f:
        return f.read()
def __getReadMe(fileName="README.rst"):
    try:
        import pypandoc
        return pypandoc.convert(fileName, "rst").replace("\r","")
    except(IOError, ImportError):
        try:
            return __readFile(fileName)
        except FileNotFoundError:
            raise RuntimeError("File not found!")
def __regexFunc(pattern, packageName="pyrez"):
    import re
    pattern_match = re.search(r'^__{pattern}__\s*=\s*[\'"]([^\'"]*)[\'"]'.format(pattern=pattern), __readFile("{}/__version__.py".format(packageName)), re.MULTILINE)#r"^__{pattern}__ = ['\"]([^'\"]*)['\"]".format(meta=meta)

    return pattern_match.group(1) if pattern_match else ''
NAME, AUTHOR, AUTHOR_EMAIL, DESCRIPTION, LICENSE, URL, VERSION = __regexFunc("package_name"), __regexFunc("author"), __regexFunc("author_email"), __regexFunc("description"), __regexFunc("license"), __regexFunc("url"), __regexFunc("version")#https://www.python.org/dev/peps/pep-0440/

if sys.version_info[:2] < (3, 5) and datetime.utcnow().year >= 2020:
    print("ERROR: {} requires at least Python 3.5 to run.".format(NAME.capitalize()))
    sys.exit(1)
class BaseCommand(Command):
    """Support setup.py upload."""
    description = __doc__
    user_options = []
    @staticmethod
    def input(message):
        try:
            user_input = raw_input
        except NameError:
            user_input = input
        return user_input(message)
    @staticmethod
    def confirm(message):
        """ask a yes/no question, return result"""
        try:
            raw_input
        except NameError:
            raw_input = input
        if not sys.stdout.isatty():
            return False
        reply = BaseCommand.input("\n{message} [Y/N]:".format(message=message))
        return reply and reply[0].lower() == 'y'
    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033 {0}".format(s))#print("\033[1m{0}\033[0m".format(s))
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        pass
class DocsCommand(BaseCommand):
    """ For building the Pyrez documentation with `python setup.py docs`. This generates html, and documentation files. """
    def run(self):
        print(self.confirm("TESTING?!"))
class UploadCommand(BaseCommand):
    """Support setup.py upload."""

    description = "Build and publish the package."

    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        from shutil import rmtree
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(HERE, "dist"))
        except OSError:
            pass
        self.status("Updating Pip, Wheel and Twine…")
        call("pip install --upgrade pip setuptools wheel twine", shell=False)
        self.status("Building Source and Wheel (universal) distribution…")
        # Warning (Wheels): If your project has optional C extensions, it is recommended not to publish a universal wheel, because pip will prefer the wheel over a source installation.
        call("{} setup.py sdist bdist_wheel --universal".format(sys.executable), shell=False)
        self.status("Uploading the {} package to PyPI via Twine…".format(NAME))
        call("twine upload dist/*", shell=False)
        if self.confirm("Push tags"):
            self.status("Pushing git tags…")
            call("git tag {}".format(VERSION), shell=False)#git tag v{0}
            call("git push --tags", shell=False)
        sys.exit()
#https://docs.python.org/3/distutils/setupscript.html
#https://packaging.python.org/tutorials/packaging-projects/#description
#https://stackoverflow.com/questions/26737222/pypi-description-markdown-doesnt-work
#https://stackoverflow.com/questions/1471994/what-is-setup-py
#https://stackoverflow.com/questions/17803829/how-to-customize-a-requirements-txt-for-multiple-environments
DOCS_EXTRAS_REQUIRE = [
    "sphinx_rtd_theme>=0.4.3,<1",
    "sphinxcontrib-asyncio",
    "sphinxcontrib-websupport",
]
DEV_EXTRAS_REQUIRE = [
    "pip>=19.1.1",
    "pipenv>=2018.11.26",
    "setuptools>=41.0.1",
    "twine>=1.13.0",
    "wheel==0.33.4",
]
INSTALL_REQUIRE = [
    "requests>=2.22.0,<3",
]
LICENSES = {
    "Apache": "License :: OSI Approved :: Apache Software License",
    "BSD": "License :: OSI Approved :: BSD License",
    "GPLv3": "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "ISCL": "License :: OSI Approved :: ISC License (ISCL)",
    "LGPL": "'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
    "MIT": "License :: OSI Approved :: MIT License",
}
setup(
    # A string corresponding the package author’s name
    author=AUTHOR,

    # A string corresponding the email address of the package author
    author_email=AUTHOR_EMAIL,
    classifiers=[
        # Trove classifiers - Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers | https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        LICENSES[LICENSE],
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        #"Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Games/Entertainment",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    cmdclass={
        "upload": UploadCommand, #$ setup.py upload support.
        "docs": DocsCommand,
    },
    description=DESCRIPTION,

    # A dictionary mapping entry point group names to strings or lists of strings defining the entry points. Entry points are used to support dynamic discovery of services or plugins provided by a project.
    entry_points = {
        "console_scripts": [
            "{project_slug}={project_slug}.command_line:main".format(project_slug=NAME),#"{0}-cli={0}.command_line:main".format(NAME),
        ],
    },

    # A dictionary mapping names of “extras” (optional features of your project) to strings or lists of strings specifying what other distributions must be installed to support those features.
    extras_require={
        "dev": DEV_EXTRAS_REQUIRE,
        "docs": DOCS_EXTRAS_REQUIRE,
    },
    #download_url="https://pypi.org/project/{}/#files".format(NAME),
    #__getGithub("tarball/{}".format(VERSION))
    download_url=__getGithub("archive/{}.tar.gz".format(VERSION)),

    # If set to True, this tells setuptools to automatically include any data files it finds inside your package directories (Accept all data files and directories it finds inside your package directories that are specified by your MANIFEST.in file)
    include_package_data=True,

    # A string or list of strings specifying what other distributions need to be installed when this one is
    install_requires=INSTALL_REQUIRE,
    keywords=["pyrez", "hirez", "hi-rez", "smite", "paladins", "realmapi", "open-source", "api", "wrapper", "library", "python", "api-wrapper", "paladins-api", "smitegame", "smiteapi", "realm-api", "realm-royale", "python3", "python-3", "python-3-6"],
    license=LICENSE,
    long_description=__getReadMe(), # long_description=open ('README.rst').read () + '\n\n' + open ('HISTORY.rst').read (), #u'\n\n'.join([readme, changes]),
    long_description_content_type="text/markdown; charset=UTF-8; variant=GFM", #https://guides.github.com/features/mastering-markdown/
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,

    # A string corresponding to distribution name of your package. This can be any name as long as only contains letters, numbers, _ , and -. It also must not already taken on pypi.org
    name=NAME,
    packages=find_packages(exclude=["docs", "tests*", "examples", ".gitignore", ".github", ".gitattributes", "README.md"]),# packages=[name]
    platforms = "Any",

    # A string corresponding to a version specifier (as defined in PEP 440) for the Python version, used to specify the Requires-Python defined in PEP 345.
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,<4", #python_requires=">=3.0, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*, !=3.8.*",
    setup_requires=DEV_EXTRAS_REQUIRE,

    # is the URL for the homepage of the project. For many projects, this will just be a link to GitHub, GitLab, Bitbucket, or similar code hosting service.
    url=URL,

    # A string corresponding the version of this release
    version=VERSION,

    # A boolean flag specifying whether the project can be safely installed and run from a zip file.
    zip_safe=True,

    # An arbitrary map of URL names to hyperlinks, allowing more extensible documentation of where various resources can be found than the simple url and download_url options provide.
    project_urls={
        "Documentation": "https://{}.readthedocs.io/en/stable/".format(NAME),
        "Discord: Support Server": "https://discord.gg/XkydRPS",
        #"Changelog": "https://{}.readthedocs.io/en/stable/news.html".format(NAME),
        "Github: Issues": __getGithub("issues"),
        "Github: Repo": __getGithub(),
        "Say Thanks!": "https://saythanks.io/to/luissilva1044894",
    },
)
#python setup.py sdist bdist_wheel > create dist folder
#twine upload --repository-url https://test.pypi.org/legacy/ dist/* > upload test-pypi
#twine upload dist/* > upload pypi
#python setup.py sdit upload -r pypi > upload pypi
