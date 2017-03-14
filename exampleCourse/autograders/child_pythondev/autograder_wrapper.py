# An example wrapper script that takes existing autograder output
# and converts it to a format readable by the grading machine

# this wrapper is run as the ag user by autograder.sh

import autograder as ag
import os
import json


def main(job_id):
    # Call the autograder, we expect it to write to results.txt
    output = ag.main()
    print(output)


    # Start generating the grading results json
    grading_result = {'job_id': job_id}

    grading_result['output'] = output
    lines = output.split("\n")

    earned_points = 0
    total_points = 0

    if len(lines) > 1 and (len(lines)) % 4 == 0:
        # Tests ran successfully
        grading_result['testedCompleted'] = 'true'
        tests = []

        # Traverse through all the lines, storing the results
        # Autograder's test output are in the format: name, points scored, max points, message
        line_num = 0
        for i in range(0, int(len(lines) / 4)):
            test = {}
            test['name'] = lines[line_num].rstrip('\n')
            test['id'] = i
            print(lines[line_num+1].rstrip('\n'))
            test['point'] = lines[line_num + 1].rstrip('\n')
            earned_points += int(lines[line_num + 1].rstrip('\n'))
            test['maxPoints'] = lines[line_num + 2].rstrip('\n')
            total_points += int(lines[line_num + 2].rstrip('\n'))
            test['output'] = lines[line_num + 3].rstrip('\n')
            test['message'] = ''
            line_num += 4
            tests.append(test)

        # Add the tests to the grading result
        grading_result['tests'] = tests

        print("earned_points: ", earned_points);
        print("total_points: ", total_points);
        grading_result['score'] = float(earned_points) / float(total_points)

    elif len(lines) == 1:
        # Compiler error in autograder
        grading_result['testedCompleted'] = 'false'

    else:
        # No tests ran or something bad happened
        grading_result['testedCompleted'] = 'false'

    # Remove the results file
    # os.remove('results.txt')

    # Write the grading results to stdout
    print(json.dumps(grading_result))
if __name__ == '__main__':
    # Pass in a dummy job id
    main(49)
