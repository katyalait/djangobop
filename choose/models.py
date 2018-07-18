from PIL import Image
from django.shortcuts import get_object_or_404
from django.db import models
import re

class User_Image(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def pub_date(self):
        return self.date.strftime('%b %e %Y')

    def calculate_percentage(self, colours, counts):
        percentages = []
        points = 0
        size = len(counts)
        message = "Results not updated"
        for line in counts:
            #calculate the total number of points found
            points = points+line
        for line in range(len(counts)):
            #create percentage
            percent = (counts[line]/points)*100
            if percent > 0.5:
                c1 = colours[line]
                try:
                    r1 = Result.objects.get(image=self.name,colour=c1)
                except Exception as e:
                    r1 = Result(image=self.name, colour=c1, percentage=percent)
                    r1.save()
                    message = "Result table updated"
                percentages.append(percent)
        return message

    def color_table_update(self, colour_list):
        s = []
        return_list = []
        message = "Colours not updated"
        for line in colour_list:
            #extract rgb value to hex
            rgb = re.split("[ ( , ) ]", str(line))
            rgb2 = rgb[1:6]
            r = int(rgb2[0])
            g = int(rgb2[2])
            b = int(rgb2[4])
            rgb_to_hex = lambda r, g, b: '%02x%02x%02x' %(r,g,b)
            in_hex = rgb_to_hex(r, g, b)
            rgb = "(" + str(r) + "," + str(g) + "," + str(b) + ")"
            return_list.append(in_hex)
            try:
                c1 = Colour.objects.get(hex=in_hex)
            except Exception as e:
                c1 = Colour(hex=in_hex, rgb=rgb, pathogen_group="n/a")
                c1.save()
        return return_list

    def analyse(self):
        try:
            message = "Trying results"
            r1 = Result.objects.get(image=self.name)
            results = list(Results.objects.filter(image=self.name))
            return message
        except Exception as e:
            im = Image.open(self.image)
            colors = im.getcolors(256*256*256)
            raw_percents = []
            raw_colours = []
            for line in colors:
                raw_percents.append(line[0])
                raw_colours.append(line[1])
            #update colours name_table and gets list of colors in hex
            colours_list = self.color_table_update(raw_colours)
            #create percentage table
            message = self.calculate_percentage(colours_list, raw_percents)
            results = Result.objects.filter(image=self.name)
            results = list(results)
            return results


    def display_data(self):
        colour_list = self.analyse()
        return self.name

class Colour(models.Model):
    hex = models.CharField(max_length=6)
    rgb = models.CharField(max_length=15)
    pathogen_group = models.CharField(max_length=100, default="n/a")

class Result(models.Model):
    image = models.CharField(max_length=200)
    colour = models.CharField(max_length=6)
    percentage = models.FloatField()

class Counter(models.Model):
    num = models.IntegerField()
    def increment(self):
        self.num = self.num + 1
        return self.num
    def decrement(self):
        self.num = self.num -1
        return self.num
    def initialise(self):
        self.num = 0
        return ""
