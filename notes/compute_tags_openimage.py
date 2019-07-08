d_names = dict()
with open("class-descriptions.csv") as f:
 for line in f:
   line = line.strip().split(",")
   d_names[line[0]] = line[1]

res = dict()
with open("train-annotations-human-imagelabels.csv") as f:
   for line in f:
     line = line.strip().split(",")
     if line[0] in res and line[3] == "1":
       res[line[0]].append(d_names[line[2]])
     elif line[3] == "1":
       res[line[0]] = [d_names[line[2]]]

with open("assos_imagestags_openimage.tsv", "w") as f:
  f.write("\n".join(["\t".join(x) for x in res.values()]))
