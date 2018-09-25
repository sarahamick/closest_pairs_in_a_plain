import math
import re
import sys
import os


def min_distance(nodes):
    minDistance = sys.maxsize
    closest_pair = []

    for node2 in nodes:
        for node1 in nodes:
            if node1[0] != node2[0]:
                distance = euclidean(node1, node2)
                if distance < minDistance:
                    minDistance = distance
                    closest_pair.clear()
                    closest_pair.append(node1)
                    closest_pair.append(node2)
    return closest_pair


def euclidean(node1, node2):

    x_distance = float((node1[1] - node2[1]) ** 2)
    y_distance = float((node1[2] - node2[2]) ** 2)
    distance = float(math.sqrt(x_distance + y_distance))
    return distance


def closest_pair_non_recursive(list_of_nodes):

    Px = sorted(list_of_nodes, key=lambda x: x[1])

    i = 0
    while i < len(Px):
        Px[i][3] = i
        i=i+1

    Py = sorted(Px, key=lambda y: y[2])

    i = 0
    while i < len(Py):
        Py[i][4] = i
        i = i+1

    Px2 = sorted(Py, key=lambda x: x[1])

    pair = (closest_pair_recursive(Px2, Py))
    if pair[0][0] != pair[1][0]:
        return euclidean(pair[0], pair[1])


def closest_pair_recursive(px, py):
    if len(px) <= 3:  # euclidean distance it
        return min_distance(px)

    qy = []
    ry = []

    qx = px[:math.ceil(len(px)/2)]
    rx = px[math.ceil(len(px)/2):]

    cutoff = qx[-1][3]

    for i in range(len(py)):
        if py[i][3] <= cutoff:
            qy.append(py[i])
        else:
            ry.append(py[i])

    pair_q = closest_pair_recursive(qx, qy)
    pair_r = closest_pair_recursive(rx, ry)

    # ---------------

    if pair_r[0][0] !=  pair_r[1][0] and pair_q[0][0] != pair_q[1][0]:
        pair_r_dist = euclidean(pair_r[0], pair_r[1])
        pair_q_dist = euclidean(pair_q[0], pair_q[1])

    delta = min(pair_r_dist, pair_q_dist)

    l_or_x_star = qx[-1][1]

    sy = []
    for node in py:
        if abs(node[1] - l_or_x_star) < delta:
            sy.append(node)

    counter = 0
    minum_distance = sys.maxsize
    min_pair = []
    for node in sy:
        i = 0
        while i <= 14 and (counter+i) < len(sy):
            if(node[0] != sy[counter+i][0]):
                distance = euclidean(node, sy[counter+i])
                if distance < minum_distance:
                    minum_distance = distance
                    min_pair.clear()
                    min_pair.append(node)
                    min_pair.append(sy[counter+i])
            i = i+1
        counter = counter+1

    if minum_distance < delta:
        return min_pair
    elif pair_q_dist < pair_r_dist:
        return pair_q
    else:
        return pair_r


def check_accuracy(file1, file2):

    print()
    print("Checking accuracy of output compared to expected output...")
    print()

    expected_output = dict()
    actual_output = dict()
    list_of_files = []
    with open(file1) as f1:
        for line in f1:
            fileline = line.split(" ")
            if not list_of_files.__contains__(fileline[0]):
                list_of_files.append(fileline[0])
            expected_output[fileline[0]] = [fileline[1], fileline[2]]

    with open(file2) as f2:
        for line in f2:
            fileline = line.split(" ")
            if not list_of_files.__contains__(fileline[0]):
                list_of_files.append(fileline[0])
                actual_output[fileline[0]] = [fileline[1], fileline[2]]

    for fi in list_of_files:
        default_list = ["-1", "-1"]
        expected_output.setdefault(fi, default_list)
        actual_output.setdefault(fi, default_list)

    numWrong = 0
    for name in list_of_files:

        if actual_output[name] != ["-1", "-1"]:
            expected_distance = float(expected_output[name][1][:-1])
            actual_distance = float(actual_output[name][1][:-1])
            if abs(expected_distance - actual_distance) > 1:
                numWrong = numWrong + 1
                print()
                print("File", name, "has a difference of", (expected_distance - actual_distance), "between expected and actual output")
                print("Expected:", expected_output[name])
                print("Actual:", actual_output[name])

    if numWrong == 0:
        print("Output matches expected output on all", len(list_of_files), "files")


def read_in():

    path = 'data'
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            filenames.append(filename)

    filenames.sort()

    for filename in filenames:
        list_of_nodes = []

        wholename = "data/" + filename
        with open(wholename) as f:

            regex = re.compile(r"(\s*(\S+)\s+(\S+)\s+(\S+))")
            wordreg = re.compile(r"([a-zA-Z]+)")

            if re.search(wordreg, f.readline()) is not None:
                found_node = False
                while not found_node:
                    if f.readline().startswith("NODE"):
                        found_node = True

            for line in f:
                if regex.search(line) is not None:
                    name = re.search(regex, line).group(2)
                    xcor = float(re.search(regex, line).group(3))
                    ycor = float(re.search(regex, line).group(4))

                    node = [name, xcor, ycor, -1, -1]
                    list_of_nodes.append(node)

        edited_filenamea = filename[:-4]
        edited_filename_list = list(edited_filenamea)
        edited_filename_list[-4] = "."
        edited_filename = "".join(edited_filename_list)

        print("../data/", edited_filename, ": ", len(list_of_nodes), " ", closest_pair_non_recursive(list_of_nodes), sep='')


read_in()
check_accuracy("data/output/expected_out.txt", "data/output/actual_out.txt")
