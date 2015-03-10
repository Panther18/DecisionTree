__author__ = 'Panther'

"""
This project builds a decision tree based on the given training set and
tests the accuracy of the same comparing it against the training data and the test data.
Contents of the file:
    Main program:
        This is the driver program.
        Reads the input from the file and stores the data in thr form of list of lists.
            The number of outer lists is equal to the number of attributes of the training data + 1 class value
            The number of elements for each of the inner list corresponds to the number of the instances in the training
             data
        Import the decision tree module
        Create a head node for the decision tree and pass all of the data and the attribute details
        The result of this will have a decision tree built
        Pass each record of the training set to calculate the accuracy
        Read the test file and pass each record of the test file to calculate the accuracy

    Expected Input: Two arguments, one for each of the training data and the test data
    Output produced: Decision tree, accuracy of the training data and the accuracy of the test data
"""
import decision_tree
import sys

# open the training file
try:
    with open(sys.argv[1], "r") as readFile:
        """ --- read input --- """
        """ ---read attributes --- """
        # define variables
        attr_list = []
        attributes = []
        number_of_attributes = 0
        data_list = []
        # read and store the attribute names and its values
        attr_list = readFile.readline()
        attr_list = attr_list.split()
        # store each attribute as a dictionary and add it to the list of attributes
        # count number of attributes
        count = 0
        for each in attr_list:
            attributes.append({'Name': attr_list[count], 'Values': attr_list[count + 1]})
            attr_list.pop(count + 1)
            number_of_attributes += 1
            count += 1

        """ ---read each record and store in the list --- """
        # Define the list of lists equal to number of attributes (+1 to hold the class list values also)
        data_list = [[] for count in range(0, number_of_attributes + 1)]
        # iterate through each record and add to the list
        for each_record in readFile:
            each_record = each_record.split()
            try:
                for each_attribute in range(0, number_of_attributes + 1):
                    data_list[each_attribute].append(each_record[each_attribute])
            except IndexError as error:
                print('ERROR: copying the instances from file to list')

        # initially, all attributes are remaining
        all_attributes = []
        # copy all the attribute indexes
        for count in range(0, number_of_attributes):
            all_attributes.append(count)
        # create a root node of the decision tree
        head = decision_tree.Node(number_of_attributes, all_attributes, data_list, attributes)
        # call the build decision tree of the root node
        head.build_decision_tree()

        # print the decision tree
        head.navigate_tree(-1)
        print()
        # calculate accuracy of the training data by passing each record and comparing its class value
        check = []
        hits = miss = 0
        for record in range(0, len(data_list[0])):
            check.clear()
            check = []
            for count in range(0, number_of_attributes+1):
                check.append(data_list[count][record])
            matched = head.find_class(check)
            if matched:
                hits += 1
            else:
                miss += 1

        print()
        print('Accuracy of training set is (' + str(len(data_list[number_of_attributes])) + ' instances): ' + str((hits/(hits+miss))* 100))

        # open the test file and check for the accuracy of the decision tree built
        try:
            with open(sys.argv[2], "r") as readFile:
                test_list = [[] for count in range(0, number_of_attributes + 1)]
                # iterate through each record and add to the list
                # ignore the first line which reads the name of the attributes and their corresponding possible values
                readFile.readline()
                for each_record in readFile:
                    each_record = each_record.split()
                    try:
                        for each_attribute in range(0, number_of_attributes + 1):
                            test_list[each_attribute].append(each_record[each_attribute])
                    except IndexError as error:
                        print('ERROR: copying the instances from file to list')

            check = []
            hits = miss = 0
            for record in range(0, len(test_list[0])):
                check.clear()
                check = []
                for count in range(0, number_of_attributes+1):
                    check.append(test_list[count][record])
                matched = head.find_class(check)
                if matched:
                    hits += 1
                else:
                    miss += 1

            print('Accuracy of test set is (' + str(hits + miss) + ' instances): ' + str(round(((hits/(hits+miss))* 100),2)))

        except IndexError as missing_command_line_argument:
            print('Error missing command line argument. Expecting a path to the location ')

        except IOError:
            print('Error in opening the file')

        except:
            print(' --ERROR--. Unhandled exception has occurred. while working on the test data')

except IOError:
    print('Error in opening the file')

except IndexError as missing_command_line_argument:
    print('Error missing command line argument. Expecting a path to open the train.txt file')

except:
    print(' --ERROR--. Unhandled exception has occurred.')