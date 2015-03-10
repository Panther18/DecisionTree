__author__ = 'Panther'

"""
This module defines a class called Node.
Each object of Node reflects to each node of the decision tree.
    Each Node has the corresponding fields in
        leaf_node: indicates whether it is a leaf or not
        number_of_attributes: Total number of attributes in the training data
        remaining_attributes: Total number of remaining attributes to consider for building the decision tree
        def_attribute_index: Index of the defining attributes, the attribute based on which the tree will be split at this node
        class_index: The index to locate the class value in the data list
        number_of_zeroes: Number of zero class values seen at this node
        number_of_ones: Number of one class values seen at this node
        main_entropy: The entropy of this node
        my_class_value: Majority of the class values present at this node
        my_children: Locates each of the children and the corresponding unique value of the defining attribute that leads to this child
        my_data: Data that this Node deals with to find the best attribute
        attributes: List of attributes present in the training set
    Methods:
        __init__: Constructor of the class
        find_majority_class: This class finds the majority of the class values present in my_data
        find_my_entropy: This class calculates the main entropy of the node
        set_my_class: Calculates the class_value of the Node
            For a non-leaf node, it returns the majority of the class values
        set_class_index: Sets the number_of_zeroes and number_of_ones that appear in the class value of my_data
        set_leaf: Sets the leaf_node to true and assigns the class_value of the leaf.
        find_defining_attribute: Calculates the Information gain of each of the remaining attributes and returns the
         index of that attribute that produces the max. information gain
        fetch_data_split: Returns those set of records that matches a particular value of a particular attribute
        build_tree: Builds the tree recursively in a depth first manner
        navigate_tree: Prints the tree in a depth first manner
        find_class: Passes down the test record to the corresponding child which responds 'hit' if the class value
         matches or 'miss' otherwise
        entropy: calculates the entropy of a given number to the log of base 2 (by default)
        information_gain: Calculates the information gain of a certain attribute on a particular data
        get_me_class_list: Returns those set of records from the data that match a specific class value
        fetch_attribute_name: Returns the name of the attribute based on its index position
"""
# import required modules
import math

# define the class


