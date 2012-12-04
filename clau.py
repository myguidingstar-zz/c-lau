#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk, os, gtk, unicodedata, re
pygtk.require('2.0')

def normalizeDiacritics(source, diacriticsPosClassicOn=True):
    TONE = '(['+u'\u0300'+u'\u0309'+u'\u0303'+u'\u0301'+u'\u0323'+'])'
    result = unicodedata.normalize('NFD',source.replace(u'\u0110', u'\u00D0').replace(u'\u0111', u'\u00F0'))
    result = re.sub('(?i)' + TONE + '([aeiouy' + u'\u0306'+u'\u0302'+u'\u031B]'+'+)', "\\2\\1", result)
    result = re.sub('(?i)(?<=['+u'\u0306'+u'\u0302'+u'\u031B'+'])(.)' + TONE + '\\B', "\\2\\1", result)
    result = re.sub('(?i)(?<=[ae])([iouy])' + TONE, "\\2\\1", result)
    result = re.sub('(?i)(?<=[oy])([iuy])' + TONE, "\\2\\1", result)
    result = re.sub('(?i)(?<!q)(u)([aeiou])' + TONE, "\\1\\3\\2", result)
    result = re.sub('(?i)(?<!g)(i)([aeiouy])' + TONE, "\\1\\3\\2", result)
    if diacriticsPosClassicOn:
        result = re.sub('(?i)(?<!q)([ou])([aeoy])' + TONE + '(?!\\w)', "\\1\\3\\2", result)
    return unicodedata.normalize('NFC',result).replace(u'\u00D0', u'\u0110').replace(u'\u00F0', u'\u0111');

def normalizeClipboard():
  clipboard = gtk.clipboard_get()
  text = clipboard.wait_for_text()
  if isinstance(text, str) or isinstance(text, unicode):
    clipboard.set_text(normalizeDiacritics(text))
    clipboard.store()

class SystrayIconApp:
	def __init__(self):
		self.tray = gtk.StatusIcon()
		self.tray.set_from_stock(gtk.STOCK_CONVERT)
		self.tray.connect('popup-menu', self.on_right_click)
		self.tray.set_tooltip(('C-lau tray app'))

    	def on_right_click(self, icon, event_button, event_time):
		self.make_menu(event_button, event_time)

    	def make_menu(self, event_button, event_time):
		menu = gtk.Menu()

		# show about dialog
		about = gtk.MenuItem("About")
		about.show()
		menu.append(about)
		about.connect('activate', self.show_about_dialog)

		# show normalize dialog
		normalize = gtk.MenuItem("Normalize diacritics")
		normalize.show()
		menu.append(normalize)
		normalize.connect('activate', self.show_normalize_dialog)

		# add quit item
		quit = gtk.MenuItem("Quit")
		quit.show()
		menu.append(quit)
		quit.connect('activate', gtk.main_quit)

		menu.popup(None, None, gtk.status_icon_position_menu,
		           event_button, event_time, self.tray)

	def  show_about_dialog(self, widget):
		about_dialog = gtk.AboutDialog()
		about_dialog.set_destroy_with_parent (True)
		about_dialog.set_icon_name ("C-lau")
		about_dialog.set_name('C-lau')
		about_dialog.set_version('0.1')
		about_dialog.set_copyright("(C) 2012 Hoang Minh Thang")
		about_dialog.set_comments('C-lau (spelled `cờ lau` - which may remind you of Đinh Bộ Lĩnh) is A Linux tray app that helps normalize Vietnamese diacritics from clipboard.')
		about_dialog.set_authors(['Hoang Minh Thang <p@banphim.net>'])
		about_dialog.run()
		about_dialog.destroy()

	def  show_normalize_dialog(self, widget):
		normalizeClipboard()

if __name__ == "__main__":
	SystrayIconApp()
	gtk.main()



