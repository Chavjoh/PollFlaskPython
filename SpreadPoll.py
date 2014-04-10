#!/usr/bin/python
# coding: utf-8

import sys
from flask import Flask, render_template, request, redirect, url_for
import gspread
from GoogleAccount import google_user, google_pass

# Create the flask app
app = Flask(__name__)

@app.route('/')
def poll_list():
	worksheets_list = spreadsheet.worksheets()
	return render_template('home.html', polls=worksheets_list)

@app.route('/<poll_slug>', methods=['GET'])
def display_poll(poll_slug):
	try:
		poll = spreadsheet.worksheet(poll_slug)
	except gspread.exceptions.WorksheetNotFound:
		return "Sorry, no poll at that url", 404

	options = poll.row_values(1)
	title = options.pop(0)

	return render_template('poll.html', **locals())

@app.route('/<poll_slug>', methods=['POST'])
def vote(poll_slug):
	try:
		poll = spreadsheet.worksheet(poll_slug)
	except gspread.exceptions.WorksheetNotFound:
		return "Sorry, no poll at that url", 404

	voter = request.form['who']

	nb_voters = len(poll.col_values(1))

	poll.update_cell(nb_voters+1, 1, voter)

	return redirect(url_for('display_poll', poll_slug=poll_slug))

if __name__ == '__main__':
	# Connect to google docs and find the spreadsheet named "Polls"
	try:
		gc = gspread.login(google_user, google_pass)
	except gspread.exceptions.AuthenticationError:
		print("Cannot log in")
		sys.exit(1)

	try:
		spreadsheet = gc.open("Polls")
	except gspread.exceptions.SpreadsheetNotFound:
		print("Cannot find spreadsheet")
		sys.exit(1)
	
	app.run(debug=True) # TODO: Disable debug mode in production
	