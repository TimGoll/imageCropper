from PIL import Image
import os, json, time, threading, Queue

class FileReader:
	def __init__(self):
		self.sourcefolders = []
		self.filelist = []
		self.settings = []
		self.imageAmount = 0
	
	### DIRERCTORY PARSER ###
	def get_sourcefolders(self, basefolder):
		dir_year = os.listdir(basefolder)
		
		for year in dir_year:
			dir_month = os.listdir(basefolder + '\\' + year)
			
			for month in dir_month:
				self.sourcefolders.append(year + '\\' + month)
				
	def get_filelist(self, basefolder, subfolder):
		self.filelist.append([])
		
		for root, dirs, files in os.walk(basefolder + '\\' + subfolder, topdown=False):
			for name in files:
				self.filelist[len(self.filelist) -1].append(name)
				self.imageAmount += 1
				
		self.filelist[len(self.filelist) -1] = sorted(self.filelist[len(self.filelist) -1])
				
	def compute_base_directory(self):
		self.get_sourcefolders(self.settings['source_path'])
		
		for name in self.sourcefolders:
			flr.get_filelist(self.settings['source_path'], name)
			
		print("")
		print("Gefundene Verzeichnisse:")
		for dir in self.sourcefolders:
			print(' - ' + self.settings['source_path'] + '\\' + dir)
		print("")
		print("Gefundene Bilder: " + str(self.imageAmount))
		print("")
		print("Tippe 'start' um zu beginnen, 'exit' um das Programm zu beenden.")
		print("")
			
	

	### CONFIG READER ###
	def read_jsonToArray(self, path):
		with open(path, 'r') as file:
			return json.load(file)
		
	def write_arrayToJson(self, path, newData):
		with open(path, 'w') as file:
			json.dump(newData, file)


	### MAIN ###
	def start(self):
		self.settings = self.read_jsonToArray('config\config.json')
		
		print("")
		print("+--------------------------+")
		print("|       IMAGE-SCRIPT       |")
		print("+--------------------------+")
		print("")
		
		print("Aktuelle Einstellungen:")
		print(" - Offset: \t\tx " + str(self.settings['offset']['x']) + ", \ty " + str(self.settings['offset']['y']))
		print(" - Quellgroesse: \tx " + str(self.settings['source_size']['x']) + ", \ty " + str(self.settings['source_size']['y']))
		print(" - Zielgroesse: \tx " + str(self.settings['dest_size']['x']) + ", \ty " + str(self.settings['dest_size']['y']))
		print(" - Quellverzeichnis: \t" + self.settings['source_path'] + '\\')
		print(" - Zielverzeichnis: \t" + self.settings['dest_path'] + '\\')
		
	def work(self):
		index_array = self.read_jsonToArray('config\lastnum.json')
	
		box = [
			self.settings['offset']['x'],
			self.settings['offset']['y'],
			self.settings['offset']['x'] + self.settings['source_size']['x'],
			self.settings['offset']['y'] + self.settings['source_size']['y']
		]
		
		size = [
			self.settings['dest_size']['x'],
			self.settings['dest_size']['y']
		]
		
		print("")
	
		processing_image_index = 1
		for index, file_array in enumerate(self.filelist):
			sourcefolders_split = self.sourcefolders[index].split('\\')
			
			year  = sourcefolders_split[0]
			month = sourcefolders_split[1]
			
			if (not str(year) in index_array): #fuege fehlendes Jahr hinzu
				index_array.update({str(year):{}})
				
			if (not str(month) in index_array[str(year)]):
				index_array[str(year)].update({str(month):0})

			for file in file_array:
				path = self.settings['source_path'] + '\\' + self.sourcefolders[index] + '\\' + file
				print("Verarbeite Bild " + '{:03d}'.format(processing_image_index) + "  ---  " + path)
			
				image = Image.open(path)
				image = image.crop(box)
				image = image.resize(size)
				
				number = '{:03d}'.format(index_array[str(year)][str(month)])
				name   = self.settings['dest_path'] + '\\' + self.settings['prefix'] + '_' + year + '_' + month + '-' + number + '.jpg'
				image.save(name)
				
				index_array[str(year)][str(month)] += 1
				processing_image_index += 1
		
		self.write_arrayToJson('config\lastnum.json', index_array)
		
		print("")
		print("Bildverarbeitung abgeschlossen.")
		print("")
		rdl.readLineQueue.put("exit")

class Readline (threading.Thread):
    readLineQueue = Queue.Queue()

    def run (self):
        while (True):
            newinput = raw_input()
            self.readLineQueue.put(newinput)
			
flr = FileReader()
rdl = Readline()
try:
	# INIT
	flr.start()
	flr.compute_base_directory()
	
	# START READLINE THREAD (ConsoleInputs)
	rdl.setDaemon(True) #Daemon - thread stops after exiting main-thread
	rdl.start()
	
	while(True):
		# READLINE: ConsoleInputs
		if (rdl.readLineQueue.qsize() > 0):
			data = rdl.readLineQueue.get()
			rdl.readLineQueue.task_done()
			
			if (data.lower() == "exit"):
				break
			elif (data.lower() == "start"):
				flr.work()
			
			
		time.sleep(0.01)
	
	#flr.print_()	
	
except KeyboardInterrupt:
	print ("Programm beendet")