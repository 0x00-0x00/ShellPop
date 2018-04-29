from setuptools import setup
from setuptools.command.install import install
import os
import platform
import shutil


LINUX_SCRIPT_PATH = "/usr/local/bin/shellpop"
WINDOWS_SCRIPT_PATH = "C:\\Users\\Public\\Program Files\\Shellpop\\shellpop"

# Platform detection snippet added by Touhid Shaik
if platform.system() == "Linux":
    SCRIPTS = "bin/shellpop"
elif platform.system() == "Windows":
    
    # This checks and ensures that script is installed, even if there are no folders.
    if os.path.isdir("C:\\Users\\Public\\Program Files") is False:
      os.mkdir("C:\\Users\\Public\\Program Files")
    
    if os.path.isdir("C:\\Users\\Public\\Program Files\\ShellPop") is False:
      os.mkdir("C:\\Users\\Public\\Program Files\\ShellPop")
      
    shutil.copyfile("bin/shellpop", WINDOWS_SCRIPT_PATH)
    SCRIPTS = WINDOWS_SCRIPT_PATH
else:
    pass

setup(name='shellpop',
      version='0.3.3.8',
      description='Bind and Reverse shell code generator to aid Penetration Tester in their work.',
      url='https://github.com/0x00-0x00/ShellPop.git',
      author='zc00l, lowfuel, touhid_shaik',
      author_email='andre.marques@fatec.sp.gov.br',
      license='MIT',
      packages=['shellpop'],
      package_dir={"shellpop": "src"},
      package_data={
          "shellpop": ["src/*"],
      },

        # No data files yet.
      #data_files=[
      #    ('shellpop', ['src/agent_list.json']),
      #],

      scripts=["bin/shellpop"],
      zip_safe=False)
