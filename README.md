# Geothermal Resource Assessment: Power Density
Modernisation of the Cumming power density Excel tool

## Project Context
Cumming developed the Excel in the early 90s to replace a fortran method he had been using during 80’s while undertaking global geothermal exploration and development with Unical. 

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

- For pedagogical reasons, add the equations to the streamlit app. These should be in a format that can be hidden if desired
- Remove the ability to switch the distribution (i.e., always assume that P90 is the smallest area)
- Make the summary table of results print to screen as a Pandas dataframe and make it downloadable as a csv. We will need to check how streamlit works in the background: What if more than one person is using the web app at the same time? Are we writing to disk?
- Make the data that we build the full curves from downloadable as a csv
- Plot the input values inside the plots (temp, power density P10/P90, area P10/P90)
- Keep track of multiple scenarios inside the app for comparison

## Power Users
We would like to put together a PyPI package (pip install X) for power users that includes two functions: 

1. Pass in one or more sets of parameters and return the results
2. Plot one or more results curves (plotting library TBC). Plotly is kinda preferred because you can mouse over the curves and get results back. 

Name suggestions welcome!!
- powercap
- powerdens
- geopower
- your suggestion here... 

# References 


