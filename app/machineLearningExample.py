import random

# parameters for data
data_min = 0
data_max = 10000

threshold1 = 2000
threshold2 = 4000

count_learning_data = 18000
count_test_data = 2000

# as a percentage out of 100
success_rate = 99.9


class Intelligence:
    threshold_Score1 = 0
    threshold_Score2 = 0

    def __str__(self):
        return f"Threshold Score1: {self.threshold_Score1}\nThreshold Score2: {self.threshold_Score2}"


def generateData(count):
    threshold_Score1 = threshold1
    threshold_Score2 = threshold2

    data = []
    for _ in range(count):
        Score1 = random.randint(data_min, data_max)
        Score2 = random.randint(data_min, data_max)

        # Determine label based on thresholds
        if Score1 >= threshold_Score1 and Score2 >= threshold_Score2:
            label = "Pass"
        else:
            label = "Fail"

        # Append the example to training data
        data.append({"Score1": Score1, "Score2": Score2, "label": label})

    return data


def clamp(value, min_val, max_val):
    return max(min(value, max_val), min_val)


def correctRange(intelligence):
    intelligence.threshold_Score1 = clamp(intelligence.threshold_Score1, data_min, data_max)
    intelligence.threshold_Score2 = clamp(intelligence.threshold_Score2, data_min, data_max)


def learn(intelligence, training_data):
    for example in training_data:
        # Extract features and label from the example
        Score1 = example["Score1"]
        Score2 = example["Score2"]
        label = example["label"]

        # Make a prediction based on current thresholds
        if Score1 >= intelligence.threshold_Score1 and Score2 >= intelligence.threshold_Score2:
            prediction = "Pass"
        else:
            prediction = "Fail"

        # Update thresholds based on the actual label
        if prediction != label:
            if label == "Pass":
                intelligence.threshold_Score1 -= random.randint(0, round(0.5 + data_max / 100))
                intelligence.threshold_Score2 -= random.randint(0, round(0.5 + data_max / 100))
            else:
                intelligence.threshold_Score1 += random.randint(0, round(0.5 + data_max / 100))
                intelligence.threshold_Score2 += random.randint(0, round(0.5 + data_max / 100))
            correctRange(intelligence)


def passTest(intelligence, test_data):
    count = len(test_data)
    successes = 0
    for example in test_data:
        # Extract features and label from the example
        Score1 = example["Score1"]
        Score2 = example["Score2"]
        label = example["label"]

        # Make a prediction based on current thresholds
        if Score1 >= intelligence.threshold_Score1 and Score2 >= intelligence.threshold_Score2:
            prediction = "Pass"
        else:
            prediction = "Fail"
        if prediction == label:
            successes += 1

    if successes <= success_rate * count / 100:
        print(f"The intelligence has FAILED the test with a success rate of: {successes / count * 100}% using "
              f"\n{intelligence}")
        return False

    print(f"The intelligence has PASSED the test with a success rate of: {successes / count * 100}% using "
          f"\n{intelligence}")
    return True


def trainModel(intelligence):
    training_complete = False

    while not training_complete:
        training_data = generateData(count_learning_data)
        learn(intelligence, training_data)
        test_data = generateData(count_test_data)
        training_complete = passTest(intelligence, test_data)

    return intelligence


def main():
    intelligence = Intelligence()
    intelligence = trainModel(intelligence)
    print(f"\n\nFinal thresholds are:\n{intelligence}")


main()
