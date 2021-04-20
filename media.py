from shutil import move
import os
import config as cfg


def rename(filename_old, filename_new):
	filename = filename_new.split(".")
	filename_new = f"{filename[0].strip()}.{filename[1]}"
	os.rename(filename_old, filename_new)
	return f"RENAME: {filename_old} -> {filename_new}"

def needs_formating(filename):
	for quality in cfg.video_quality:
		if (
			"-" in filename
			or "_" in filename
			and str(quality) in filename
		): return True
	return False


class Media:
	def __init__(self, path):
		self.path = path

	def move(self, filename=None, show_title=None):
		os.chdir(f"X:/PLEX/TEMP/{self.path}")
		target_dir = f"../../{self.path}"
		if show_title:
			show_title, season = show_title
			try: os.mkdir(f"X:/PLEX/{self.path}/{show_title}")
			except OSError: pass
			try: os.mkdir(f"X:/PLEX/TV SHOWS/{show_title}/Season {season}")
			except OSError: pass
		if filename:
			files = [filename]
		else:
			files = os.listdir()
		for file in files:
			move(file, f"{target_dir}/{file}")

	def rename(self, filename):
		try:
			name = filename.replace("-", " ")
			names = filename.split("-")
			if "season" in names and "episode" in names and "_" in filename:
				self.path = "TV SHOWS"
				season = name.split("season")[1].strip().split()[0]
				season = season if len(season) >= 2 else "0" + season
				episode = name.split("episode")[1].strip().split()[0]
				show_title = name.split("season")[0].strip()
				episode_title = name.split("episode")[1].replace(episode, "").strip().split("_")[0]
				filename = f"{show_title} - S{season}E{episode} - {episode_title}"
			elif needs_formating(filename):
				self.path = "MOVIES"
				for quality in cfg.video_quality:
					filename = filename            \
						.replace(str(quality), "") \
						.replace("-", " ")         \
						.replace("_", "")          \
						.split(".")[0]             \
						.strip()
			return filename + ".mp4"
		except IndexError:
			pass
		return False
