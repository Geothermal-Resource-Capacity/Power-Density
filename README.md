# Conventional Geothermal Resource Capacity Estimate with Power Density
### A project that converts the Cumming lognormal power density Excel tool to Python and delivers it as a simple web-app

---

## Project Scope

This project started during the 2021 Geothermal Hackathon, a two-day event where much was achieved thanks to the great group of people who showed up to contribute. The project is under active development. 

The aim is to have a tool that operates on three levels: 

1. Simple graphical interface in Steamlit for teaching and exploring the tool - Check out the [current version of the app](https://share.streamlit.io/geothermal-resource-capacity/power-density/main/streamlit/Power-Density_streamlit.py)
2. Expanded documentation as a Jupyter Notebook that is also deployed into Curvenote
3. PyPI package for the power users who may want to test multiple scenarios all at once

## Contributors

Original tool and method design: 
- William (Bill) Cumming 

Project initiator: 
- Irene Wallis (Cubic Earth)

Collaborators: 
- Hannah Wood
- Jan Niederau 
- Jeff Jex
- Will Middlebrook

## Repo structure
- docs = published papers and original excel method
- environments = environment file for conda users
- figures = plots called by either the streamlit app or other files
- notebooks = ipynb used to build the methods and explore the data
- power_user_class = ???
- streamlit -
  - Power-Density_streamlit.py = runs streamlit app
  - requirements.txt = environment file used by streamlit sharing server
- power_dens.py = primary function for the method

---
## The Power Density Method

Power density is one of the methods used estimate the capacity of a conventional geothermal resource. It is typically used when there are insufficient data to undertake a numerical simulation. 

The lognormal power density excel tool was developed by William (Bill) Cumming in the 90's and documented in the paper linked below.

[Cumming (2016) Resource Capacity Estimation Using Lognormal Distributions of Power Density Derived from Producing Fields and Area Derived from Resource Conceptual Models; Advantages, Pitfalls and Remedies](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2016/Cumming.pdf)

This method relies on the development of coherent conceptual models of the resource, as described in the paper below. 

[Cumming, William (2016) Resource Conceptual Models of Volcano-Hosted Geothermal Reservoirs for Exploration Well Targeting and Resource Capacity Assessment: Construction, Pitfalls and Challenges](https://publications.mygeoenergynow.org/grc/1032377.pdf)

The subsurface geometries of the P10-P50-P90 reservoir conceptual models are defined by available resource data and analogue reasoning. The potential production area is then defined using these geometries.  

[Cumming (2009) Geothermal Resource Conceptual Models Using Surface Exploration Data](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2009/cumming.pdf)

Where only surface data and geophysical (MT) data are available, a range of possible subsurface resource geometries are possible. The below linked paper provides a continuum of reservoir geometries that may be used by resource teams as templates while they develop their conceptual model alternatives. 

[Wallis, I. C., Rowland, J. V., Cumming, W. and Dempsey, D. E., 2017, The subsurface geometry of a natural geothermal reservoir. New Zealand Geothermal Workshop: Rotorua, New Zealand.](https://www.geothermal-energy.org/pdf/IGAstandard/NZGW/2017/111_Wallis-Final_.pdf)

The power density is selected based on analogue resources. Wilmarth et al. (2015, 2021) have compiled a database of power density for conventional geothermal reservoirs. They have provided the latest version of this database for inclusion in this repo:  PowerDensityDatabase_MWilmarth-JStimac-GGanefianto-2020-WGC-Data.xlsx

[Wilmarth, M and Stimac, J (2015) Power Density in Geothermal Fields, Proceedings World Geothermal Congress 2015](https://www.geothermal-energy.org/pdf/IGAstandard/WGC/2015/16020.pdf)

Below linked are two case studies where this power density method was used to estimate resource capacity. 

- [Catherine Boseley, William Cumming, Luis Urzua-Monsalve, Tom Powell and Malcolm Grant (2010) A Resource Conceptual Model for the Ngatamariki Geothermal Field Based on Recent Exploration Well Drilling and 3D MT Resistivity Imaging](https://www.geothermal-energy.org/pdf/IGAstandard/WGC/2010/1146.pdf)

- [Steve Sewell, William Cumming, Lutfhie Azwar, Candice Bardsley (2012) Integrated MT and Natural State Temperature Interpretation for a Conceptual Model Supporting Reservoir Numerical Modelling and Well Targeting at the Rotokawa Geothermal Field, New Zealand](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2012/Sewell.pdf)


---

## Future work

### Streamlit app
The streamlit app is designed for people learning to do resource assessment or resource teams that lack in-house python expertise. As such, it is a stripped-down version that walks users through the process. As such, we should aim to have some guiding text, pedagogical elements and minimize cognitive noise. 

- For pedagogical reasons, add the equations to the streamlit app. These should be in a format that can be hidden if desired. Hannah has written these by hand and committed them as a photo to the repo. 
- Add the power density plot to the streamlit app as an image 
- Remove the ability to switch the distribution (i.e., always assume that P90 is the smallest area)
- Make the summary table of results print to screen as a Pandas dataframe and make it downloadable as a csv. We will need to check how streamlit works in the background: What if more than one person is using the web app at the same time? Are we writing to disk?
- Make the data that we build the full curves from downloadable as a csv
- Plot the input values inside the plots (temp, power density P10/P90, area P10/P90)
- Keep track of multiple scenarios inside the app for comparison
- Select the distribution type (log normal or normal or other) that you want to use the analysis. Potentially add triangular and uniform (rectangular) distributions. If adding additional distribution types, the notebook may also require functionality for the user to specify values in addition to the P90 and P10 (e.g. max, min, mid). There may be a dependency between the distribution type and the types of input parameters which are required. 
-  Option to add a graph/histogram showing the distribution of each input parameter so that the user can more clearly visualize the distributions they are adding. 
-  Potential to investigate adding Monte Carlo sampling as an alternative method of combining the distributions of the input parameters (commonly used in oil and gas context)
-  Could add P10:90 ratio as a single metric for describing the relative uncertainty range of the final results. 
-  Could add probability density functions as an alternative means for viewing the results. 

### Juypter Notebook
- Irene to either tidy up the digitized power density data or get a copy of the underlying data to make a plot for the streamlit app and the Jupyter notebook

### Power Users
We would like to put together a PyPI package (pip install X) for power users that includes two functions: 

1. Pass in one or more sets of parameters and return the results
2. Plot one or more results curves (plotting library TBC). Plotly is kinda preferred because you can mouse over the curves and get results back. 

Name suggestions welcome!!
- powercap
- powerdens
- geopower
- your suggestion here... 
