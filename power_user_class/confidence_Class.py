#libs for computation
import numpy as np
import scipy
from scipy.stats import norm, lognorm
import pandas as pd

class prospect_Confidence(object):
    """  		  	   		     		  		  		    	 		 		   		 		  

  		  	   		     		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, prints information for debugging.
        If verbose = False your code does not generate ANY output.
    """
    # constructor
    def __init__(self, verbose = False):
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method
        """
        self.verbose = verbose


    def calculate_cumulative_conf(self,
                                  areaP90: float=1.,
                                  areaP10: float=10.,
                                  pdP90: float=10.,
                                  pdP10: float=24):
        """Calculate cumulative confidence level for expected development size in MW
        Args:
            areaP90 (float): pessimistic area in sqkm
            areaP10 (float): optimistic area in sqkm
            pdP90 (float): pessimistic power density in MWe/sqkm
            pdP10 (float): optimistic power density in MWe/sqkm

        Returns:
            prob_df (pandas Dataframe): cumulative confidence curve in Reservoir Size
        """

        assert isinstance(areaP90, float), "areaP90 variable data type expected to be float"
        assert isinstance(areaP10, float), "areaP10 variable data type expected to be float"
        assert isinstance(pdP90, float), "pdP90 variable data type expected to be float"
        assert isinstance(pdP10, float), "pdP10 variable data type expected to be float"

        if self.verbose:
            print("areaP90: " , areaP90 )
            print("areaP10: " , areaP10 )
            print("pdP90: " , pdP90 )
            print("pdP10: " , pdP10 )

        # calculate area > 250 °C
        area_mu = ((np.log(areaP90)+np.log(areaP10))/2)
        area_sigma = (np.log(areaP10)-np.log(areaP90))/((norm.ppf(0.9)-(norm.ppf(0.1))))

        # calculate powerdensity mean and standard dev
        powerdens_mu = ((np.log(pdP90)+np.log(pdP10))/2)
        powerdens_sigma = (np.log(pdP10)-np.log(pdP90))/((norm.ppf(0.9)-(norm.ppf(0.1))))


        capacity_mu = area_mu + powerdens_mu
        capacity_sigma = ((area_sigma**2)+(powerdens_sigma**2))**0.5
        eds = [lognorm.ppf(x/100, capacity_sigma, loc=0, scale=np.exp(capacity_mu)) for x in range(0,100)]
        indx = list(np.arange(0,100)[::-1])
        edsepc_tups = list(zip(indx,eds))
        prob_df = pd.DataFrame(edsepc_tups, columns = ['Cumulative confidence (%)', 'expected development size (MW)'])

        return prob_df


    def add_scenarios(self,
                   areaP90,
                   areaP10,
                   pdP90,
                   pdP10,
                   ):
        """Calculate cumulative confidence level for expected development size in MW
        Args:
            areaP90 (array or list): pessimistic area in sqkm
            areaP10 (array or list): optimistic area in sqkm
            pdP90 (array or list): pessimistic power density in MWe/sqkm
            pdP10 (array or list): optimistic power density in MWe/sqkm

        Returns:
            prob_df (pandas Dataframe): cumulative confidence curve in Reservoir Size by different scenarios
        """

        try:

            # iterating over scenarios
            list_scenario_df = []
            for ap90, ap10, pd90, pd10 in zip(areaP90,areaP10,pdP90,pdP10):









