import argparse


def main():


    parser = argparse.ArgumentParser(description="Basic geo-files image processing tool")

    parser.add_argument("option", type=str, help="Choose option: [crop, ]")
