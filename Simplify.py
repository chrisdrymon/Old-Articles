"""An Example of a DNNClassifier for the Article dataset."""
import tensorflow as tf
import pandas as pd


def load_data(y_name='Answer'):
    """Returns the article dataset as (train_x, train_y), (test_x, test_y)."""

    train_path = '/home/chris/Desktop/SmallMLTrain.csv'
    test_path = '/home/chris/Desktop/SmallMLTest.csv'

    train = pd.read_csv(train_path)

    train_x, train_y = train, train.pop(y_name)

    test = pd.read_csv(test_path)
    test_x, test_y = test, test.pop(y_name)

    return (train_x, train_y), (test_x, test_y)


def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(5000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset


def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features=dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset


tf.logging.set_verbosity(tf.logging.INFO)
batchSize = 100
trainSteps = 300

# Fetch the data
(train_X, train_Y), (test_X, test_Y) = load_data()

# Categorical Columns wrapped in Indicator Columns
my_feature_columns = []
for key in train_X.keys():
    temp_column = tf.feature_column.\
        categorical_column_with_vocabulary_file(key=key, vocabulary_file='/home/chris/Desktop/Everythinglist.txt',
                                                default_value=0)
    my_feature_columns.append(tf.feature_column.indicator_column(temp_column))

classifier = tf.estimator.DNNClassifier(feature_columns=my_feature_columns,
                                        hidden_units=[200, 50, 50], n_classes=6, model_dir='/home/chris/Desktop/logger')

# Train the Model.
classifier.train(
    input_fn=lambda:train_input_fn(train_X, train_Y, batchSize),
    steps=trainSteps)

# Evaluate the model.
eval_result = classifier.evaluate(
    input_fn=lambda:eval_input_fn(test_X, test_Y, batchSize))

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))
