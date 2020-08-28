import os
import glob
import xml.etree.ElementTree as ET

foldername = os.path.basename(os.getcwd())
if foldername == "tools": os.chdir("..")


data_dir = '/labels/'
Dataset_names_path = "model_data/pascal_voc07_cls_names.txt"
# Dataset_train = "model_data/pascal_voc07_train.txt"
# Dataset_test = "model_data/pascal_voc07_test.txt"
is_subfolder = False

Dataset_names = []
      
def ParseXML(img_folder):
    for xml_file in glob.glob(img_folder+'/*.xml'):
        tree=ET.parse(open(xml_file))
        root = tree.getroot()
        image_name = root.find('filename').text

        #######
        image_size = root.find('size')
        #######
        img_path = img_folder+'/'+image_name
        with open(img_folder+'/'+image_name.strip('.jpg')+'.txt','w') as file:
	        for i, obj in enumerate(root.iter('object')):
	            difficult = obj.find('difficult').text
	            cls = obj.find('name').text
	            if cls not in Dataset_names:
	                Dataset_names.append(cls)
	            cls_id = Dataset_names.index(cls)
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
	            #img_path += ' '+OBJECT
	            #print(img_path)
	            print(image_name)
	            print(OBJECT)
	            #raise Exception
	        #print(img_path)
	        #file.write(img_path+'\n')

def run_XML_to_YOLOv3():
    for i, folder in enumerate(['train','test']):
        #with open([Dataset_train,Dataset_test][i], "w") as file:
        print(os.getcwd()+data_dir+folder)
        img_path = os.path.join(os.getcwd()+data_dir+folder) # pythonlessons/custom_data/train
        if is_subfolder:
            for directory in os.listdir(img_path):
                xml_path = os.path.join(img_path, directory) # directory == pythonlessons/custom_data/train/:
                ParseXML(xml_path) # model_data/train.txt = file 
        else:
            ParseXML(img_path)

    print("Dataset_names:", Dataset_names)
    with open(Dataset_names_path, "w") as file:
        for name in Dataset_names:
            file.write(str(name)+'\n')

run_XML_to_YOLOv3()
