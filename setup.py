from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This returns list of required Libraries 
    """
    requirement_list:List[str] = []
    with open('requirements.txt','r') as myfile:
        requirement_list = myfile.read().splitlines()

    return requirement_list

# print(get_requirements())
# This function all the python packages inside the packages that are made by you
setup(
    name='sensor',
    version='0.0.1',
    author='Darshan',
    author_email='darshanbhiwapurkar@gmail.com',
    description='sensor fault detection',
    url='https://github.com/Darshbhi99/sensor-fault-detection.git',
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires='>=3.7'
)

