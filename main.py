#!/usr/bin/env python
import argparse
from task import Task
from scheduler import Scheduler


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
    return tasks


def create_scheduler(file_name, edf, ee):
    with open(file_name, 'r') as f:
        param = f.readline().split()
        return Scheduler(*param, edf, ee)


def main():
    args = parse_cmd_args()

    file_name = args.file
    schedule_type = args.scheduler
    EE_enable = False if args.EE is '' else True

    print("Scheduling {} with {} {}".format(file_name, schedule_type, args.EE))

    sch = create_scheduler(file_name, schedule_type, EE_enable)
    tasks = create_tasks(file_name)

    total_energy = 0
    timing_diag = sch.schedule(tasks)
    if len(timing_diag) == 0:
        print('COULD NOT SCHEDULE')
    for burst in timing_diag:
        total_energy += burst[4]
        print(burst)

    print('Total energy consumed: {}'.format(total_energy))


if __name__ == '__main__':
    main()
