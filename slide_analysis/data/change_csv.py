import csv

oldname = "/home/awu/ML/Praxis-III/slide_analysis/data/train/train_df_old.csv"
newname = "/home/awu/ML/Praxis-III/slide_analysis/data/train/train_df.csv"

with open(oldname, 'r') as file:
    file.readline()
    lines = csv.reader(file)
    line_list = []
    file_list = []
    for line in lines:
        new = line[0].replace('.','',2).replace("\\", "/")
        line_list.append([new, line[1], line[2], line[3], line[4], line[5]])
    for row in line_list:
        file_list.append(['/home/awu/ML/Praxis-III/slide_analysis' + row[0], row[1], row[2], row[3], row[4], row[5]])

with open(newname, 'w') as file:
    writer = csv.writer(file, lineterminator = '\n')
    for row in file_list:
        writer.writerow(row)
        
with open(newname, "r+") as file:
     existing=file.read()
     file.seek(0)
     file.write("path,category,x1,x2,y1,y2\n"+existing)

