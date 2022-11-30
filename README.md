# Telemetry Time Bins 🐁

### Overview

__Kaha Sciences Mouse Telemetry System__

The [Kaha Sciences Mouse Telementry System](https://www.kahasciences.com/wireless-telemetry-overview/) allows signals like movement and temperature to be tracked over time when mice are in their home cages.
This avoids the handling of mice, which inteferes with their natural physiological function.

__Purpose__

The .ASC output from the telemetry devices show the timestamps for temperature and locomotor activity values. This repository :
* Converts this output into a time binned file.
* Separates the temperature and locomotor activity data into separate sheets. <br>

__Preview of the graphical user interface__

<p align="center">
  <img src="https://user-images.githubusercontent.com/101311642/204723125-195a911b-0c59-4b09-87cc-596405825e86.png" width="360">
</p><br/>

__Input and output data__

![image](https://user-images.githubusercontent.com/101311642/204725203-df823a68-9194-43b6-b35e-528653baac58.png)

### Installation

Install [Anaconda Navigator](https://www.anaconda.com/products/distribution). <br>
Open Anaconda Prompt (on Mac open terminal and install X-Code when prompted). <br>
Download this repository to your home directory by typing in the line below.
```
git clone https://github.com/Andrews-Lab/Telemetry_time_bins.git
```
Change the directory to the place where the downloaded folder is. <br>
```
cd Telemetry_time_bins
```

Create a conda environment and install the dependencies.
```
conda env create -n TTB -f Dependencies.yaml
```

### Usage
Open Anaconda Prompt (on Mac open terminal). <br>
Change the directory to the place where the git clone was made.
```
cd Telemetry_time_bins
```

Activate the conda environment.
```
conda activate TTB
```

Run the codes.
```
python Telemetry.py
```

### Guide

View the guide about [how to analyse your telemetry data](How_to_use_telemetry_codes.pdf).

<br>

### Acknowledgements

__Author:__ <br>
[Harry Dempsey](https://github.com/H-Dempsey) (Andrews lab and Foldi lab) <br>

__Credits:__ <br>
Sarah Lockie, Zane Andrews <br>

__About the labs:__ <br>
The [Andrews lab](https://www.monash.edu/discovery-institute/andrews-lab) investigates how the brain senses and responds to hunger. <br>
The [Foldi lab](https://www.monash.edu/discovery-institute/foldi-lab) investigates the biological underpinnings of anorexia nervosa and feeding disorders. <br>
