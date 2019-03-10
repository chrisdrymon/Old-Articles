import tensorflow as tf
import pandas as pd
import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#tf.logging.set_verbosity(tf.logging.INFO)


def load_data(y_name='Bracket'):
    """Returns the article dataset as (train_x, train_y), (test_x, test_y)."""

    df_path = '/home/chris/Desktop/KrippTrain.csv'

    df = pd.read_csv(df_path)

    df = df.sample(frac=1).reset_index(drop=True)
    splitNum = int(df.shape[0] * .8)
    krippTrain = df[:splitNum]
    krippTest = df[splitNum:]

    train_x, train_y = krippTrain, krippTrain.pop(y_name)

    test_x, test_y = krippTest, krippTest.pop(y_name)

    return (train_x, train_y), (test_x, test_y)


def train_input_fn(features, labels, element_count, batch_size):
    """An input function for training"""

    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    dataset = dataset.shuffle(element_count).repeat().batch(batch_size)

    return dataset


def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features = dict(features)
    if labels is None:
        # If no labels, use only features.
        inputs = features
        print("An input had no label!")
    else:
        inputs = (features, labels)

    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset


(train_X, train_Y), (test_X, test_Y) = load_data()

elementCount = train_X.shape[0]
batchSize = 50
epochs = 10
trainSteps = int(elementCount/batchSize)*epochs
print(trainSteps, "training steps.")

my_feature_columns = []

dayColumn = tf.feature_column.\
    categorical_column_with_vocabulary_list(key='Day', vocabulary_list=["Sunday","Monday","Tuesday","Wednesday",\
                                                                    "Thursday","Friday", "Saturday"], default_value=0)
my_feature_columns.append(tf.feature_column.indicator_column(dayColumn))

classColumn = tf.feature_column.\
    categorical_column_with_vocabulary_list(key='Class', vocabulary_list=["Paladin","Rogue","Warrior","Mage",\
                                                                "Warlock","Shaman","Druid","Hunter"], default_value=0)
my_feature_columns.append(tf.feature_column.indicator_column(classColumn))

scoreColumn = tf.feature_column.numeric_column(key='Score')
my_feature_columns.append(scoreColumn)

classifier = tf.estimator.DNNClassifier(feature_columns=my_feature_columns, hidden_units=[10, 10], n_classes=3,
                                        model_dir='/home/chris/Desktop/TensLog/krippy')

j = 0

while j < epochs:

    classifier.train(input_fn=lambda: train_input_fn(train_X, train_Y, elementCount, batchSize), steps=trainSteps)

    eval_result = classifier.evaluate(input_fn=lambda: eval_input_fn(test_X, test_Y, batchSize))

    print('\nEpoch', (j+1), 'test set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    j += 1
