import argparse
from train import main_train
from classify import main_classify

parser = argparse.ArgumentParser(description='Run the program')
parser.add_argument('mode', metavar='mode', type=str,
                    help="Specify 'train' or 'classify' to classify or train the model")
args = parser.parse_args()

if args.mode.upper() == "TRAIN":
    main_train()

else if args.mode.upper() == "CLASSIFY":
    main_classify()

else:
    print("Please enter 'train' or 'mode'")
