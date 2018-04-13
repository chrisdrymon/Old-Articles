import pandas as pd
import tensorflow as tf

CSV_COLUMN_NAMES = ['Article', 'Morph', '-2form', '-2lemma', '-2morph',	'-1form', '-1lemma', '-1morph', '1form',
                    '1lemma', '1morph', '2form', '2lemma', '2morph', '3form', '3lemma', '3morph', 'Answer']

ANSWERS = ['ellipsed', -2, -1, 1, 2, 3]


def load_data(y_name='Answer'):
    """Returns the article dataset as (train_x, train_y), (test_x, test_y)."""

    train_path = '/home/chris/Desktop/SmallMLTrain.csv'
    test_path = '/home/chris/Desktop/SmallMLTest.csv'

    train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)

    train_x, train_y = train, train.pop(y_name)

    test = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)
    test_x, test_y = test, test.pop(y_name)

    return (train_x, train_y), (test_x, test_y)


def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(3441).repeat().batch(batch_size)

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
