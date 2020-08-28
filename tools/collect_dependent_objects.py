'''
This file will seperate the dataset of particular objects and 
the indexing of the objects will start from the previous class.
N.B: This file will also not take objects from the picture that 
has previous class.
'''

import glob 
import os 
import xml.etree.ElementTree as ET 
import shutil 

objects_wanted = ['car']
objects_prev = ['person']


destination_folder = './dataset_car_wrt_person2'
target_folder = '.'

if os.path.exists(destination_folder):
	shutil.rmtree(destination_folder)

os.mkdir(destination_folder)
os.mkdir(destination_folder+os.sep+'train')
os.mkdir(destination_folder+os.sep+'test')

total_objects  =  objects_prev + objects_wanted


def ParseXML(train_test):
	for xml_file in glob.glob(target_folder+os.sep+train_test+"/*.xml"):
		tree = ET.parse(open(xml_file))
		root = tree.getroot()
		image_name = root.find('filename').text

		desired_object_present = False

		for i, obj in enumerate(root.iter('object')):
			object_name = obj.find('name').text
			if object_name in objects_wanted:
				desired_object_present = True 

		objects_prev_present = False

		for obj in root.iter('object'):
			object_name = obj.find('name').text
			if object_name in objects_prev:
				objects_prev_present = True 


		if desired_object_present and not objects_prev_present:
			shutil.copy(target_folder+os.sep+train_test+os.sep+image_name, destination_folder+os.sep+train_test+os.sep+ image_name)
			with open(destination_folder+os.sep+train_test+os.sep+ image_name.strip('.jpg')+'.txt','w') as file:
				for i, obj in enumerate(root.iter('object')):
					object_name = obj.find('name').text
					if object_name in objects_wanted:
						cls_id = total_objects.index(object_name)
						xmlbox = obj.find('bndbox')
						xmin = float(xmlbox.find('xmin').text)/float(root.find('size').find('width').text)
						ymin = float(xmlbox.find('ymin').text)/float(root.find('size').find('height').text)
						xmax = float(xmlbox.find('xmax').text)/float(root.find('size').find('width').text)
						ymax = float(xmlbox.find('ymax').text)/float(root.find('size').find('height').text)
						x_center = (xmax - xmin)/2.0 + xmin
						y_center = (ymax - ymin)/2.0 + ymin
						width = xmax - xmin
						height = ymax - ymin
						OBJECT = (str(cls_id)+' ' +str(x_center)+' '
								  +str(y_center)+' '
								  +str(width)+' '
								  +str(height)
								  )
						file.write(OBJECT+'\n')

			file.close()





for train_test in ['train','test']:
	ParseXML(train_test)
