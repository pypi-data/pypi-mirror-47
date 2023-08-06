# StoveOpt
The package creates simulation files for forced draft biomass cookstoves, and uses simple optimization algorithm to assess cookstove performance as it relates to secondary air flow average velocity
[![Build Status](https://travis-ci.org/Liam-Cassidy/StoveOpt.png)](https://travis-ci.org/Liam-Cassidy/StoveOpt)

## Documentation
The documentation for the StoveOpt software is available at: <https://liam-cassidy.github.io/StoveOpt/>

## Installation
The StoveOpt software package can be installed via pip from PyPI, as follows:
```
> pip install StoveOpt
```

## Usage 
In order to excecute the software, following the installation step, the user should navigate to the directory where the package input file included; this will be where the package is installed, for example, enter on the command line:
```
> cd C:\Users\Lee\Anaconda3\Lib\site-packages\StoveOpt\
```

Once the user reaches the working directory of the package, the user should edit the input file his should /StoveOpt/inputFiles/ directory. Within the directory, the user should edit the input.yaml file to include the path and filename of the input stove geometry.
For example: 
geometry_file_directory: C:\Users\Lee\Anaconda3\Lib\site-packages\StoveOpt\stovegeom
geometry_file_name: Stove_Geometry.xlsx


Next, the package can be excecuted as a module by entering the following command into the command line:
```
> python -m StoveOpt -i [input file path]
```

The required argument, designated above as "[input file path]", should be the full path of the input.yaml file included in the package. For example:
```
> python -m StoveOpt -i C:\Users\Lee\Anaconda3\Lib\site-packages\StoveOpt\inputFiles\input.yaml
```

At the current stage of the project, the command will have edited the template case files for the subsequent simulations. An error message that shows there is no ".../probes/0/T" file indicates that a simulation hasn't been excecute.
TO EXECUTE SIMULATIONS, user should install OpenFOAM V6 (https://openfoam.org/download/), and follow directions given in the paper listed in upcoming Theory section.

*OpenFOAM was not included in the requirements file in order to respect user storage space, as OpenFOAM is a rather large application.*


## Theory
The governing theories used in the simulations and optimizations of software version 0.3.3 can be accessed at the following locations: <https://doi.org/10.5281/zenodo.3244466>

## License
The software is published under the MIT License, allowing for commercial use, modification, distribution, and private use.

## Contributing
The project is not at a release level, where contributions will be helpful. Stay posted for the project to mature, when contributions will be greatly appreciated!


## Author
The project was created by Liam Cassidy (cassidyl@oregonstate.edu)



