
## Future work
The aim is to have a tool that operates on two levels: 

1. Simple graphical interface in Steamlit for teaching and exploring the tool - 
2. PyPI package for the power users who may want to test multiple scenarios all at once

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
