#!/usr/bin/python
#  -*- coding: utf-8 -*-

from tkinter import *
from distbports import Ports

from datetime import datetime, timedelta
import timezonefinder, pytz

from dateutil.tz import gettz


class LoadingComputer:

    def __init__(self, master):

        # Style

        self.back = '#F2F1EF'

        # Initialize port distance database from JSON file located at /distances/distances_json

        path_to_distance_tables = '/Users/jordantaylor/PycharmProjects/distances/distances_json'
        self.ports = Ports(path_to_distance_tables)
        self.portscities = list(set(self.ports.cities))
        self.portlist = sorted(self.portscities)
        self.numberofports = len(self.ports.dist)
        self.listChem = self.portlist

        # Initialize main tkinter frame

        self.frame = Frame(master, borderwidth=3, padx=5, pady=5, background=self.back) #relief=RIDGE,
        self.frame.pack(fill=BOTH)
        self.entryRibbon()

        # Arguments
        self.lpname = ""
        self.dpname = ""
        self.lptable = {}
        self.distance = 0

    def entryRibbon(self):

        # ----- LAYOUT ENTRY RIBBON

        columnNames = ['CITY', 'COUNTRY', 'LATITUDE', 'LONGITUDE']
        columns =[0, 1, 2, 3]
        widths = [40, 40, 25, 25]
        self.optionList = self.listChem

        # Execute header layout

        for y in range(0,len(columnNames)):

            self.spacer = Label(self.frame, text=columnNames[y], width=widths[y], background=self.back)
            self.spacer.grid(row=1, column=columns[y])

        # Load port optionmenu

        self.v=StringVar()
        self.v.set('Load Port')
        self.productName = OptionMenu(self.frame, self.v, *self.optionList, command=self.loadport)
        self.productName.config(background=self.back, fg='white')
        self.productName.grid(row=2, column=0, sticky=E+W)

        # Discharge port optionmenu

        self.r = StringVar()
        self.r.set('Discharge Port')
        self.productName = OptionMenu(self.frame, self.r, *self.optionList, command=self.dischport)
        self.productName.config(background=self.back, fg='white')
        self.productName.grid(row=4, column=0, sticky=E+W)

        # Loadport results

        self.lpcountry = Label(self.frame, background = self.back)
        self.lpcountry.grid(row=2, column=1)

        self.lplat = Label(self.frame, background=self.back)
        self.lplat.grid(row=2, column=2)

        self.lplong = Label(self.frame, background=self.back)
        self.lplong.grid(row=2, column=3)

        # Dischport results

        self.dpcountry = Label(self.frame, background = self.back)
        self.dpcountry.grid(row=4, column=1)

        self.dplat = Label(self.frame, background=self.back)
        self.dplat.grid(row=4, column=2)

        self.dplong = Label(self.frame, background=self.back)
        self.dplong.grid(row=4, column=3)

        # Grid spacer
        self.space = Label(self.frame)
        self.space.config(background=self.back, fg='white')
        self.space.grid(row=6, column=0, sticky=E + W)

        # Distance label

        self.d = Label(self.frame, text='Distance in Nautical Miles')
        self.d.config(background=self.back)
        self.d.grid(row=8, column=0, sticky=E)

        self.dt = Label(self.frame, text='')
        self.dt.config(background=self.back)
        self.dt.grid(row=8, column=1, sticky=W)


        # Grid spacer
        self.space = Label(self.frame)
        self.space.config(background=self.back, fg='white')
        self.space.grid(row=9, column=0, sticky=E + W)

        # @ 10 KT

        self.d = Label(self.frame, text='10 Knots')
        self.d.config(background=self.back)
        self.d.grid(row=90, column=0, sticky=E)

        self.ten = Label(self.frame, text='')
        self.ten.config(background=self.back)
        self.ten.grid(row=90, column=1, sticky=W)

        # @ 12.5 KT

        self.d = Label(self.frame, text='12.5 Knots')
        self.d.config(background=self.back)
        self.d.grid(row=100, column=0, sticky=E)

        self.twelve = Label(self.frame, text='')
        self.twelve.config(background=self.back)
        self.twelve.grid(row=100, column=1, sticky=W)

        # @ 15 KT

        self.d = Label(self.frame, text='15 Knots')
        self.d.config(background=self.back)
        self.d.grid(row=110, column=0, sticky=E)

        self.fifteen = Label(self.frame, text='')
        self.fifteen.config(background=self.back)
        self.fifteen.grid(row=110, column=1, sticky=W)



        # Grid spacer
        self.space = Label(self.frame)
        self.space.config(background=self.back, fg='white')
        self.space.grid(row=200, column=0, sticky=E + W)


        # Quit

        self.quit = Button(text="Quit", anchor="s", command=self.frame.quit)
        self.quit.pack(fill='both',pady = 5)

    def calculate(self):



        self.dt.destroy()

        try:

            self.ten.destroy()
            self.twelve.destroy()
            self.fifteen.destroy()

            self.distance = self.lptable[self.dpname]
            self.dt = Label(self.frame, text=self.distance)
            self.dt.config(background=self.back)
            self.dt.grid( row=8, column=1, sticky=E+W)

            spddist = int(self.distance)

            ten = str(int(round((int(spddist / 10)/24),0) ))  + " Days    "+    str(     (int(spddist / 10)) % 24)   + " Hours "
            twel = str(int(round((int(spddist / 12.5)/24),0) ))  + " Days    "+    str(     (int(spddist / 12.5)) % 24)   + " Hours "
            fifteen = str(int(round((int(spddist / 15)/24),0) ))  + " Days    "+    str(     (int(spddist / 15)) % 24)   + " Hours "







            tdten = datetime.now() + timedelta(days=int(round((int(spddist / 10)/24),0) ))  + timedelta(hours=(int(spddist / 10)) % 24)
            tdten = tdten.strftime("%H:00 / %d %b (%A)")

            tdtwel = datetime.now() + timedelta(days=int(round((int(spddist / 12.5)/24),0) ))  + timedelta(hours=(int(spddist / 12.5)) % 24)
            tdtwel = tdtwel.strftime("%H:00 / %d %b (%A)")

            tdfift = datetime.now() + timedelta(days=int(round((int(spddist / 15)/24),0) ))  + timedelta(hours=(int(spddist / 15)) % 24)
            tdfift = tdfift.strftime("%H:00 / %d %b (%A)")

            # @ 10 KT

            self.ten = Label(self.frame, text=ten)
            self.ten.config(background=self.back)
            self.ten.grid(row=90, column=1, sticky=W+E)


            # @ 10 KT

            self.ten = Label(self.frame, text=tdten)
            self.ten.config(background=self.back)
            self.ten.grid(row=90, column=2, sticky=W)


            # @ 12.5 KT

            self.twelve = Label(self.frame, text=twel)
            self.twelve.config(background=self.back)
            self.twelve.grid(row=100, column=1, sticky=W+E)

            # @ 12.5 KT

            self.twelve = Label(self.frame, text=tdtwel)
            self.twelve.config(background=self.back)
            self.twelve.grid(row=100, column=2, sticky=W)


            # @ 15 KT

            self.fifteen = Label(self.frame, text=fifteen)
            self.fifteen.config(background=self.back)
            self.fifteen.grid(row=110, column=1, sticky=W+E)



            # @ 15 KT

            self.fifteen = Label(self.frame, text=tdfift)
            self.fifteen.config(background=self.back)
            self.fifteen.grid(row=110, column=2, sticky=W)


        except:
            pass


        pass


    def gettimezone(self, lat, long):

        from pytz import timezone
        # http://pytz.sourceforge.net/

        # https://stackoverflow.com/questions/15742045/getting-time-zone-from-lat-long-coordinates
        tf = timezonefinder.TimezoneFinder()


        tz = tf.certain_timezone_at(lat=lat, lng=long)

        tz = datetime.now(pytz.timezone(tz)).strftime('%z')

        return tz





    def loadport(self, prodName):

        self.lpname = prodName

        portgen = (x for x in range(0, self.numberofports))  # generator functiongit

        while True:
            ind = next(portgen)
            if self.ports.dist[ind]['properties']['city'] == prodName:
                outcome = self.ports.dist[ind]['properties']
                self.lptable = self.ports.dist[ind]['distances']
                break

        lat = float(outcome['latitude'])
        lat = round(lat, 1)

        long = float(outcome['longitude'])
        long = round(long, 1)

        lptz = self.gettimezone(lat, long)

        print(lptz)

        self.lpcountry.destroy()
        self.lplat.destroy()
        self.lplong.destroy()

        # Loadport results

        self.lpcountry = Label(self.frame, text=(outcome['country']), background = self.back)
        self.lpcountry.grid(row=2, column=1)

        self.lplat = Label(self.frame, text=lat, background=self.back)
        self.lplat.grid(row=2, column=2)

        self.lplong = Label(self.frame, text=long, background=self.back)
        self.lplong.grid(row=2, column=3)

        self.calculate()

    def dischport(self, prodName):

        self.dpname = prodName

        print(self.dpname)

        portgen = (x for x in range(0, self.numberofports))  # generator function

        while True:
            ind = next(portgen)
            if self.ports.dist[ind]['properties']['city'] == prodName:
                outcome = self.ports.dist[ind]['properties']
                break
        print(outcome)
        print()

        lat = float(outcome['latitude'])
        lat = round(lat, 1)

        long = float(outcome['longitude'])
        long = round(long, 1)

        self.dpcountry.destroy()
        self.dplat.destroy()
        self.dplong.destroy()

        # Dischport results

        self.dpcountry = Label(self.frame, text=(outcome['country']), background = self.back)
        self.dpcountry.grid(row=4, column=1)

        self.dplat = Label(self.frame, text=lat, background=self.back)
        self.dplat.grid(row=4, column=2)

        self.dplong = Label(self.frame, text=long, background=self.back)
        self.dplong.grid(row=4, column=3)

        self.calculate()

    def quit(self):
        main.root.quit()

def main():

    root = Tk()







    root.option_add('*font', ('Helvetica', 12))

    app = LoadingComputer(root)
    root.title("Distances Between Commercial World Ports")


    root.mainloop()

if __name__ == '__main__':
    main()


