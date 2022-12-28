from setuptools import find_packages, setup
from typing import List

# Defining variables
requirement_file_name = "requirements.txt"
hyphen_e_dot = "-e ."

def get_requirements() -> List[str]:
    """
    Description: This function returns packages from requirements file as a list.
    =============================================================================
    return List containing packages to be installed.
    """
    # A file named "requirements.txt", will be opened with the reading mode.
    with open(requirement_file_name) as requirement_file:
        requirement_list = requirement_file.readlines()

    # Remove new line character from the end of the line.
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    
    # Removing "-e ." from the end of the list as it is not a package name and only used to trigger "setup.py".
    if hyphen_e_dot in requirement_list:
        requirement_list.remove(hyphen_e_dot)
    return requirement_list

setup(
    name="premium",
    version="0.0.1",
    author="Satya Nerurkar",
    author_email="satyanerurkar@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements())