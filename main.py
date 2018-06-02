#!/usr/bin/python
#  -*- coding: utf-8 -*-



# Offline calculation of distances between ports and estimated time of arrival.


from tkinter import *
from distbports import Ports

from datetime import datetime, timedelta
import timezonefinder, pytz

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
        self._dpzd = 0


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
        columnNames = ['CITY', 'COUNTRY', 'LATITUDE', 'LONGITUDE', 'ZONE DESCRIPTION']
        columns =[0, 1, 2, 3,4]
        widths = [40, 40, 25, 25, 25]
        self.optionList = self.listChem

        # Execute header layout column names HEADER
        for y in range(0,len(columnNames)):
            self.spacer = Label(self.frame, text=columnNames[y], width=widths[y], background=self.back)
            self.spacer.grid(row=1, column=columns[y])

        # Load port optionmenu HEADER
        self.v=StringVar()
        self.v.set('Load Port')
        self.productName = OptionMenu(self.frame, self.v, *self.optionList, command=self.loadport)
        self.productName.config(background=self.back, fg='white')
        self.productName.grid(row=2, column=0, sticky=E+W)

        # Discharge port optionmenu HEADER
        self.r = StringVar()
        self.r.set('Discharge Port')
        self.productName = OptionMenu(self.frame, self.r, *self.optionList, command=self.dischport)
        self.productName.config(background=self.back, fg='white')
        self.productName.grid(row=4, column=0, sticky=E+W)

        # Loadport label results HEADER
        self.lpcountry = Label(self.frame, background = self.back); self.lpcountry.grid(row=2, column=1)
        self.lplat = Label(self.frame, background=self.back); self.lplat.grid(row=2, column=2)
        self.lplong = Label(self.frame, background=self.back); self.lplong.grid(row=2, column=3)
        self.lpzd = Label(self.frame, background=self.back); self.lpzd.grid(row=2, column=4)

        # Dischport label results HEADER
        self.dpcountry = Label(self.frame, background = self.back); self.dpcountry.grid(row=4, column=1)
        self.dplat = Label(self.frame, background=self.back); self.dplat.grid(row=4, column=2)
        self.dplong = Label(self.frame, background=self.back); self.dplong.grid(row=4, column=3)
        self.dpzd = Label(self.frame, background=self.back); self.dpzd.grid(row=4, column=4)

        # Grid spacer
        self.space = Label(self.frame); self.space.config(background=self.back, fg='white'); self.space.grid(row=6, column=0, sticky=E + W)

        # Distance label: 'Distance in Nautical Miles' and distance number i.e. 6530
        self.dnm = Label(self.frame, text='Distance in Nautical Miles')
        self.dnm.config(background=self.back)
        self.dnm.grid(row=8, column=0, sticky=E)

        self.dt = Label(self.frame, text='')
        self.dt.config(background=self.back)
        self.dt.grid(row=8, column=1, sticky=W)

        # Grid spacer
        self.space = Label(self.frame); self.space.config(background=self.back, fg='white'); self.space.grid(row=9, column=0, sticky=E + W)

        # @ 10 KT
        self.d = Label(self.frame, text='10 Knots')
        self.d.config(background=self.back)
        self.d.grid(row=90, column=0, sticky=E)

        self.ten = Label(self.frame, text='')
        self.ten.config(background=self.back)
        self.ten.grid(row=90, column=4, sticky=W)

        # @ 12.5 KT
        self.d = Label(self.frame, text='12.5 Knots')
        self.d.config(background=self.back)
        self.d.grid(row=100, column=0, sticky=E)

        self.twelve = Label(self.frame, text='')
        self.twelve.config(background=self.back)
        self.twelve.grid(row=100, column=4, sticky=W)

        # @ 15 KT
        self.d = Label(self.frame, text='15 Knots')
        self.d.config(background=self.back)
        self.d.grid(row=110, column=0, sticky=E)

        self.fifteen = Label(self.frame, text='')
        self.fifteen.config(background=self.back)
        self.fifteen.grid(row=110, column=4, sticky=W)

        # Grid spacer
        self.space = Label(self.frame)
        self.space.config(background=self.back, fg='white')
        self.space.grid(row=200, column=0, sticky=E + W)





        self.footer = Frame()
        self.footer.pack(fill=BOTH)


        # Execute header layout column names HEADER
        for y in range(0,len(columnNames)):
            self.spacer = Label(self.footer, width=widths[y])
            self.spacer.grid(row=0, column=columns[y])

        self.spacer = Label(self.footer, text="KNOTS",pady="5")
        self.spacer.grid(row=0, column=0)

        self.spacer = Label(self.footer, text="OFFSET, HOURS (not required)",pady="5")
        self.spacer.grid(row=0, column=1)


        # ETA ENTRY
        self.vknot = StringVar()
        self.ent = Entry(self.footer,textvariable=self.vknot)
        self.ent.config()
        self.ent.grid(row=20, column=0, sticky=E + W)


        # ETA ENTRY
        self.offset = StringVar()

        self.off = Entry(self.footer,textvariable=self.offset)
        self.off.config()
        self.off.grid(row=20, column=1, sticky=E + W)

        # ETA BUTTON
        self.knot = Button(self.footer, command=self.calccustometa)
        self.knot.config(text="Calculate ETA", bg=self.back)
        self.knot.grid(row=20, column=2, sticky=E + W)


        # ETA LABEL
        self.custeta = Label(self.footer)
        self.custeta.config()
        self.custeta.grid(row=20, column=4, sticky=E + W)




        self.spacer = Label()
        self.spacer.pack(fill='both')


        self.fr = Frame(background=self.back)
        self.fr.pack(fill=BOTH)

        #
        #
        #
        # # Quit
        # self.quit = Label(self.fr)
        # self.quit.config(background=self.back)
        # self.quit.pack(fill='both')

        # Quit
        self.quit = Label(self.fr,text="2018 jordantaylor.io")
        self.quit.config(background=self.back,foreground="#696969")
        self.quit.pack(anchor="e",padx ="10")

        # Quit
        self.quit = Button(self.fr,text="Quit", anchor="s",command=self.frame.quit)
        self.quit.config()
        self.quit.pack(fill='both')






    def calccustometa(self):

        try:
            self.custeta.destroy()
            spddist = int(self.distance)
            t = float(self.vknot.get())

            try:
                of = float(self.offset.get())
                print(of)
            except:
                of = 0

            tdfift = datetime.utcnow() + timedelta(days=((float(spddist / t) / 24)) + (self._dpzd / 24) + (of/24))
            tdfift = tdfift.strftime("%H:00 / %d %b LT")

            # Grid spacer
            self.custeta = Label(self.footer, text = tdfift)
            self.custeta.config()

            self.custeta.grid(row=20, column=4, sticky=E + W)



        except:
            self.custeta = Label(self.footer, text = "")
            self.custeta.config()

            self.custeta.grid(row=20, column=4, sticky=E + W)

    def calculate(self):
        self.dt.destroy()
        try:
            self.custeta.destroy()
        except:
            pass
        try:

            self.ten.destroy()
            self.twelve.destroy()
            self.fifteen.destroy()
            self.distance = self.lptable[self.dpname]
            self.dt = Label(self.frame, text=self.distance)
            self.dt.config(background=self.back)
            self.dt.grid( row=8, column=1, sticky=E+W)

            spddist = int(self.distance)

            ten = str(int(round((int(spddist / 10)/24),0) ))  + " Days "+    str(     (int(spddist / 10)) % 24)   + " Hours "
            twel = str(int(round((int(spddist / 12.5)/24),0) ))  + " Days "+    str(     (int(spddist / 12.5)) % 24)   + " Hours "
            fifteen = str(int(round((int(spddist / 15)/24),0) ))  + " Days "+    str(     (int(spddist / 15)) % 24)   + " Hours "

            tdten = datetime.utcnow()+ timedelta(days=((float(spddist / 10.0)/24))+(self._dpzd/24))
            tdten = tdten.strftime("%H:00 / %d %b LT")

            tdtwel = datetime.utcnow()+ timedelta(days=((float(spddist / 12.5)/24))+(self._dpzd/24))
            tdtwel = tdtwel.strftime("%H:00 / %d %b LT")

            tdfift = datetime.utcnow()+ timedelta(days=((float(spddist / 15)/24))+(self._dpzd/24))
            tdfift = tdfift.strftime("%H:00 / %d %b LT")

            # @ 10 KT
            self.ten = Label(self.frame, text=ten)
            self.ten.config(background=self.back)
            self.ten.grid(row=90, column=1, sticky=W+E)

            # @ 10 KT
            self.ten = Label(self.frame, text=tdten)
            self.ten.config(background=self.back)
            self.ten.grid(row=90, column=4, sticky=W+E)

            # @ 12.5 KT
            self.twelve = Label(self.frame, text=twel)
            self.twelve.config(background=self.back)
            self.twelve.grid(row=100, column=1, sticky=W+E)

            # @ 12.5 KT
            self.twelve = Label(self.frame, text=tdtwel)
            self.twelve.config(background=self.back)
            self.twelve.grid(row=100, column=4, sticky=W+E)

            # @ 15 KT
            self.fifteen = Label(self.frame, text=fifteen)
            self.fifteen.config(background=self.back)
            self.fifteen.grid(row=110, column=1, sticky=W+E)

            # @ 15 KT

            self.fifteen = Label(self.frame, text=tdfift)
            self.fifteen.config(background=self.back)
            self.fifteen.grid(row=110, column=4, sticky=W+E)

        except:
            pass
        pass

    def loadport(self, prodName):

        def gettimezone(lat, long):

            tf = timezonefinder.TimezoneFinder()
            tz = tf.certain_timezone_at(lat=lat, lng=long)
            tz = datetime.now(pytz.timezone(tz)).strftime('%z')

            return tz

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

        lptz = gettimezone(lat, long)

        try:
            lptz = gettimezone(lat, long)
        except:
            lptz = 'NaN'

        self.lpcountry.destroy()
        self.lplat.destroy()
        self.lplong.destroy()
        self.lpzd.destroy()

        # Loadport results

        self.lpcountry = Label(self.frame, text=(outcome['country']), background = self.back)
        self.lpcountry.grid(row=2, column=1)

        self.lplat = Label(self.frame, text=lat, background=self.back)
        self.lplat.grid(row=2, column=2)

        self.lplong = Label(self.frame, text=long, background=self.back)
        self.lplong.grid(row=2, column=3)

        self.lpzd = Label(self.frame, text=lptz, background=self.back)
        self.lpzd.grid(row=2, column=4)

        self.calculate()

    def dischport(self, prodName):

        def gettimezone(lat, long):



            tf = timezonefinder.TimezoneFinder()
            tz = tf.certain_timezone_at(lat=lat, lng=long)

            utc_offset_time = datetime.now(pytz.timezone(tz))

            return utc_offset_time

        self.dpname = prodName

        portgen = (x for x in range(0, self.numberofports))  # generator function

        while True:
            ind = next(portgen)
            if self.ports.dist[ind]['properties']['city'] == prodName:
                outcome = self.ports.dist[ind]['properties']
                break

        lat = float(outcome['latitude'])
        lat = round(lat, 1)

        long = float(outcome['longitude'])
        long = round(long, 1)

        try:
            dptz = gettimezone(lat, long)

            dptz = dptz.strftime('%z') # get just zone description
            sign = dptz[:1]
            intn = int(dptz[1:3])
            if sign == '-': intn = -intn
            else: pass


            self._dpzd = intn

        except:
            dptz = 'NaN'

        self.dpcountry.destroy()
        self.dplat.destroy()
        self.dplong.destroy()
        self.dpzd.destroy()

        # Dischport results

        self.dpcountry = Label(self.frame, text=(outcome['country']), background = self.back)
        self.dpcountry.grid(row=4, column=1)

        self.dplat = Label(self.frame, text=lat, background=self.back)
        self.dplat.grid(row=4, column=2)

        self.dplong = Label(self.frame, text=long, background=self.back)
        self.dplong.grid(row=4, column=3)

        self.lpzd = Label(self.frame, text=dptz, background=self.back)
        self.lpzd.grid(row=4, column=4)

        self.calculate()

    def quit(self):
        main.root.quit()

def main():

    root = Tk()

    # def hello():
    #     pass
    #
    # menubar = Menu(root)
    # helpmenu = Menu(menubar, tearoff=0)
    # helpmenu.add_command(label="About", command=hello)
    # menubar.add_cascade(label="About", menu=helpmenu)


    # root.config(menu=menubar)









    root.option_add('*font', ('Helvetica', 12))
    app = LoadingComputer(root)


    root.title("Distances and Estimated Time of Arrival Between Commercial World Ports")










    root.mainloop()

if __name__ == '__main__':
    main()


