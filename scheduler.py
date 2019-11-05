import argparse
from task import Task


def parse_cmd_args():
    parser = argparse.ArgumentParser(description='Create schedule using EDF or other')
    parser.add_argument('file', type=str, nargs='?', help='File containing jobs to schedule')
    parser.add_argument('scheduler', type=str, nargs='?', help='Type of scheduler', choices=['EDF', 'edf', 'RM', 'rm'])
    parser.add_argument('EE', type=str, nargs='?', default='', choices=['EE', 'ee', ''], help='Energy Efficient')
    args = parser.parse_args()
    return args


def create_tasks(file_name):
    tasks = []
    with open(file_name, 'r') as f:
        next(f)
        for line in f:
            param = line.split()
            tasks.append(Task(*param))

    for task in tasks:
        print(task)
    return tasks


def main():
    args = parse_cmd_args()

    file_name = args.file
    schedule_type = args.scheduler
    EE_enable = False if args.EE is '' else True

    print('SCH: {}'.format(schedule_type))
    print('EE: {}'.format(EE_enable))

    tasks = create_tasks(file_name)


if __name__ == '__main__':
    main()
