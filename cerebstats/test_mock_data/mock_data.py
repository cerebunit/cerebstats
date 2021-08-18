import requests
import json 
import numpy as np
import random
import os
import sys


class MockData(object):
    """
    **Available methods:**

    +-----------------------------------------+-----------------+
    | Method name                             | Method type     |
    +=========================================+=================+
    | :py:meth:`.count_files`                 | static method   |
    +-----------------------------------------+-----------------+
    | :py:meth:`.display_files`               | static method   |
    +-----------------------------------------+-----------------+
    | :py:meth:`.clear_files`                 | static method   |
    +-----------------------------------------+-----------------+
    | :py:meth:`.generate_random_data_files`  | static method   |
    +-----------------------------------------+-----------------+

    **Example generating mock data using reference dataset:**

    ::

        ref_datasetlink = "https://raw.githubusercontent.com/cerebunit/cerebdata/master/expdata/cells/PurkinjeCell/Llinas_Sugimori_1980_soma_restVm.json"
        MockData.generate_random_data_files(ref_datasetlink, sample_low=-70, sample_high=-46,num_of_files=10)

    """

    @staticmethod
    def count_files():
        """
        Counts the number of files present in the mock data directory.
        """
        target_path = "./test_quality_mock_data"
        os.makedirs(target_path, exist_ok=True)
        file_list = [name for name in os.listdir(target_path) if os.path.isfile(target_path+ '/' + name)]
        return len(file_list)

    @staticmethod
    def display_files():
        """
        Displays all the files present in the mock data directory.
        """
        target_path = "./test_quality_mock_data"
        os.makedirs(target_path, exist_ok=True)
        file_list = [name for name in os.listdir(target_path) if os.path.isfile(target_path+ '/' + name)]
        for data_file in file_list:
            print(data_file)

    @staticmethod
    def clear_files():
        """
        This function wipes or deletes all the files at the path
        where the mock data is generated.
        """
        target_path = "./test_quality_mock_data"
        os.makedirs(target_path, exist_ok=True)
        for data_file in os.listdir(target_path):
            file_path = target_path + '/' + data_file
            if(os.path.isfile(file_path)):
                os.remove(file_path)

    @staticmethod
    def generate_random_data_files(reference_datasetlink, sample_low=None, sample_high=None, num_of_files=None):
        """
        This function accepts the link to the reference dataset 
        along with the lower bound and upper bound of the raw_data
        and the number of mock data files required to be generated as arguments.
        It generates mock data randomly to calculate statistics required
        to evaluate the validation test.

        **Arguments**

        +----------+-----------------------------+---------------------------------+
        | Argument | Representation              | Value type                      |
        +==========+=============================+=================================+
        | first    | reference dataset link      | URL to dataset; Dataset must be |
        |          |                             | in JSON format                  |
        +----------+-----------------------------+---------------------------------+
        | second   | sample low                  | float                           |
        +----------+-----------------------------+---------------------------------+
        | third    | sample high                 | float                           |
        +----------+-----------------------------+---------------------------------+
        | fourth   | number of files             | int; number of files to be      |
        |          |                             | generated.                      |
        +----------+-----------------------------+---------------------------------+

        **Note**
        For the second and third arguments which is Sample low and Sample High, 
        the raw data array will be generated internally considering the Sample low as 
        lowest possible value and Sample High as the largest possible value in raw data array.

        If the raw_data key is present in the reference dataset then the newly generated mock dataset 
        will also have that raw_data key.

        If the raw_data key is not present in the reference dataset then the 
        newly generated mock dataset will also not contain this key. 
        But the raw data array would still be generated internally considering
        the sample low and sample high to calculate other values like SD, Mean etc. 
        """

        os.makedirs("./test_quality_mock_data", exist_ok=True)
        
        for i in range(1,num_of_files+1):

            ref_dataset = json.loads( requests.get(reference_datasetlink).text )
            data_dict = ref_dataset
            raw_data_arr = None

            if "sample_size" in ref_dataset.keys():
                data_dict["sample_size"] = random.randint(ref_dataset["sample_size"],100)
                raw_data_arr = [float(random.randint(sample_low,sample_high)) for x in range(data_dict['sample_size'])]
            else:
                random_sample_size = random.randint(10,100)
                raw_data_arr = [float(random.randint(sample_low,sample_high)) for x in range(random_sample_size)]


            if "raw_data" in ref_dataset.keys():
                data_dict["raw_data"] = raw_data_arr
            
            if "mean" in ref_dataset.keys():
                data_dict["mean"] = np.mean(raw_data_arr)
            
            if "SD" in ref_dataset.keys():
                data_dict["SD"] = np.std(raw_data_arr)

            with open("test_quality_mock_data/data"+str(i)+".json",'w') as outfile:
                json.dump(data_dict, outfile)
            print("Mock Data File "+ str(i)+ " generated...")
