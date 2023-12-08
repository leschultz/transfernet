from transfernet import validate, train, models, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd


def main():

    # Parameters
    save_dir = './outputs'
    freeze_n_layers = 1  # Layers to freeze staring from first for transfer

    # Source training parameters
    source_n_epochs = 1000
    source_batch_size = 32
    source_lr = 0.0001
    source_patience = 200

    # Target training parameters
    target_n_epochs = 10000
    target_batch_size = 32
    target_lr = 0.0001
    target_patience = 200

    # Load data
    X_source, y_source = datasets.load('make_regression_source')
    X_target, y_target = datasets.load('make_regression_target')

    # Define architecture to use
    model = models.ExampleNet(X_source.shape[1])

    # Split source into train and validation
    splits = train_test_split(
                              X_source,
                              y_source,
                              train_size=0.8,
                              random_state=0,
                              )
    X_source_train, X_source_val, y_source_train, y_source_val = splits

    # Split target into train and validation
    splits = train_test_split(
                              X_target,
                              y_target,
                              train_size=0.8,
                              random_state=0,
                              )
    X_target_train, X_target_val, y_target_train, y_target_val = splits

    # Validate the method by having explicit validation sets
    validate.run(
                 model,
                 X_source_train,
                 y_source_train,
                 X_source_val,
                 y_source_val,
                 X_target_train,
                 y_target_train,
                 X_target_val,
                 y_target_val,
                 source_n_epochs,
                 source_batch_size,
                 source_lr,
                 source_patience,
                 target_n_epochs,
                 target_batch_size,
                 target_lr,
                 target_patience,
                 freeze_n_layers,
                 save_dir,
                 scaler=StandardScaler(),
                 )

    # Train 1 model on all data
    train.run(
              model,
              X_source,
              y_source,
              X_target,
              y_target,
              source_n_epochs,
              source_batch_size,
              source_lr,
              source_patience,
              target_n_epochs,
              target_batch_size,
              target_lr,
              target_patience,
              freeze_n_layers,
              save_dir,
              scaler=StandardScaler(),
              )


if __name__ == '__main__':
    main()
