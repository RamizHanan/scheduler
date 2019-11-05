import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Create schedule using EDF or other')
    parser.add_argument('file', type=str, nargs='?', help='File containing jobs to schedule')
    parser.add_argument('scheduler', type=str, nargs='?', help='Type of scheduler', choices=['EDF', 'edf', 'RM', 'rm'])
    parser.add_argument('EE', type=str, nargs='?', default='', choices=['EE', 'ee', ''], help='Energy Efficient')
    args = parser.parse_args()

    file_name = args.file
    schedule_type = args.scheduler
    EE_enable = False if args.EE is '' else True

    file = open(file_name, 'r')
    print(file.read())
    print('SCH: {}'.format(schedule_type))
    print('EE: {}'.format(EE_enable))


if __name__ == '__main__':
    main()
