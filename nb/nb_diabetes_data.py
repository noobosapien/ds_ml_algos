import csv
import math
from random import randrange


def dic_inc(dic, key):
    if key is None:
        pass
    if dic.get(key, None) is None:
        dic[key] = 1
    else:
        dic[key] = dic[key] + 1


def dic_key_count(dic, key):
    if key is None:
        return 0
    if dic.get(key, None) is None:
        return 0
    else:
        return int(dic[key])


def csv_file_to_list(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def order_csv_data_complete(data):
    heading = data.pop(0)
    complete_data = []

    for item in data:
        complete_data.append(item)

    return (heading, complete_data)


def csv_file_to_ordered_data(filename):
    data = csv_file_to_list(filename)
    return order_csv_data_complete(data)


def train_test_spilt(complete_data, ratio):
    training_set = []
    testing_set = []
    testing_set_validate = []

    indices = []

    for _ in range(math.floor(ratio * len(complete_data))):
        index = randrange(0, len(complete_data))

        while index in indices:
            index = randrange(0, len(complete_data))

        indices.append(index)

    for id in range(len(complete_data)):
        item = complete_data[id]

        if id in indices:
            testing_set_validate.append(item)

            t_item = item.copy()
            t_item.pop(len(t_item) - 1)
            t_item.append(None)
            testing_set.append(t_item)
        else:
            training_set.append(item)

    return (training_set, testing_set, testing_set_validate)


def bayes_prob(heading, complete_data, incomplete_data, enquired):
    conditional_counts = {}
    enquired_col_classes = {}

    for item in complete_data:
        dic_inc(enquired_col_classes, item[enquired])

        for i in range(0, len(heading)):
            if i != enquired:
                dic_inc(conditional_counts, (heading[i], item[i], item[enquired]))

    completed_items = []

    for incomplete_item in incomplete_data:
        partial_probs = {}
        complete_probs = {}

        probs_sum = 0

        for enquired_group in enquired_col_classes.items():
            probability = float(
                dic_key_count(enquired_col_classes, enquired_group[0])
            ) / len(complete_data)

            for i in range(0, len(heading)):
                if i != enquired:
                    probability = probability * (
                        float(
                            dic_key_count(
                                conditional_counts,
                                (heading[i], incomplete_item[i], enquired_group[0]),
                            )
                        )
                        / (dic_key_count(enquired_col_classes, enquired_group[0]))
                    )

            partial_probs[enquired_group[0]] = probability
            probs_sum += probability

        for enquired_group in enquired_col_classes.items():
            if probs_sum != 0:
                complete_probs[enquired_group[0]] = (
                    partial_probs[enquired_group[0]] / probs_sum
                )

        incomplete_item[enquired] = complete_probs
        completed_items.append(incomplete_item)

    return completed_items


(heading, complete_data) = csv_file_to_ordered_data("diabetes_data.csv")
enquired = 16

(training_set, testing_set, testing_set_validate) = train_test_spilt(complete_data, 0.2)

output_probabilities = bayes_prob(heading, training_set, testing_set, enquired)

for out in output_probabilities:
    if not out[enquired]:
        continue

    enq_col = out[enquired]
    enq_col = max(enq_col, key=enq_col.get)
    out.pop(enquired)
    out.append(enq_col)

correct = 0

for i in range(len(testing_set_validate)):
    if output_probabilities[i][enquired] == testing_set_validate[i][enquired]:
        correct += 1

correct_perc = (float(correct) / len(testing_set_validate)) * 100
print(correct_perc)
