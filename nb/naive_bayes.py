import sys

sys.path.append("./common_utils")
import common_utils.common_utils as common


def bayes_probability(heading, complete_data, incomplete_data, enquired_column):
    # heading(list) of All the headings of the file
    # complete_data(list of lists) of all the completed data of the file
    # incomplete_data(list of lists) of all the incomplete data of the file
    # enquired_column(int) the column that needs to be the Y

    conditional_counts = {}
    enquired_column_classes = {}

    for data_item in complete_data:
        common.dic_inc(enquired_column_classes, data_item[enquired_column])

        for i in range(0, len(heading)):
            if i != enquired_column:
                common.dic_inc(
                    conditional_counts,
                    (heading[i], data_item[i], data_item[enquired_column]),
                )

    completed_items = []

    for incomplete_item in incomplete_data:
        partial_probs = {}
        complete_probs = {}

        probs_sum = 0

        for enquired_group in enquired_column_classes.items():
            probability = float(
                common.dic_key_count(enquired_column_classes, enquired_group[0])
            ) / len(complete_data)

            for i in range(0, len(heading)):
                if i != enquired_column:
                    probability = probability * (
                        float(
                            common.dic_key_count(
                                conditional_counts,
                                (
                                    heading[i],
                                    incomplete_item[i],
                                    enquired_group[0],
                                ),
                            )
                        )
                        / (
                            common.dic_key_count(
                                enquired_column_classes, enquired_group[0]
                            )
                        )
                    )

            partial_probs[enquired_group[0]] = probability
            probs_sum += probability

        for enquired_group in enquired_column_classes.items():
            complete_probs[enquired_group[0]] = (
                partial_probs[enquired_group[0]] / probs_sum
            )

        incomplete_item[enquired_column] = complete_probs
        completed_items.append(incomplete_item)

    return completed_items


if len(sys.argv) < 2:
    sys.exit("Please input the CSV file.")

(heading, complete_data, incomplete_data, enquired_column) = (
    common.csv_file_to_ordered_data(sys.argv[1])
)

completed_data = bayes_probability(
    heading, complete_data, incomplete_data, enquired_column
)

print(completed_data)
