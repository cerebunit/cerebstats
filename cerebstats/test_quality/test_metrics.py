import requests
import json 
import numpy as np
import random
import os
import sys
from tabulate import tabulate
from cerebstats.test_mock_data import MockData


class TestMetrics(object):    
    """
    **Available methods:**

    +-----------------------------------------+-----------------+
    | Method name                             | Method type     |
    +=========================================+=================+
    | :py:meth:`.calculate_metrics`           | instance method |
    +-----------------------------------------+-----------------+
    | :py:meth:`.get_specificity`             | instance method |
    +-----------------------------------------+-----------------+
    | :py:meth:`.get_sensitivity`             | instance method |
    +-----------------------------------------+-----------------+
    | :py:meth:`.get_npv`                     | instance method |
    +-----------------------------------------+-----------------+
    | :py:meth:`.get_ppv`                     | instance method |
    +-----------------------------------------+-----------------+

    **Steps to calculate test metrics:**
    
    1. Generate mock data using MockData class.
    2. Instantiate an TestMetrics object.
    3. Calculate Metrics.
    4. (Optional) Display Outcomes.
    5. Run getter methods to get values for Specificity, Sensitivity, Positive Predictive Value 
    and Negative Predictive Value.

    Eg.

    ::

        from cerebunit.validation_tests.cells.Purkinje import SomaRestingVmTest as srvt
        model = {"modelname":"PC2003Khaliq","modelscale":"cells"}

        TM = TestMetrics(model, srvt, alpha=0.05, epsilon=5) # alpha and epsilon are optional
        TM.calculate_metrics()
        
        TM.display_outcomes()
        specificity = TM.get_specificity()
        sensitivity = TM.get_sensitivity()
        positive_predictive_value = TM.get_ppv()
        negative_predictive_value = TM.get_npv()

    Note: alpha is the level of significance and epsilon is the boundary limit for error percentage as implemented in :py:meth:`.calculate_metrics`.
    """
    
    __TP = 0
    __TN = 0
    __FP = 0
    __FN = 0
    __num_of_files = 0

    def __init__(self, model, validation_test, alpha=0.05, epsilon=5):
        """
        This constructor method initializes the dictionary ``.model``, 
        validation test ``.validation_test``, level of significance ``.alpha``
        and error limit (Epsilon) ``.epsilon``.

        Default value for ``.alpha`` is set to 0.05 while value of ``.epsilon`` is set to 5.  
        """
        self.level_of_significance = alpha
        self.epsilon = epsilon
        self.modelscale = model["modelscale"]
        self.modelname = model["modelname"]
        self.validation_test = validation_test
        

        from executive import ExecutiveControl as ec
        self.exc = ec()
        self.desired_model = ec.choose_model( modelscale=self.modelscale, modelname=self.modelname )

    def calculate_metrics(self):
        """
        This function calculates the True Positives, False Positives, True Negatives 
        and False Negatives for the generated mock data.

        The metrics are calculated in the way as shown in the below table.

        +-----------------------------+--------------------------------------------+----------+
        | Condition 1: ``p >= alpha`` | Condition 2: ``Error Percentage < epsilon``| Outcome  |
        +=============================+============================================+==========+
        | True                        | True                                       | TP       |
        +-----------------------------+--------------------------------------------+----------+
        | True                        | False                                      | FP       |
        +-----------------------------+--------------------------------------------+----------+
        | False                       | True                                       | FN       |
        +-----------------------------+--------------------------------------------+----------+
        | False                       | False                                      | TN       |
        +-----------------------------+--------------------------------------------+----------+

        """

        self.__TP = 0
        self.__TN = 0
        self.__FP = 0
        self.__FN = 0
        self.__num_of_files = MockData.count_files()
        
        for i in range(self.__num_of_files):
            print("\nRunning "+ str(i+1) +" of "+ str(self.__num_of_files)+" \n\n")
            random_data_file = open("test_quality_mock_data/data"+ str(i+1) + ".json",'r')
            random_data = json.load(random_data_file)
            random_data_vtest = self.validation_test(random_data)
            random_data_statistics = random_data_vtest.judge(self.desired_model)
            stats = random_data_statistics.statistics
            p = stats.get('p')
            
            error_percentage = 0
            if 'u0' in stats.keys():
                error_percentage = abs((stats['u0'].magnitude - stats['u'].magnitude) / (stats['u0'].magnitude)) * 100 
            elif 'eta0' in stats.keys():
                error_percentage = abs((stats['eta0'].magnitude - stats['eta'].magnitude) / (stats['eta0'].magnitude)) * 100
            
            # Check for TP, FP, FN, TN
            if error_percentage < self.epsilon and p >= self.level_of_significance:
                self.__TP += 1
            elif error_percentage >= self.epsilon and p >= self.level_of_significance:
                self.__FP += 1
            elif error_percentage < self.epsilon and p < self.level_of_significance:
                self.__FN += 1
            elif error_percentage >= self.epsilon and p < self.level_of_significance:
                self.__TN += 1
            print("\n\n")
    
    def display_outcomes(self):
        """
        This function displays the outcomes such as True Positives, False Positives, True Negatives and False Negatives
        from the calculated metrics.
        """
        outcomes = [['TP', self.__TP],
                ['FP', self.__FP],
                ['TN', self.__TN],
                ['FN', self.__FN]] 
        print (tabulate(outcomes, headers=["Outcome", "Value"], tablefmt = 'psql'))

    def get_specificity(self):
        """
        This function returns the value of specificity based on calculated metrics. It is
        calculated as below:
        
        :math:`Specificity = \\frac{TN}{TN + FP}`
        """
        try:
            specificity = self.__TN / (self.__FP + self.__TN)
        except ZeroDivisionError:
            specificity = None
            print('Specificity: Division by Zero. Try generating mock data with different set of values.')

        return specificity

    def get_sensitivity(self):
        """
        This function returns the value of sensitivity based on calculated metrics. It is
        calculated as below:
        
        :math:`Sensitivity = \\frac{TP}{TP + FN}`
        """
        try:
            sensitivity = self.__TP / (self.__FN + self.__TP)
        except ZeroDivisionError:
            sensitivity = None
            print('Sensitivity: Division by Zero. Try generating mock data with different set of values.')

        return sensitivity

    def get_npv(self):
        """
        This function returns the value of Negative Predictive Value based on calculated metrics. 
        It is calculated as below:
        
        :math:`NPV = \\frac{TN}{TN + FN}`
        """
        try:
            npv = self.__TN / (self.__TN + self.__FN)
        except ZeroDivisionError:
            npv = None
            print('NPV: Division by Zero. Try generating mock data with different set of values.')
        
        return npv

    def get_ppv(self):
        """
        This function returns the value of Positive Predictive Value based on calculated metrics. 
        It is calculated as below:
        
        :math:`PPV = \\frac{TP}{TP + FP}`
        """
        try:
            ppv = self.__TP / (self.__TP + self.__FP)
        except ZeroDivisionError:
            ppv = None
            print('PPV: Division by Zero. Try generating mock data with different set of values.')

        return ppv

    def display_metrics(self):
        sensitivity = self.get_sensitivity()
        specificity = self.get_specificity()
        npv = self.get_npv()
        ppv = self.get_ppv()

        metrics = [['Specificity', specificity],
                ['Sensitivity', sensitivity],
                ['Negative Predictive Value', npv],
                ['Positive Predictive Value', ppv]] 
        print (tabulate(metrics, headers=["Metric", "Value"],tablefmt = 'psql'))
