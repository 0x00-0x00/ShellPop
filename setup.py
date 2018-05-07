from setuptools import setup
from setuptools.command.install import install
from subprocess import Popen, PIPE
import os

def applyChanges():
    proc = Popen("source ~/.bashrc", stdout=PIPE, stderr=PIPE, shell=True)
    _, _ = proc.communicate()
    return None

def activateTabComplete():
    proc = Popen("activate-global-python-argcomplete", stdout=PIPE, stderr=PIPE, shell=True)
    _, _ = proc.communicate()
    return True if proc.poll() is 0 else False

def autoComplete():
    """
    Get the content required to register Shellpop into tab auto-completion
    @zc00l
    """
    proc = Popen("register-python-argcomplete shellpop", stdout=PIPE, stderr=PIPE, shell=True)
    stdout, _ = proc.communicate()
    return stdout

class CustomInstall(install):
    def run(self):
        install.run(self)
        bashrc_file = os.environ["HOME"] + os.sep + ".bashrc"
        if not os.path.exists(bashrc_file):
            return None
        with open(bashrc_file, "r") as f:
            bashrc_content = f.read()
        if "shellpop" not in bashrc_content:
            print("Registering shellpop in .bashrc for auto-completion ...")
            activateTabComplete() # this will enable auto-complete feature.

            # This will write the configuration needed in .bashrc file
            with open(bashrc_file, "a") as f:
                f.write("\n{0}\n".format(autoComplete()))
            print("Auto-completion has been installed.")
            applyChanges()

setup(name='shellpop',
      version='0.3.5',
      description='Bind and Reverse shell code generator to aid Penetration Tester in their work.',
      url='https://github.com/0x00-0x00/ShellPop.git',
      author='zc00l, lowfuel, touhidshaikh',
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
      zip_safe=False,
      cmdclass={'install':CustomInstall})
