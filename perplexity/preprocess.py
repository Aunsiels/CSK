import os.path

if os.path.isfile("sentences_ppl.tsv"):
    sentences = set()
    with open("sentences_ppl.tsv") as f:
        for line in f:
            sentences.add(line.strip().split("\t")[0])
    to_process = []
    with open("sentences.txt") as f:
        for line in f:
            line = line.strip()
            if line not in sentences:
                to_process.append(line)
    with open("sentences_to_process.txt", "w") as f:
        f.write("\n".join(to_process) + "\n")