class Node:
    # List the variables and its types
    remaining_attributes = my_data = my_children = []
    number_of_attributes = def_attribute_index = class_index = number_of_ones = number_of_zeroes = 0
    leaf_node = False
    main_entropy = 0
    my_class_value = "0"
    my_class_name = ""
    attributes = []
    """
    This method initializes attributes of the class
    """
    def __init__(self, number_of_attributes, rem_attributes, org_data, attributes):
        # print('start of node')
        self.remaining_attributes = []
        self.my_data = []
        self.my_children = []
        self.number_of_zeroes = self.number_of_ones = 0
        self.attributes = attributes
        # Initially let this node not consider itself as a leaf
        self.leaf_node = False
        self.my_class_value = ""
        self.number_of_ones = self.number_of_zeroes = 0
        # initialize how many attributes are there and index of the class in the data list
        self.number_of_attributes = number_of_attributes
        # print('Number of attributes are: ' + str(self.number_of_attributes))
        self.class_index = number_of_attributes
        # copy the list of remaining attributes
        for each_value in range(0, len(rem_attributes)):
            self.remaining_attributes.append(rem_attributes[each_value])

        """ --- copy the data you will work on --- """
        # define the list of lists
        self.my_data = [[] for i in range(0, number_of_attributes+1)]
        # copy the data
        for each_record in range(0, len(org_data[self.class_index])):
            for index in range(0, number_of_attributes+1):
                self.my_data[index].append(org_data[index][each_record])

    """
    This function finds the value of the class that appears the most in this data
    Since the program requirements says this is a binary classification, function uses that as an advantage to calculate the majority class element
    """
    def find_majority_class(self):
        number_of_zeroes = self.my_data[self.class_index].count('0')
        number_of_ones = len(self.my_data[self.class_index]) - number_of_zeroes
        if number_of_zeroes >= number_of_ones :
            return 0
        else:
            return 1

    """
    This function calculates the entropy of the node
    """
    def find_main_entropy(self):
        # find number of zeroes and number of ones
        total_instances = len(self.my_data[self.class_index])
        no_of_zeroes = self.my_data[self.class_index].count('0')
        no_of_ones = len(self.my_data[self.class_index]) - no_of_zeroes
        # find probability of zero and one
        probability_zero = no_of_zeroes / total_instances
        probability_one = no_of_ones / total_instances
        # find total entropy

        main_entropy = (-1) * (self.entropy(probability_zero))
        main_entropy += (-1) * (self.entropy(probability_one))
        self.main_entropy = main_entropy

    """
    This function sets the class value of a non-leaf node
    """
    def set_my_class(self):
        # find the class value that is repeating the most
        if self.number_of_zeroes >= self.number_of_ones:
            self.my_class_value = '0'
        else:
            self.my_class_value = '1'

    """
    This function sets the index of the class. Identifies the number of positive and negative class values.
    """
    def set_class_index(self):
        self.number_of_zeroes = self.my_data[self.class_index].count("0")
        self.number_of_ones = len(self.my_data[self.class_index]) - self.number_of_zeroes

    """
    This function sets the node as leaf and implicitly calls the function to calculate the node's class value
    case_number is 1: if the class value is same for all the data
                   Else: It returns the majority of the class values
    """

    def set_leaf(self, case_number):
        # set the variable to indicate you are a leaf
        self.leaf_node = True
        # print('i have set my leaf to: ' + str(self.leaf_node))
        # Class value is same for all the data
        if case_number == 1:
            self.my_class_value = self.my_data[self.class_index][0]
        # if all the attributes have same values
        elif case_number == 2:
            self.my_class_value = self.find_majority_class()
        # Zero remaining attributes
        else:
            self.my_class_value = self.find_majority_class()


    """
    This function returns the index of the defining attribute
    """

    def find_defining_attribute_index(self):
        # print('In find_defining_attribute function')
        # check how many attributes are remaining
        no_of_remaining_attributes = len(self.remaining_attributes)

        #  print('Number of remaining attribute are: ' + str(no_of_remaining_attributes))

        # there are zero defining attributes, stop forming the tree
        if no_of_remaining_attributes == 0:
            # print(self.my_data[self.class_index])
            self.set_leaf(3)
            return -1
        """ --- Return if the class values of the entire data is same --- """
        # if the class values is same for this data, then don't split
        if self.my_data[self.class_index].count(self.my_data[self.class_index][0]) == len(self.my_data[self.class_index]):
            self.set_leaf(1)
            return -1
        """ --- Return if the data has all the data same --- """
        # create an array list to hold the temporary values
        compare_with = []
        # copy the first values of each attribute
        for var in range(0, self.number_of_attributes):
            compare_with.append(self.my_data[var][0])
        # check if the first value of each attribute is same as the rest of the data
        break_loop = False
        for var in range(0, len(self.my_data[self.class_index])):
            for check in range(0, self.number_of_attributes):
                if compare_with[check] != self.my_data[check][var]:
                    break_loop = True
                    break
            if break_loop:
                break
        # if the above loop ran for all the data, it implies the attribute values of every instance is same. So return
        # -1
        if not break_loop:
            # print(self.my_data[self.class_index])
            self.set_leaf(2)
            return -1

        if no_of_remaining_attributes > 1 :
            # find the best attribute based on the largest information gain
            self.find_main_entropy()
            max_information_gain = 0
            index_of_max_information_gain = self.remaining_attributes[0]
            for each_remaining_attribute in self.remaining_attributes:
                # get the information gain of each attribute
                info_gain = self.information_gain(self.main_entropy, each_remaining_attribute, self.number_of_attributes
                                                  , self.my_data)
                if max_information_gain < info_gain:
                    max_information_gain = info_gain
                    index_of_max_information_gain = each_remaining_attribute
            return index_of_max_information_gain
        # there is only one attribute and it will be the defining attribute
        else:
            return self.remaining_attributes[0]


    """
    This function splits the original data based on the value of the remaining attribute
    """
    def fetch_data_to_split(self, unique_value):
        # define a dummy list to hold the data it will return
        dummy_list = [[] for i in range(0, self.number_of_attributes + 1)]
        total_instances = len(self.my_data[self.class_index])

        for instance in range(0, total_instances):
            # this record matches the data that will be part of the data that will be separated
            if self.my_data[self.def_attribute_index][instance] == unique_value:
                for each_attribute in range(0, self.number_of_attributes + 1):
                    dummy_list[each_attribute].append(self.my_data[each_attribute][instance])

        return dummy_list

    """
    This function builds the decision tree based on the remaining attributes, and the corresponding data
    """

    def build_decision_tree(self):
        """ ---choose the defining attribute --- """
        defining_attribute_index = self.find_defining_attribute_index()
        if defining_attribute_index == -1:
            # end of splitting the tree for this branch, return to parent function
            return
        else:
            # set the class values for the defining attribute name, value and update your attribute_remaining list
            def_attribute_unique_values = []
            self.def_attribute_index = defining_attribute_index
            self.my_class_name = self.fetch_attribute_name(self.def_attribute_index)
            def_attribute_unique_values = sorted(set(self.my_data[self.def_attribute_index]))
            self.set_class_index()
            self.set_my_class()

        """ --- split the tree with branching factor = # of unique values of the defining attribute --- """
        # modify the remaining attribute list, remove this attribute index from this list
        self.remaining_attributes.remove(self.def_attribute_index)
        try:
            for each_unique_value in def_attribute_unique_values:
                dummy_list = self.fetch_data_to_split(each_unique_value)
                """ --- send this information to the child --- """
                dummy_child = Node(self.number_of_attributes, self.remaining_attributes, dummy_list, self.attributes)
                self.my_children.append({'value': each_unique_value, 'address':dummy_child})
                dummy_child.build_decision_tree()
        except:
            print('Error in build_decision_tree')

    def navigate_tree(self, tab_count = -1):
        tab_count += 1
        # If you are a leaf node, reply the class_value
        if self.leaf_node:
            return str(self.my_class_value)

        """ --- do a depth first traversal --- """
        for travel in range(0, len(self.my_children)):
            # print the required number of tabs
            print()
            for tab in range(0, tab_count):
                print('|' + ' ', end = '')

            print('|' + self.my_class_name + '= ' + str(self.my_children[travel]['value']) + ':', end = '')
            format_print = self.my_children[travel]['address'].navigate_tree(tab_count)
            if format_print == '0'  or format_print == '1':
                print(str(format_print), end = '')

    """
    This functions passes the test data along the decision tree based on its values.
    Returns True if the class value is same as the class of the test record, else returns False
    """
    def find_class(self, test_data):
        # print(str(self.my_class_value))
        """ ---Check if you are a lead node --- """
        if self.leaf_node:
            # check if the class value is equal to the class value of the test data
            if str(self.my_class_value) == str(test_data[self.class_index]):
                return True
            else:
                return False
        # You are a non-lead node, pass the data to the corresponding child
        else:
            for each_child in range(0, len(self.my_children)):
                if self.my_children[each_child]['value'] == test_data[self.def_attribute_index]:
                    return self.my_children[each_child]['address'].find_class(test_data)
        # No child has been found for this value of the attribute,
        # so compare the class value of the test data with the majority of the class value of the parent

        if self.my_class_value == test_data[self.class_index]:
            return True
        else:
            return False

    """
    Entropy functions the value of (num / dem) * log(num/dem) to the base 2
    if numerator is 0, it will return 0
    """
    def entropy(self, num, base = 2):
        if not num == 0:
            return (num) * (math.log((num), base))
        else:
            return 0

    """
    This function returns a list of class values of those instances whose attribute_index value == value_to_match
    """
    def get_me_class_list(self, value_to_match, attribute_index, org_data):
        dummy_list = []
        count = 0
        for each_record in org_data[attribute_index]:
            if each_record == value_to_match:
                dummy_list.append(org_data[self.number_of_attributes][count])
            count += 1
        return dummy_list

    """
    This function returns the information gain of the attribute for the data passed
    attribute_index: lies between 0 - Number of attributes
    """

    def information_gain(self, main_entropy, attribute_index, total_number_of_attributes, org_data):
        number_of_attributes = total_number_of_attributes
        class_index = number_of_attributes
        total_instances = len(org_data[attribute_index])

        # find number of zeroes and number of ones

        """ ---find the conditional entropy of this attribute --- """
        # find number of unique elements of this attribute
        unique_values = set(org_data[attribute_index])
        # for each of the attribute calculate the entropy and sum them
        conditional_entropy = 0
        for each_unique_value in unique_values:
            # find all the records whose attribute_index value = each_unique_value
            this_value_appears = org_data[attribute_index].count(each_unique_value)
            # get the class list of those records whose attribute_index value == each_unique_value
            dummy_list = self.get_me_class_list(each_unique_value, attribute_index, org_data)
            # find number of zeroes and ones
            no_of_zeroes = dummy_list.count('0')
            no_of_ones = len(dummy_list) - no_of_zeroes
            # find probability of zero and one
            probability_zero = no_of_zeroes / (len(dummy_list))
            probability_one = no_of_ones / (len(dummy_list))
            # calculate entropy for this attribute when value = each_unique_value
            each_unique_value_entropy = -1 * (self.entropy(probability_zero))
            each_unique_value_entropy += -1 *(self.entropy(probability_one))

            conditional_entropy += (this_value_appears / total_instances) * (each_unique_value_entropy)

        return main_entropy - conditional_entropy

    """
    This function returns the name of the attribute based on the index of the attribute
    """
    def fetch_attribute_name(self, attribute_index):
        # check if the attribute index is less than the number of attributes present
        if (attribute_index < self.number_of_attributes) and attribute_index >= 0:
            # find the name of the attribute
            return self.attributes[attribute_index]['Name']
            # not a valid index
        else:
            return None