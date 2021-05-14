# Geothermal Resource Assessment: Power Density
Modernisation of the Cumming power density Excel tool

## Project Context
Cumming developed the Excel in the early 90s to replace a fortran method he had been using during 80’s while undertaking global geothermal exploration and development with Unical. 

## End Goal

The aim is to have a tool that operates on three levels: 

1. Simple graphical interface in Steamlit for teaching and exploring the tool
2. Expanded documentation as a Jupyter Notebook that is also deployed into Curvenote
3. PyPI package for the power users who may want to test multiple scenarios all at once

There will still be some work to tidy this up after the Hackathon, but we have already achieved most of this! 

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


# Future work

## Streamlit app
The streamlit app is designed for people learning to do resource assessment or resource teams that lack in-house python expertise. As such, it is a stripped-down version that walks users through the process. As such, we should aim to have some guiding text, pedagogical elements and minimise cognitive noise. 

- For pedagogical reasons, add the equations to the streamlit app. These should be in a format that can be hidden if desired. Hannah has written these by hand and committed them as a photo to the repo. 
- Add the power density plot to the streamlit app as an image 
- Remove the ability to switch the distribution (i.e., always assume that P90 is the smallest area)
- Make the summary table of results print to screen as a Pandas dataframe and make it downloadable as a csv. We will need to check how streamlit works in the background: What if more than one person is using the web app at the same time? Are we writing to disk?
- Make the data that we build the full curves from downloadable as a csv
- Plot the input values inside the plots (temp, power density P10/P90, area P10/P90)
- Keep track of multiple scenarios inside the app for comparison
- Select the distribution type (log normal or normal or other) that you want to use the analysis 

## Juypter Notebook
- Irene to either tidy up the digitised power density data or get a copy of the underlying data to make a plot for the streamlit app and the Jupyter notebook

## Power Users
We would like to put together a PyPI package (pip install X) for power users that includes two functions: 

1. Pass in one or more sets of parameters and return the results
2. Plot one or more results curves (plotting library TBC). Plotly is kinda preferred because you can mouse over the curves and get results back. 

Name suggestions welcome!!
- powercap
- powerdens
- geopower
- your suggestion here... 

# Resources 

The P10-P90 areas passed into the tool are developed using the conceptual model method. 

The subsurface geometries of the P10-P50-P90 reservoir are defined by available resource data and analogue reasoning. Wallis et al. (2017) provides a continuum of reservoir geometries that may be used by resource teams as templates while they develop their conceptual model alternatives. 

Cumming power density tool

Wallis, I. C., Rowland, J. V., Cumming, W. and Dempsey, D. E., 2017, The subsurface geometry of a natural geothermal reservoir. New Zealand Geothermal Workshop: Rotorua, New Zealand. [link to file](https://www.geothermal-energy.org/pdf/IGAstandard/NZGW/2017/111_Wallis-Final_.pdf)

Cumming (2009) Geothermal Resource Conceptual Models Using Surface Exploration Data

[link to file](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2009/cumming.pdf)


Catherine Boseley, William Cumming, Luis Urzua-Monsalve, Tom Powell and Malcolm Grant (2010) A Resource Conceptual Model for the Ngatamariki Geothermal Field Based on Recent Exploration Well Drilling and 3D MT Resistivity Imaging

[link to file](https://www.geothermal-energy.org/pdf/IGAstandard/WGC/2010/1146.pdf)


Steve Sewell, William Cumming, Lutfhie Azwar, Candice Bardsley (2012) Integrated MT and Natural State Temperature Interpretation for a Conceptual Model Supporting Reservoir Numerical Modelling and Well Targeting at the Rotokawa Geothermal Field, New Zealand 

[link to file](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2012/Sewell.pdf)

Cumming, William (2016) Resource Conceptual Models of Volcano-Hosted Geothermal Reservoirs for Exploration Well Targeting and Resource Capacity Assessment: Construction, Pitfalls and Challenges

[link to file](https://publications.mygeoenergynow.org/grc/1032377.pdf)

Cumming (2016) Resource Capacity Estimation Using Lognormal Distributions of Power Density Derived from Producing Fields and Area Derived from Resource Conceptual Models; Advantages, Pitfalls and Remedies

[link to file](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2016/Cumming.pdf)
