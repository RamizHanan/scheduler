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
    output = sch.schedule(tasks)
    if isinstance(output, list):
        print('COULD NOT SCHEDULE')
        return 0
    timing_diag = output['sch']

    print('\n{:5}    {:4}   {:4}    {:4}    {:6}'.format('start', 'task', 'hz', 'time', 'energy'))
    for burst in timing_diag:
        total_energy += burst[4]
        # (984, 'w2', '648', 17, 5.219)
        print('{:5}    {:4}   {:4}    {:4}    {:6}J'.format(*burst))

    print('\n\nTotal energy consumed: {}'.format(round(total_energy, 3)))
    print('Percent of time in IDLE: {}%'.format(output['percent']['IDLE'] * 100))
    print('Percent of time in not in IDLE: {}%'.format(output['percent']['NOT_IDLE'] * 100))
    print('Execution time: {}'.format(sch.exec_time))


if __name__ == '__main__':
    main()
