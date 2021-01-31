import csv
import numpy as np
import matplotlib.pyplot as plt
import os

averageover = 300

allfilenames = []
average_x_wing_force = []
average_y_wing_force = []
max_iteration = []
total_time = []
min_quality = []
ram_used = []
total_cells = []
transcript_file = []

for f in os.listdir():
    f_name , f_ext = os.path.splitext(f)
    if (f_ext == ".csv"):
        if (f_name.split(sep="-")[3] == "report"):
            allfilenames.append(f_name)

for i in range (0,len(allfilenames)):
    file = allfilenames[i]
    file_n = "{0}{1}".format(file,".csv")
    with open(file_n) as csvfile:
        data=np.loadtxt(csvfile, delimiter=' ', skiprows=3 )
    iteration = data[-averageover:,-0]
    x_wing_force = data[-averageover:,1]
    y_wing_force = data[-averageover:,2]

    average_x_wing_force.append(x_wing_force.mean())
    average_y_wing_force.append(y_wing_force.mean())
    max_iteration.append(max(iteration))


for t in os.listdir():
    t_name , t_ext = os.path.splitext(t)
    if (t_ext == ".trn"):
        transcript_file.append(t_name)
print(transcript_file)
for i in range (0,len(transcript_file)):
    tran_file = transcript_file[i]
    tran_file_n = "{0}{1}".format(tran_file,".trn")

    with open (tran_file_n, 'r') as trans:
        lines = trans.readlines()
        for line in lines:
            if line.find("elapsed-time:") != -1:
                total_time.append(line.split()[1])

            if line.find("Minimum Orthogonal Quality") != -1:
                min_quality.append(line.split()[4])

            if line.find("Total") != -1:
                ram_used.append(line.split()[3])
                break

            if line.find(" Grid Level  0:") != -1:
                total_cells.append(line.split()[3])


with open("resultssummary.csv" , "w", newline="") as f:
    fieldnames = ["report_file", "transcript_file", "iteration", "x_force", "y_force", "min_quality", "ram_used", "total_cells"]
    # fieldnames = ["report_file", "transcript_file", "iteration", "x_force", "y_force", "min_quality", "ram_used"]
    thewriter = csv.DictWriter(f, fieldnames=fieldnames)
    thewriter.writeheader()
    for i in range(0,len(allfilenames)):
        thewriter.writerow({"report_file" : allfilenames[i], "x_force" : average_x_wing_force[i] ,"y_force" : average_y_wing_force[i], "iteration" : max_iteration[i], "transcript_file" : transcript_file[i], "min_quality" : min_quality[i], "ram_used" : ram_used[i], "total_cells" : total_cells[i] })
        # thewriter.writerow({"report_file" : allfilenames[i], "x_force" : average_x_wing_force[i] ,"y_force" : average_y_wing_force[i], "iteration" : max_iteration[i], "transcript_file" : transcript_file[i], "min_quality" : min_quality[i], "ram_used" : ram_used[i]})


#x_wing_force_plot = plt.plot(iteration,x_wing_force)
#y_wing_force_plot = plt.plot(iteration,y_wing_force)
#plt.axhline(y=y_wing_force.mean())
#plt.show()

#print("{:.1%}".format(x_wing_force.std()/x_wing_force.mean()))
#print(x_wing_force.mean())
