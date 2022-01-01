import random

import numpy as np


class DataFormatter:
    """
    From the data format obtained, organize it to the format required by model.

    Choose training, validating, and testing data sets
    """

    def __init__(self, data):
        """
        input and output can be in any format

        :param data: {'input': input data, 'output': output data }
        """
        self.data = data
        self.input_data = self.data['input']
        self.output_data = self.data['output']
        self.test_input_data = None
        self.test_output_data = None
        self.validity_input_data = None
        self.validity_output_data = None
        self.train_input_data = None
        self.train_output_data = None

    def format_data(self):
        """
        Format data to
        1. input array
        2. output array
        """
        self.input_data = self.data['input'] #np.array([])
        self.output_data = self.data['output'] # np.array([])
        return self.input_data, self.output_data

    def get_train_validity_test_data(self, train_percentage=80, validity_percentage=0):
        """

        :return:
            1. test_input_data
            2. test_output_data
        """

        num_inputs = self.input_data.shape[1]
        num_train_inputs = int(train_percentage / 100 * num_inputs)
        num_validity_inputs = int(validity_percentage / 100 * num_inputs)

        random_select_rows = random.sample(range(0, num_inputs), num_inputs)

        self.train_input_data = np.array([self.input_data[index] for index in random_select_rows[:num_train_inputs]])
        self.train_output_data = np.array([self.output_data[index] for index in random_select_rows[:num_train_inputs]])

        self.validity_input_data = np.array(
            [
                self.input_data[index]
                for index in random_select_rows[num_train_inputs:(num_train_inputs + num_validity_inputs)]
            ]
        )
        self.validity_output_data = np.array(
            [
                self.output_data[index]
                for index in random_select_rows[num_train_inputs:(num_train_inputs + num_validity_inputs)]
            ]
        )

        self.test_input_data = np.array(
            [
                self.input_data[index]
                for index in random_select_rows[(num_train_inputs + num_validity_inputs):]
            ]
        )

        self.test_output_data = np.array(
            [
                self.output_data[index]
                for index in random_select_rows[(num_train_inputs + num_validity_inputs):]
            ]
        )


class Model:
    """
    1. Create model
    2. Train and validate
    3. Score calculation
    4. Test
    5. Hyper-parameter Tuning
    6. Predict
    """

    def __init__(self, data):
        data_formatter = DataFormatter(data)



if __name__ == '__main__':
    df = DataFormatter({'input': np.random.rand(200, 10), 'output': np.random.rand(200, 1)})

    df.get_train_validity_test_data()
