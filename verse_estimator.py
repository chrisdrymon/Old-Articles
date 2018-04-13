"""An Example of a DNNClassifier for the Article dataset."""
import argparse
import tensorflow as tf

import verse_data


parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=93, type=int, help='batch size')
parser.add_argument('--train_steps', default=37, type=int,
                    help='number of training steps')


def main(argv):
    args = parser.parse_args(argv[1:])

    # Fetch the data
    (train_x, train_y), (test_x, test_y) = verse_data.load_data()

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in train_x.keys():
        temp_column = tf.feature_column.categorical_column_with_vocabulary_file(key=key, vocabulary_file='/home/chris/Desktop/Everythinglist.txt', default_value=0)
        my_feature_columns.append(tf.feature_column.indicator_column(temp_column))

#    train_y = tf.string_to_number(train_y)

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[50, 50],
        # The model must choose between 6 classes.
        n_classes=6)

    # Train the Model.
    classifier.train(
        input_fn=lambda:verse_data.train_input_fn(train_x, train_y,
                                                 args.batch_size),
        steps=args.train_steps)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda:verse_data.eval_input_fn(test_x, test_y,
                                                args.batch_size))

    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
