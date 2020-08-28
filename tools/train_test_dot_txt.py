import os 
import glob

foldername =os.path.basename(os.getcwd())
print(foldername)

if foldername == "tools":
	os.chdir("..")
print(os.getcwd())

data_dir = '../dataset_only_car_wrt_person/images/' # change this directory wrt to dataset directory
dataset_name = 'pascalvoc_car_only' # change this name to give a new one.


for folder in ['train', 'test']:
	with open('./data/'+folder+dataset_name+'.txt', 'w') as file:
		for image in os.listdir(data_dir+folder+os.sep):
			image_path = data_dir+folder + os.sep + image
			file.write(image_path+'\n')
	file.close()
