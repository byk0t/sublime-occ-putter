import os
import sublime
import sublime_plugin
import subprocess


def occ_put_settings(view=sublime.active_window().active_view()):
	"""Get settings from the sublime project file"""
	project_data = view.window().project_data()

	# Not all windows have project data
	if project_data == None:
		return None

	settings = project_data.get('settings', {}).get("occ_put")
	settings["project_folder"] = project_data.get("folders")[0]["path"]

	return settings


class OccPutCommand(sublime_plugin.EventListener):

	def on_post_save(self, view):
		
		# Get settings
		settings = occ_put_settings(view)

		# Don't do anything if there is no configuration
		if not settings:
			return
		# Don't do anything if there put_on_save is False
		elif settings.get("put_on_save", True) == False:
			return
		
		# for example "widget/Add Product To Wish List/instances/Add Product To Wish List Widget/display.template"
		file_name = view.file_name().replace(settings.get("project_folder") + "/", "")
		
		cmd = ['dcu', 
			'--put', file_name, 
			'--node', settings.get("node"), 
			'--username', settings.get("user"), 
			'--password', settings.get("password")]		
		
		sublime.status_message(file_name + " - started")
		output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, cwd=settings.get("project_folder"))
		sublime.status_message(file_name + " - done with a result: " + str(output))


class OccPutInitSettingsCommand(sublime_plugin.TextCommand):
	"""Sublime Command for creating the occPut block in the project settings file"""

	def run(self, edit, **args): 
		"""Generate settings for occPut"""
		# Load project configuration
		project_data = self.view.window().project_data()

		if project_data == None:
			print("Unable to initialize settings, you must have a .sublime-project file.")
			print("Please use 'Project -> Save Project As...' first.")
			self.view.window().run_command("show_panel", {"panel": "console", "toggle": False})
			return

		# Create configuration if it doesn't exists
		if not project_data.get('settings', {}).get("occ_put"):
			if not project_data.get('settings'):
				project_data['settings'] = {}
			project_data['settings']["occ_put"] = {}
			project_data['settings']["occ_put"]["put_on_save"] = True
			project_data['settings']["occ_put"]["node"] = ""
			project_data['settings']["occ_put"]["user"] = ""
			project_data['settings']["occ_put"]["password"] = ""            
			
			if project_data.get("folders") == None:
				print("Unable to initialize settings, you must have at least one folder in your .sublime-project file.")
				print("Please use 'Add Folder to Project...' first.")
				self.view.window().run_command("show_panel", {"panel": "console", "toggle": False})
				return

			for folder in project_data.get("folders"):
				# Handle folder named '.'
				# User has added project file inside project folder, so we use the directory from the project file
				path = folder.get("path")
				if path == ".":
					path = os.path.basename(os.path.dirname(self.view.window().project_file_name()))                

			# Save configuration
			self.view.window().set_project_data(project_data)		
		else:
			print("occPut configuration already exists.")

		# Open configuration in new tab
		self.view.window().run_command("open_file", {"file": "${project}"})	
