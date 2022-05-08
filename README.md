# Lognormal Power Density Resource Capacity Estimate 
## Converts the Cumming Excel tool into simple Python web-app

[Click here to go to the app](https://share.streamlit.io/geothermal-resource-capacity/power-density/main/streamlit/Power-Density_streamlit.py)

---

## Contributors

Initiated during the 2021 Geothermal Hackathon and now incrementally improved.

Original tool and method design: 
- William (Bill) Cumming 

Project initiator: 
- Irene Wallis (Cubic Earth)

Collaborators: 
- Hannah Wood
- Jan Niederau 
- Jeff Jex
- Will Middlebrook

Feedback and contributors welcome.

---

## Repo structure
- data = data open sourced for this project
- docs = published papers and original excel method
- environments = environment file for conda users
- figures = plots called by either the streamlit app or other files
- notebooks = ipynb used to build the methods and explore the data
- power_user_class = advanced methods under development
- streamlit -
  - Power-Density_streamlit.py = runs streamlit app
  - requirements.txt = environment file used by streamlit sharing server
- power_dens.py = primary function for the lognormal power density method

---
## The Power Density Method

Power density is one of the methods used estimate the capacity of a conventional geothermal resource. It is typically used when there are insufficient data to undertake a numerical simulation. 

The lognormal power density excel tool was developed by William (Bill) Cumming in the 90's and documented in the paper linked below.

[Cumming (2016) Resource Capacity Estimation Using Lognormal Distributions of Power Density Derived from Producing Fields and Area Derived from Resource Conceptual Models; Advantages, Pitfalls and Remedies](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2016/Cumming.pdf)

This method relies on the development of coherent conceptual models of the resource, as described in the following paper. 

[Cumming, William (2016) Resource Conceptual Models of Volcano-Hosted Geothermal Reservoirs for Exploration Well Targeting and Resource Capacity Assessment: Construction, Pitfalls and Challenges](https://publications.mygeoenergynow.org/grc/1032377.pdf)

The subsurface geometries of the P10-P50-P90 reservoir conceptual models are defined by available resource data and analogue reasoning. The potential production area is then defined using these geometries.  

[Cumming (2009) Geothermal Resource Conceptual Models Using Surface Exploration Data](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2009/cumming.pdf)

Where only surface data and geophysical (MT) data are available, a range of possible subsurface resource geometries are possible. The below linked paper provides a continuum of reservoir geometries that may be used by resource teams as templates while they develop their conceptual model alternatives. 

[Wallis, I. C., Rowland, J. V., Cumming, W. and Dempsey, D. E., 2017, The subsurface geometry of a natural geothermal reservoir. New Zealand Geothermal Workshop: Rotorua, New Zealand.](https://www.geothermal-energy.org/pdf/IGAstandard/NZGW/2017/111_Wallis-Final_.pdf)

The power density is selected based on analogue resources. Wilmarth et al. (2015, 2020+1) compiled a database of power density for conventional geothermal reservoirs. They have provided the latest version of this database for inclusion in the data section of this repo.

[Wilmarth, M and Stimac, J (2015) Power Density in Geothermal Fields, Proceedings World Geothermal Congress 2015](https://www.geothermal-energy.org/pdf/IGAstandard/WGC/2015/16020.pdf)

Below are two case studies where this power density method was used to estimate resource capacity. 

- [Catherine Boseley, William Cumming, Luis Urzua-Monsalve, Tom Powell and Malcolm Grant (2010) A Resource Conceptual Model for the Ngatamariki Geothermal Field Based on Recent Exploration Well Drilling and 3D MT Resistivity Imaging](https://www.geothermal-energy.org/pdf/IGAstandard/WGC/2010/1146.pdf)

- [Steve Sewell, William Cumming, Lutfhie Azwar, Candice Bardsley (2012) Integrated MT and Natural State Temperature Interpretation for a Conceptual Model Supporting Reservoir Numerical Modelling and Well Targeting at the Rotokawa Geothermal Field, New Zealand](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2012/Sewell.pdf)
