res_dir = "results/PasteFromConsole"

def FilesInDir(dirPath):
    from os import listdir
    from os.path import isfile, join
    files = [f for f in listdir(dirPath) if isfile(join(dirPath,f))]
    return files

results = FilesInDir(res_dir)

for con_file_res in results:
    raw_dat = [i.replace("\n","") for i in open(res_dir + "/" + con_file_res,"r").readlines()]
    data = [i.split(" ") for i in raw_dat]

    fin_data = []
    for i in data:
        print(i)
        if len(i) > 5:
            if i[1] == "Accuracy:":
                print("included")
                fin_data.append(float(i[3]))
    
    split = []
    for i in range(0,len(fin_data),50):
        temp = fin_data[int(i):int(i+50)]
        split.append(temp)
    #print(data)
    fin_data = []
    for i in range(0,len(split),10):
        temp = split[int(i):int(i+10)]
        fin_data.append(temp)
    
    labels = []
    for i in raw_dat:
        if i.find(" - Finished: ") > -1:
            labels.append(i[int(len(" - Finished: ")):])
    
    myfile = open("results/" + con_file_res.replace(".txt","") + "_results.txt","w")
    data_index = 0
    print(len(fin_data))
    for i in range(len(labels)):
        temp = []
        print(data_index, len(fin_data))
        las_data = fin_data[data_index]
        if labels[i].find("Seperated starting player Convolutional") > -1 or labels[i].find("Seperated by result Convolutional") > -1:
            t1 = fin_data[data_index]
            t2 = fin_data[data_index+1]
            print(len(t1[9]))
            data_index = data_index+1
            las_data = []
            for index in range(len(t1)):
                las_data.append((t1[index],t2[index]))
        myfile.write(labels[i])
        myfile.write("\n")
        myfile.write(str(las_data))
        myfile.write("\n")

        data_index += 1
        if data_index == len(fin_data):
            break
    #print(labels, len(fin_data))
    #break