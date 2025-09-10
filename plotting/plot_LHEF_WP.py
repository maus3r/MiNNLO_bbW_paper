#!/Usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import os
import shutil
import glob
import copy
import math
import subprocess
import textwrap
import time
from os.path import join as pjoin
if not __name__ == "__main__":
    from initialize_classes import out

if __name__ == "__main__":
  def is_number(s):
      try:
          float(s)
          return True
      except ValueError:
          return False
  def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
#{{{ class: bcolors
  class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#}}}
#{{{ class: print_output()
  class print_output():
#{{{ def: __init__(self)
    def __init__(self):
        global wrapper
        wrapper = textwrap.TextWrapper()
        wrapper.width = 80
#}}}
#{{{ def: print_error_no_stop(self,string)
    def print_error_no_stop(self,string):
        wrapper.initial_indent    = "<<MATRIX-ERROR>> "
        wrapper.subsequent_indent = "                 "
        try:
            print bcolors.FAIL + "%s" % "\n".join(wrapper.wrap(string)) + bcolors.ENDC
        except:
            print "%s" % "\n".join(wrapper.wrap(string))
            pass
#}}}
#{{{ def: print_error(self,string)
    def print_error(self,string):
        wrapper.initial_indent    = "<<MATRIX-ERROR>> "
        wrapper.subsequent_indent = "                 "
        try:
            print bcolors.FAIL + "%s" % "\n".join(wrapper.wrap(string)) + bcolors.ENDC
        except:
            print "%s" % "\n".join(wrapper.wrap(string))
            pass
        sys.exit(1)
#}}}
#{{{ def: print_warning(self,string)
    def print_warning(self,string):
        wrapper.initial_indent    = "<<MATRIX-WARN>> "
        wrapper.subsequent_indent = "                "
        try:
            print bcolors.WARNING + "%s" % "\n".join(wrapper.wrap(string)) + bcolors.ENDC
        except:
            print "%s" % "\n".join(wrapper.wrap(string))
            pass
#}}}
#{{{ def: print_info(self,string)
    def print_info(self,string):
        wrapper.initial_indent    = "<<MATRIX-INFO>> "
        wrapper.subsequent_indent = "                "
        try:
            print bcolors.OKGREEN + "%s" % "\n".join(wrapper.wrap(string)) + bcolors.ENDC
        except:
            print "%s" % "\n".join(wrapper.wrap(string))
            pass
#}}}
#{{{ def: print_jobs(self,string)
    def print_jobs(self,string):
        wrapper.width = 200
        wrapper.initial_indent    = "<<MATRIX-JOBS>> "
        wrapper.subsequent_indent = "                "
        print "%s" % "\n".join(wrapper.wrap(string))
        wrapper.width = 80
#}}}
#{{{ def: print_result(self,string)
    def print_result(self,string):
        wrapper.width = 200
        wrapper.initial_indent    = "<MATRIX-RESULT> "
        wrapper.subsequent_indent = "                "
        print "%s" % "\n".join(wrapper.wrap(string))
        wrapper.width = 80
#}}}
#{{{ def: print_read(self,string)
    def print_read(self,string):
        wrapper.initial_indent    = "<<MATRIX-READ>> "
        wrapper.subsequent_indent = "                "
        print "%s" % "\n".join(wrapper.wrap(string))
#}}}
#{{{ def: print_list(self,list_path,output_type="default")
    def print_list(self,list_path,output_type="default"):
        # define color of output
        color_end = bcolors.ENDC
        if output_type == "error":
            color_start = bcolors.FAIL
        elif output_type == "warning":
            color_start = bcolors.WARNING
        elif output_type == "info":
            color_start = bcolors.OKGREEN
        elif output_type == "default":
            color_start = ""
            color_end = ""
        else:
            self.print_error("Given output_type %s in function print_list not known." % output_type)

        with open(list_path,'r') as list_file:
            for entry in list_file:
                print color_start + "|============>> " + entry.strip() + color_end
#}}}
#}}}

#{{{ class: gnuplot
class gnuplot():
    """Class to automatically create nice gnuplot files and plot the MATRIX distributions"""
#{{{ def: __init__(self,result_folder_path_in)
    def __init__(self,result_folder_path_in):
        self.curve_list = [] # initialize an empty curve list
        self.orig_curve_dict = {} # keep original curves as dictinary of new curves giving old curves, needed for normalization
        self.curve_properties = {} # and an empty dictionary for the properties of these curves (linestyle, coloer, ...)
        self.plot_properties = {} # and another empty dictionary for the properties of the plot (xmin, xmax,...)
        self.result_folder_path  = result_folder_path_in # use pwd in stand alone mode
        self.gnuplot_folder_name = "gnuplot_LHEF"
        self.gnuplot_folder_path = pjoin(self.result_folder_path,self.gnuplot_folder_name)
        self.define_all_label_mappings()
        self.binwidth = 0
        # special cases:
        # self.njets_plot = False # in this plot we combine n_jets and total_rate
        try:
            os.makedirs(self.gnuplot_folder_path)
        except:
            pass
#}}}
#{{{ def: add_curve(self,path,properties = {})
    def add_curve(self,path,properties = {}):
        # function to add a curve (data file under path) to the list of curves, where you can give properties 
        # which is a dictionary that contains, eg, {'color': red/RGB, 'format': histogram, 'linewidth': 1, 'linestyle': 1,'label', 'uncertainties': True ... more?}
        # if you give no properties, the default properties (line styles) are used
        # default for uncertainties is Trues; this assumes a file with $1: x-value, $2: central, $3: err_central, $4/$6: up/down or down/up, $5/$7: their errors
        if not os.path.isfile(path): # maybe loosen this later and only skip the plot
            out.print_error("Trying to add a curve under path \"%s\" that does not exist. Exiting..." % path)
        if self.plot_properties:
            out.print_error("Trying to add curve, but plot properties already set. You have to first add all curves, and then you can specify the plot properties.")
        self.curve_list.append(path)
        # check first wether the property input is valid
        self.check_curve_properties(properties)
        self.curve_properties[path] = properties
#}}}
#{{{ def: check_curve_properties(self,properties)
    def check_curve_properties(self,properties):
        # function to check wether the given curve properties are valid
        # properties can be either a dictionary of dictionaries of all curves, or a dictionary for one curve
        allowed_properties = {}
        allowed_properties["line_style"]  = [] 
        allowed_properties["color"]  = [] #["red","blue","green","black"] # too many possibilities also RGB colors allowed...
        allowed_properties["format"] = ["lines","histogram","sigma_per_bin","data"]
        allowed_properties["normalization_constant"] = []
        allowed_properties["label"]  = [] # if empty everything is allowed (specify later)
        allowed_properties["exclude_from_ratio"]  = [True,False] # if empty everything is allowed (specify later)
        allowed_properties["exclude_from_main"]  = [True,False] # if empty everything is allowed (specify later)
        allowed_properties["uncertainties"]  = [True,False] # if empty everything is allowed (specify later)
        allowed_properties["show_uncertainties"]  = [True,False] # if empty everything is allowed (specify later)
        for item0 in properties:
            if isinstance(item0, dict):
                for item in item0:
                    if not item in allowed_properties:
                        out.print_error("Item %s has no entry in the dictionary of allowed_properties of a curve." % item)
                    elif allowed_properties[item] and not properties[item] in allowed_properties[item]:
                        out.print_error("Property %s of a curve for item %s is not in the list of allowed_properties for that item." % (properties[item], item))
            else:
                item = item0
                if not item in allowed_properties:
                    out.print_error("Item %s has no entry in the dictionary of allowed_properties of a curve." % item)
                elif allowed_properties[item] and not properties[item] in allowed_properties[item]:
                    out.print_error("Property %s of a curve for item %s is not in the list of allowed_properties for that item." % (properties[item], item))
#}}}
#{{{ def: get_name(self,curve_list)
    def get_name(self,curve_list = {}):
        # function that determines a name for the plot (from the names of the files of each curve) and returns it
        # first get the names from the curve_list which contains the full paths
        if "name" in self.plot_properties: # in case name is set manually use that and return
            return self.plot_properties["name"]
        
        if not curve_list:
            curve_list = self.curve_list
        name_list = []
        for curve in curve_list:
            name_list.append(curve.rsplit('/',1)[1])
        name = os.path.commonprefix(name_list)
        try:
            name = name.rsplit("__")[0]
        except:
            pass
        
        if len(name) < 2 or os.path.exists(pjoin(self.gnuplot_folder_path,name+".gnu")):
            name = '+'.join(name_list)
        return name
#}}}
#{{{ def: clean_gnuplot_folder(self)
    def clean_gnuplot_folder(self):
        # function that removes everything in the gnuplot folder
        try:
            shutil.rmtree(self.gnuplot_folder_path)
        except:
            pass        
        try:
            os.makedirs(self.gnuplot_folder_path)
        except:
            pass        
#}}}
#{{{ def: convert_to_histogram(self,path)
    def convert_to_histogram(self,path, normalization_constant = 1, rebin = 1,convert_to_sigma_per_bin = False):
        # converts a normal (space-separated) data file into a histrogram:  0  XXX         0  XXX
        #                                                                   5  YYY         5  XXX
        #                                                                  10  ZZZ   ==>   5  YYY
        #                                                                  15  ...        10  YYY
        #                                                                  ..             10  ZZZ
        # the assumption is that the histograms always start at the lower bound; 2do: add bin correction
        min_x_for_rebin = self.plot_properties.get("min_x_for_rebin","")
        rebin_above_x = self.plot_properties.get("rebin_above_x","")
        # special case: for njets plots we must add the total rate between x-values of -1 and 0
        add_total_rate = None
        if path.rsplit('/',1)[1].startswith("n_jets"):
            # get the corresponding total rate
            total_path = pjoin(path.rsplit('/',1)[0],path.rsplit('/',1)[1].replace("n_jets","total_rate"))
            with open(total_path, 'r') as f:
                for line in f:
                    if line.strip()[0]=="" or line.strip()[0]=="%" or line.strip()[0]=="#": 
                        continue
                    add_total_rate = line.split(None,1)[1].strip()
        # first try to create a histgram folder inside the gnuplot folder, where all the histograms can be
        try:
            os.makedirs(pjoin(self.gnuplot_folder_path,"histograms"))
        except:
            pass
        # then do the conversion to a histgram file
        histogram_file_name = path.rsplit('/',1)[1].replace(".dat",".hist")
        previous_y_values = None # initialize since start of first bin does not need to be repeated
        filelength = file_len(path)/rebin
#        print filelength, path
        with open(pjoin(self.gnuplot_folder_path,"histograms",histogram_file_name),'w') as hist_file:
          with open(pjoin(self.gnuplot_folder_path,"histograms",histogram_file_name.replace(".hist","_yerror.hist")),'w') as hist_file_yerr:
            with open(path, 'r') as orig_file:
                if add_total_rate: # add total rate at the very beginning of njets plot
                    hist_file.write("-1  "+add_total_rate+"\n")
                    hist_file.write("0  "+add_total_rate+"\n")
                    hist_file_yerr.write("-1  "+add_total_rate+"\n")
                    hist_file_yerr.write("0  "+add_total_rate+"\n")
                count_since_rebin = 0
                saved_y_values_array = []
                counter = 1
                firsttime = True
                for line in orig_file:
                    counter += 1
                    line = line.strip() # strip removes all spaces (including tabs and newlines)
                    # if any line starts with %, # or is an emtpy line (disregarding spaces) it is a comment line and should be skipped
                    if line=="" or line[0]=="%" or line[0]=="#": 
#                        hist_file.write(line+"\n")
                        continue
                    count_since_rebin += 1
                    x_value  = line.split(None,1)[0].strip()
                    if rebin_above_x and (float(x_value) >= float(min_x_for_rebin)):
                        rebin = rebin_above_x
                    y_values_array = line.split(None,1)[1].strip().split()
                    y_values = ""
                    if count_since_rebin == 1:
                        saved_x_value = x_value
                    if count_since_rebin < rebin:
                        saved_y_values_array.append(y_values_array)
                        continue
                    else:
                        for array in saved_y_values_array:
                            for index, value in enumerate(array):
                                if index % 2 == 0:
                                    y_values_array[index] = str(float(y_values_array[index])+float(value))
                                else:
#                                    y_values_array[index] = str(float(y_values_array[index])+float(value))
                                    y_values_array[index] = str(((float(y_values_array[index]))**2+float(value)**2)**(1/2.))
                        if not convert_to_sigma_per_bin:
                            for index, value in enumerate(y_values_array):
                                y_values_array[index] = str(float(y_values_array[index])/rebin) # for histograms need to devide out rebinning
#                        x_value_for_next = copy.copy(x_value)
                        x_value = saved_x_value
                        count_since_rebin = 0
                        saved_y_values_array = []
                    next_x_value_set = False
                    for value in y_values_array:
                        if convert_to_sigma_per_bin:
                            # get the next x-value
                            nextone = False
                            with open(path, 'r') as orig_file2:
                              for line2 in orig_file2:
                                line2 = line2.strip() # strip removes all spaces (including tabs and newlines)
                                # if any line starts with %, # or is an emtpy line (disregarding spaces) it is a comment line and should be skipped
                                if line2=="" or line2[0]=="%" or line2[0]=="#": 
                                    continue
                                x_value2  = line2.split(None,1)[0].strip()
                                if nextone:
                                    next_x_value = x_value2
                                    next_x_value_set = True
                                    break
                                elif float(x_value2) == float(x_value):
                                    nextone = True
                            if next_x_value_set:
                                y_values = y_values + "  " + str(float(value)*(float(next_x_value) - float(x_value)) * normalization_constant)
                            else:
                                y_values = previous_y_values
                            binwidth2 = (float(next_x_value)-float(x_value))#*rebin
                            if counter == filelength/2:
                                self.binwidth = (float(next_x_value)-float(x_value))#*rebin
 #                               print "yeeees",self.binwidth
 #                               print self.binwidth
                        else:
                            y_values = y_values + "  " + str(float(value) * normalization_constant)
                            binwidth2 = 0.
                    if previous_y_values: hist_file.write(x_value+"  "+previous_y_values+"\n")
                    if previous_y_values and next_x_value_set:
                        hist_file_yerr.write(str(float(x_value)+binwidth2/2)+"  "+previous_y_values+"\n")
                    hist_file.write(x_value+"  "+y_values+"\n")
                    if firsttime and "dy.WpWm__" in histogram_file_name:
                        hist_file_yerr.write(str(-5.4)+"  "+y_values+"\n")
                        firsttime = False
                    elif firsttime and "pT.Wm__" in histogram_file_name:
                        hist_file_yerr.write(str(13.4)+"  "+y_values+"\n")
                        firsttime = False
                    elif firsttime and "y.WW__" in histogram_file_name:
                        hist_file_yerr.write(str(-3.75)+"  "+y_values+"\n")
                        firsttime = False
                    else:
                        hist_file_yerr.write(str(float(x_value)+binwidth2/2)+"  "+y_values+"\n")
                    previous_y_values = y_values
                if self.binwidth == 0: self.binwidth = binwidth2
                # print "---------------------------------"
                # print path
                # print self.binwidth
                if "dy.WpWm__" in histogram_file_name:
                    hist_file_yerr.write(str(5.4)+"  "+y_values+"\n")
                    hist_file_yerr.write(str(5.4)+"  "+y_values+"\n")
                elif "pT.Wm__" in histogram_file_name:
                    hist_file_yerr.write(str(2100)+"  "+y_values+"\n")
                    hist_file_yerr.write(str(2100)+"  "+y_values+"\n")
                elif "y.WW__" in histogram_file_name:
                    hist_file_yerr.write(str(3.75)+"  "+y_values+"\n")
                    hist_file_yerr.write(str(3.75)+"  "+y_values+"\n")
                if count_since_rebin > 0:
                    if previous_y_values: hist_file.write(x_value+"  "+previous_y_values+"\n")
                    if previous_y_values: hist_file_yerr.write(str(float(x_value)+binwidth2/2)+"  "+previous_y_values+"\n")
        if path in self.curve_list: # if the original file was already added to the curve_list
            # remove the original file in the curve_list and add the new histogram file
            self.curve_list.remove(path)
            self.curve_list.append(pjoin(self.gnuplot_folder_path,"histograms",histogram_file_name))
            # and replace its properties
            self.curve_properties[pjoin(self.gnuplot_folder_path,"histograms",histogram_file_name)] = self.curve_properties.pop(path)
            # keep original curves as dictinary of new curves giving old curves, needed for normalization
            self.orig_curve_dict[pjoin(self.gnuplot_folder_path,"histograms",histogram_file_name)] = path
#}}}
#{{{ def: run_gnuplot(self,gnu_file)
    def run_gnuplot(self,gnu_file):
        # function to execute gnuplot with gnu_file as first argument
        out.print_info("Running gnuplot...")
        gnuplot = subprocess.Popen(["gnuplot",gnu_file])#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#}}}
#{{{ def: plot(self)
    def plot(self,curve_list = [],curve_properties = {},plot_properties = {}):
        # function to start the final plotting
        # you can give the curve_list and its properties also altogether via their arguments here. THE ORDERING OF BOTH IS IMPORTANT!
        if curve_list: # if not empty
            self.curve_list = curve_list # overwrite the curve list belonging to the class
            self.check_curve_properties(curve_properties)   # check input for all curves
            for curve in curve_list:
#                self.check_curve_properties(curve_properties.get(curve,{}))   # check input for each curve
                self.curve_properties[curve] = curve_properties.get(curve,{}) # and its properties (second argument is the default, which is an empty list)
        if plot_properties: # if not empty
            self.check_plot_properties(plot_properties)
            self.plot_properties = plot_properties
        # first do some checks:
        if not self.curve_list:
            out.print_error_no_stop("Trying to plot data, but curve_list is empty.")
            return
        self.check_concistency_of_curve_properties(self.curve_properties)
        # other checks?

        # first determine name of the plot (because of njet/total rate special case)
        self.plot_name = self.get_name(self.curve_list)
        out.print_info("Trying to plot: %s" %self.plot_name)
        gnu_file = pjoin(self.gnuplot_folder_path,self.plot_name+".gnu")
        # then convert all histogram curves (note currently only supported that none or all are histograms; catched in check_concistency_of_curve_properties)
        tmp_curve_list = []
        for item in self.curve_list:
            tmp_curve_list.append(item) # make a copy to be able to change the orignal list while looping over
            # if self.plot_name == "n_jets": # for n_jet plots
            #     self.njets_plot = True
            #     tmp_curve_list.append(item.replace("n_jets","total_rate")) # add also total rate
            #     self.curve_properties[item.replace("n_jets","total_rate")] = {} # and add empty properties
        for curve in tmp_curve_list:
            if not "format" in self.curve_properties[curve] or self.curve_properties[curve]["format"] == "histogram": # histograms is default, so do the conversion also if no format is given
                self.convert_to_histogram(curve,self.curve_properties[curve].get("normalization_constant",1.),self.plot_properties.get("rebin",1))
            elif self.curve_properties[curve]["format"] == "sigma_per_bin":
                self.convert_to_histogram(curve,self.curve_properties[curve].get("normalization_constant",1.),self.plot_properties.get("rebin",1),True)
            elif self.curve_properties[curve]["format"] == "data" or self.curve_properties[curve]["format"] == "lines":
                # make sure the position in the curve list stays the same
                self.curve_list.remove(curve)
                self.curve_list.append(curve)
            else:
                out.print_error("Curve \"format\" not recognized.")
        # check if the values in the files are all zeros (stop the plotting if that is the case)
        if not self.get_axis_properties():
            out.print_error_no_stop("The plots appear to be all empty (or contain only zeros and nans). Skipping this plot...")
        else:
            # create gnuplot file
            self.create_gnu_file(gnu_file)
            # execute gnuplot for gnu_file
            self.run_gnuplot(gnu_file)
            out.print_info("Plot successfully generated.")
#}}}
#{{{ def: check_concistency_of_curve_properties(self,curve_properties)
    def check_concistency_of_curve_properties(self,curve_properties):
        # function to check wether the properties of the different curves are consistent with each other
        pass
        # should work now for data
        # 1. check: we can only plot curves of the same format into the same plot
        # curve_format = ""
        # for curve, properties in curve_properties.iteritems():
        #     if curve_format and not curve_format == properties.get("format",""):
        #         out.print_error("Currently, one can combine only curves of the same format into the same plot, but trying to combine format \"%s\" and format \"%s\"" % (curve_format,properties.get("format")))
        #     else:
        #         curve_format = properties.get("format","")
#}}}
#{{{ def: set_plot_properties(self,properties,value = None)
    def set_plot_properties(self,properties,value = None):
        # function to set plot properties; with one argument you directly give the full list under properties (and overwrite any given plot properties before)
        # with two arguments you can set a single property to the given value (Note: the value must be different from None!)
        self.check_plot_properties(properties,value)
        if value is None and isinstance(properties, dict):
            self.plot_properties[properties] = value
        else:
            self.plot_properties[properties] = value
#}}}
#{{{ def: check_plot_properties(self,properties,value = None)
    def check_plot_properties(self,properties,value = None):
        # function to check wether the given plot properties are valid
        # properties can be either a dictionary of all properties, or a single property of a plot
        allowed_properties = {}
        allowed_properties["name"]  = [] # set name of plot, otherwise automatically determined
        allowed_properties["rebin"]  = [] # if empty everything is allowed (specify types later)
        allowed_properties["rebin_above_x"]  = [] # if empty everything is allowed (specify types later)
        allowed_properties["min_x_for_rebin"]  = [] # if empty everything is allowed (specify types later)
        allowed_properties["xmin"]  = [] # if empty everything is allowed (specify types later)
        allowed_properties["xmax"]  = []
        allowed_properties["ymin"]  = []
        allowed_properties["ymax"]  = []
        allowed_properties["ymin_ratio"] = []
        allowed_properties["ymax_ratio"] = []
        allowed_properties["title"]    = []
        allowed_properties["process"]  = []
        allowed_properties["collider"] = []
        allowed_properties["energy"]   = []
        allowed_properties["normalization"] = [x for x in range(1,len(self.curve_list)+1)]
        allowed_properties["logscale_y"] = [True,False]
        allowed_properties["logscale_x"] = [True,False]
        allowed_properties["logscale_y_ratio"] = [True,False]
        allowed_properties["logscale_x_ratio"] = [True,False]
        allowed_properties["xlabel"] = []
        allowed_properties["xunit"]  = []
        allowed_properties["ylabel"] = []
        allowed_properties["yunit"]  = []
        allowed_properties["reference"] = []
        allowed_properties["version"]   = []
        allowed_properties["category"]  = []
        allowed_properties["categoryleft"]  = []
        allowed_properties["xtics"]  = []
        allowed_properties["mxtics"] = []
        allowed_properties["xtics_ratio"]  = []
        allowed_properties["xtics_add"]  = []
        allowed_properties["mxtics_ratio"] = []
        allowed_properties["ytics_ratio"]  = []
        allowed_properties["mytics_ratio"] = []
        allowed_properties["ytic_offset_x"]  = []
        allowed_properties["ytic_offset_y"] = []
        allowed_properties["xtic_offset_x"]  = []
        allowed_properties["xtic_offset_y"] = []
        allowed_properties["mytics"] = []
        allowed_properties["norm_label"] = []
        allowed_properties["exclude_from_ratio"] = [] # must be a list
        allowed_properties["exclude_from_main"] = [] # must be a list
        allowed_properties["legend"] = ["left","right","down","down down","down left","down center"] # must be a list
        allowed_properties["legend_ratio"] = ["left","right","down","down left"] # must be a list
        if value is None and isinstance(properties, dict): # dictionary of properties
            for item in properties:
                if not item in allowed_properties:
                    out.print_error("Item \"%s\" has no entry in the dictionary of allowed_properties of the plot." % item)
                elif allowed_properties[item] and not properties[item] in allowed_properties[item]:
                    out.print_error("Property \"%s\" of the plot for item \"%s\" is not in the list of allowed_properties for that item." % (properties[item], item))
        else: # single property
            if not properties in allowed_properties:
                out.print_error("Item \"%s\" has no entry in the dictionary of allowed_properties of the plot." % properties)
            elif allowed_properties[properties] and not value in allowed_properties[properties]:
                out.print_error("Property \"%s\" of the plot for item \"%s\" is not in the list of allowed_properties for that item." % (value, properties))
#}}}
#{{{ def: create_gnu_file(self,gnu_file)
    def create_gnu_file(self,gnu_file):
        # function to create the whole gnuplot file; this will be quite long and tricky
        # so it will be splitted in many steps
        with open(gnu_file, "w") as out_file:
            out_file.write(self.get_gnuplot_default_general()) # writes out the default general part
            out_file.write(self.get_gnuplot_settings_general()) # writes out the default general part
            out_file.write(self.get_gnuplot_default_main_frame()) # writes out the default general part
            out_file.write(self.get_gnuplot_settings_main_frame()) # writes out the default general part
            out_file.write(self.get_gnuplot_plot_main_frame()) # writes out the default general part
            out_file.write(self.get_gnuplot_default_ratio()) # writes out the default general part
            out_file.write(self.get_gnuplot_settings_ratio()) # writes out the default general part
            out_file.write(self.get_gnuplot_plot_ratio()) # writes out the default general part
#}}}
#{{{ def: get_gnuplot_default_general(self)
    def get_gnuplot_default_general(self):
        # function that returns the default general part to create the gnuplot file
        default_general = """
reset
set terminal pdfcairo enhanced dashed dl 1.5 lw 3 font \"Helvetica,30\" size 7.6, 8
set encoding utf8

## default key features
#set key at graph 1.03,0.97
set key reverse  # put text on right side
set key Left     # left bounded text
set key spacing 1.1
set key samplen 2
## to have a assisting grid of dashed lines
set grid front
## set margins
set lmargin 5
set rmargin 2
"""
        return default_general
#}}}
#{{{ def: get_gnuplot_settings_general(self)
    def get_gnuplot_settings_general(self):
        # function that returns the user-definable settings made in the general part to create the gnuplot file
        # create a parameter_list dictionary so that it is more obvious which values are set in the string created below
        parameter_list = {}
        # set all parameters that you can modify below, so that they can be passed to the string
        parameter_list["pdf_file"] = pjoin(self.gnuplot_folder_path,self.plot_name+".pdf") # path of the output pdf file
        parameter_list["MATRIX_reference"] = self.plot_properties.get("reference","XXXX.XXXXX") # set it to something meaningful later
# not used    parameter_list["MATRIX_version"] = self.plot_properties.get("version","0.0.1alpha") # set it to something meaningful later
        if self.plot_properties.get("legend","right") == "right":
            parameter_list["key_x"]  = 0.99 # x-position of key 
            parameter_list["key_y"]  = 0.95 # y-position of key 
        elif self.plot_properties.get("legend","right") == "left":
            parameter_list["key_x"]  = 0.50 # x-position of key 
            parameter_list["key_y"]  = 0.95 # y-position of key 
        elif self.plot_properties.get("legend","right") == "down":
            parameter_list["key_x"]  = 0.73 # x-position of key 
            parameter_list["key_y"]  = 0.25 # y-position of key 
        elif self.plot_properties.get("legend","right") == "down center":
            parameter_list["key_x"]  = 0.7 # x-position of key 
            parameter_list["key_y"]  = 0.32 # y-position of key 
        elif self.plot_properties.get("legend","right") == "down down":
            parameter_list["key_x"]  = 0.55 # x-position of key 
            parameter_list["key_y"]  = 0.25 # y-position of key 
        elif self.plot_properties.get("legend","right") == "down left":
            parameter_list["key_x"]  = 0.55 # x-position of key 
            parameter_list["key_y"]  = 0.45 # y-position of key 
        if is_number(self.get_axis_properties()["xtics"]): # only set it if a number is given
            parameter_list["xtics"]  = self.get_axis_properties()["xtics"]  # distance between big x-tics 
        else: # otherwise set it empty, as it will create bin labels below the main plot
            parameter_list["xtics"]  = ""
        parameter_list["xtics_add"] = re.sub(r'\".*?\"', '\"\"', self.plot_properties.get("xtics_add",""))
        parameter_list["mxtics"] = self.get_axis_properties()["mxtics"] # number of small x-tics between the big x-tics
        parameter_list["mytics"] = self.get_axis_properties()["mytics"] # number of small y-tics between the big y-tics
        if self.plot_properties.get("logscale_y",True):
            parameter_list["logscale_y"] = "set logscale y" # determine wether y-achsis uses a logscale
            parameter_list["format_y"] = "\"10^{\%T}\"" # format of the label of the y-tics
            parameter_list["mytics"] = 10 # number of small y-tics between the big y-tics
        else:
            parameter_list["logscale_y"] = "#set logscale y"
            parameter_list["format_y"] = "" # format of the label of the y-tics
        if self.plot_properties.get("logscale_x",False): parameter_list["logscale_x"] = "set logscale x" # determine wether x-achsis uses a logscale
        else: parameter_list["logscale_x"] = "#set logscale x"
        parameter_list["ytic_offset_x"] = self.plot_properties.get("ytic_offset_x",0)   # offset in x-direction of the label at the y-tics
        parameter_list["ytic_offset_y"] = self.plot_properties.get("ytic_offset_y",0.1) # offset in y-direction  of the label at the y-tics
        parameter_list["ylabel"] = self.get_axislabels_and_units()["ylabel"] # label of the y-axis
        parameter_list["yunit"]  = self.get_axislabels_and_units()["yunit"]  # unit of the y-axis
        if all(key in self.plot_properties for key in ("process","collider","energy")):
            parameter_list["title"] = self.plot_properties["process"]+"\\\\@"+self.plot_properties["collider"]+" "+self.plot_properties["energy"] # set upper right title
        elif "title" in self.plot_properties:
            parameter_list["title"] = self.plot_properties["title"]
        else:
            parameter_list["title"] = ""

        settings_general = """
## general settings
set key at graph %(key_x)s, %(key_y)s
set xtics %(xtics)s
set xtics add %(xtics_add)s
set mxtics %(mxtics)s
set mytics %(mytics)s
%(logscale_y)s
%(logscale_x)s
set ytic offset %(ytic_offset_x)s, %(ytic_offset_y)s
set format y %(format_y)s

set label \"%(ylabel)s %(yunit)s\" at graph 0, 1.06
set label \"%(title)s\" right at graph 1, graph 1.07

set output \"%(pdf_file)s\"
""" % parameter_list # takes the values from the parameter_list dictionary from the keys in the string
        return settings_general
#}}}
#{{{ def: get_gnuplot_default_main_frame(self)
    def get_gnuplot_default_main_frame(self):
        # function that returns the default settings for the main frame to create the gnuplot file
        default_main_frame = """
##############
# main frame #
##############

# origin, size of main frame
set origin 0, 0.48
set size 1, 0.47
set bmargin 0 # set marging to remove space
set tmargin 0 # set margin to remove space
set format x \"\"
"""
        return default_main_frame
#}}}
#{{{ def: get_gnuplot_settings_main_frame(self)
    def get_gnuplot_settings_main_frame(self):
        # function that returns user-definiable settings in the main frame to create the gnuplot file
        settings_main_frame = """
## define line styles
## define line styles
set style line 2 dt (3,3) lc rgb \"black\" lw 1
set style line 3 dt (7,4) lc rgb \"red\" lw 1
set style line 1 lt 4 lc rgb \"blue\" lw 1
set style line 4 dt (10,3,3,3) lc rgb \"magenta\" lw 1
set style line 5 dt (15,2) lc rgb \"forest-green\" lw 1
set style line 6 dt (8,4,8,4,3,4) lc rgb \"forest-green\" lw 1
set style line 7 dt (10,3,3,3,3,3) lc rgb \"#B8860B\" lw 1
set style line 8 lt 1 lc rgb \"violet\" lw 1
set style line 9 dt (10,3,3,3) lc rgb \"brown\" lw 1

## for the uncertainty band borders (less thick)
set style line 12 dt (3,3) lc rgb \"black\" lw 0.1
set style line 13 dt (9,6) lc rgb \"red\" lw 0.1
set style line 11 dt (15,2) lc rgb \"blue\" lw 0.1
set style line 14 lt 4 lc rgb \"magenta\" lw 0.1
set style line 15 dt (20,3,10,3) lc rgb \"forest-green\" lw 0.1
set style line 16 dt (7,4) lc rgb \"forest-green\" lw 0.1
set style line 17 dt (10,3,3,3,3,3) lc rgb \"#B8860B\" lw 0.11
set style line 18 lt 1 lc rgb \"violet\" lw 0.1
set style line 19 dt (10,3,3,3,3,3) lc rgb \"brown\" lw 0.1

# set style line 2 dt (3,3) lc rgb \"black\" lw 1
# set style line 3 dt (7,4) lc rgb \"red\" lw 1.25
# set style line 1 lt 1 lc rgb \"blue\" lw 0.75
# set style line 4 dt (10,3,3,3) lc rgb \"forest-green\" lw 0.75
# set style line 5 lt 5 lc rgb \"orange\" lw 0.75
# set style line 6 lt 6 lc rgb \"magenta\" lw 0.75
# ## for the uncertainty band borders (less thick)
# set style line 12 dt (3,3) lc rgb \"black\" lw 0.1
# set style line 13 dt (9,6) lc rgb \"red\" lw 0.1
# set style line 11 lt 1 lc rgb \"blue\" lw 0.1
# set style line 14 dt (10,3,3,3) lc rgb \"forest-green\" lw 0.1
# set style line 15 lt 5 lc rgb \"orange\" lw 0.1
# set style line 16 lt 6 lc rgb \"magenta\" lw 0.1

## define ranges
set xrange [%(xmin)s:%(xmax)s]
set yrange [%(ymin)s:%(ymax)s]

set multiplot
""" % self.get_axis_properties()
        return settings_main_frame
#}}}
#{{{ def: get_gnuplot_plot_main_frame(self)
    def get_gnuplot_plot_main_frame(self):
        # function that returns the plotting of curves in the main frame to create the gnuplot file
        plot_main_frame = "plot "
        counter = 1
        order = ["LO","NLO","NNLO","N3LO","N4LO","N4LO","N4LO","N4LO","N4LO"] # use the order as the default label
        prop = self.curve_properties # introduce local short-cut
        # 2do: ADD LINE STYLES HERE !!! NOT ABOVE !!!
        last_curve = ""
        for curve in self.curve_list:
            line_style = prop[curve].get("line_style",counter)
            if counter in self.plot_properties.get("exclude_from_main",[]): 
                last_curve = curve
                counter += 1
                continue
            if prop[curve].get("exclude_from_main",False):
                last_curve = curve
                counter += 1
                continue
            if counter > 1 and counter-1 not in self.plot_properties.get("exclude_from_main",[]) and not prop.get(last_curve,{}).get("exclude_from_main",False): plot_main_frame += ",\\\n"
            if prop[curve].get("format") == "data":
                plot_main_frame += "\"%s\" using 1:2:($3*$2/100) with yerrorbars lc rgb \"dark-green\" lw 1 lt 7 ps 0.7 title \"%s\"" % (curve,prop[curve].get("label",order[counter-1]))
            else:
                plot_main_frame += "\"%s\" using 1:2 with lines ls %s title \"%s\"" % (curve,line_style,prop[curve].get("label",order[counter-1]))
            if prop[curve].get("uncertainties",True) and prop[curve].get("show_uncertainties",True):
                plot_main_frame += ", \"%s\" using 1:4:6 with filledcurves ls %s fs transparent solid 0.15 notitle" % (curve,line_style)
                plot_main_frame += ", \"%s\" using 1:4 with lines ls 1%s notitle" % (curve,line_style)
                plot_main_frame += ", \"%s\" using 1:6 with lines ls 1%s notitle" % (curve,line_style)
            last_curve = curve
            counter += 1
        return plot_main_frame
#}}}
#{{{ def: get_gnuplot_default_ratio(self)
    def get_gnuplot_default_ratio(self):
        # function that returns the default settings for the ratio frame to create the gnuplot file
        default_ratio = """
###############
# ratio inset #
###############

## remove previous settings
unset label  
#unset key
unset logscale y
unset format

## set ratio inset size
set size 1, 0.32
set origin 0, 0.11
"""
        return default_ratio
#}}}
#{{{ def: get_gnuplot_settings_ratio(self)
    def get_gnuplot_settings_ratio(self):
        # function that returns the user-definable settings of the ratio frame to create the gnuplot file
        order = ["LO","NLO","NNLO","N3LO","N4LO","N4LO","N4LO","N4LO","N4LO"] # use the order as the default label
        norm = self.curve_list[self.plot_properties.get("normalization",len(self.curve_list))-1] # gives the plot number that should be used for the normalization; default is to use the last        # create a parameter_list dictionary so that it is more obvious which values are set in the string created below
        parameter_list = {}
        # set all parameters that you can modify below, so that they can be passed to the string
        parameter_list["category"] = self.plot_properties.get("category","")
        parameter_list["categoryleft"] = self.plot_properties.get("categoryleft","")
        parameter_list["xtics_add"] = self.plot_properties.get("xtics_add","")
        parameter_list["norm_label"] = self.plot_properties.get("norm_label",self.curve_properties[norm].get("label",order[self.plot_properties.get("normalization",len(self.curve_list))-1]))
        if self.plot_properties.get("legend_ratio","right") == "right":
            parameter_list["key_x"]  = 0.93 # x-position of key 
            parameter_list["key_y"]  = 0.95 # y-position of key 
        elif self.plot_properties.get("legend_ratio","right") == "left":
            parameter_list["key_x"]  = 0.34 # x-position of key 
            parameter_list["key_y"]  = 0.95 # y-position of key 
        elif self.plot_properties.get("legend_ratio","right") == "down":
            parameter_list["key_x"]  = 0.59 # x-position of key 
            parameter_list["key_y"]  = 0.22 # y-position of key 
        if self.plot_properties.get("logscale_y_ratio",False):
            parameter_list["logscale_y"] = "set logscale y" # determine wether y-achsis uses a logscale
            parameter_list["format_y"] = "\"10^{\%T}\"" # format of the label of the y-tics
            parameter_list["mytics_ratio"] = 10 # number of small y-tics between the big y-tics
        else:
            parameter_list["logscale_y"] = "#set logscale y"
            parameter_list["format_y"] = "" # format of the label of the y-tics
        if self.plot_properties.get("logscale_x_ratio",False): parameter_list["logscale_x"] = "set logscale x" # determine wether x-achsis uses a logscale
        else: parameter_list["logscale_x"] = "#set logscale x"
        parameter_list["xtic_offset_x"] = self.plot_properties.get("xtic_offset_x",-0.21)   # offset in x-direction of the label at the y-tics
        parameter_list["xtic_offset_y"] = self.plot_properties.get("xtic_offset_y",0.4) # offset in y-direction  of the label at the y-tics


        settings_ratio = """
## can be changed
%(logscale_y)s
%(logscale_x)s
set format y %(format_y)s
set key at graph %(key_x)s, %(key_y)s
#set label \"ratio to %(norm_label)s\" at graph 0, 1.01
set label \"d{/Symbol s}/d{/Symbol s}_{%(norm_label)s}\" at graph 0, 1.1
set label \"%(category)s\" at graph 0.03, 2.5
set label \"%(categoryleft)s\" at graph 0.65, 2.5
set yrange [%(ymin_ratio)s:%(ymax_ratio)s]
set ytics %(ytics_ratio)s
set mytics %(mytics_ratio)s
set ytic offset 0.4, 0
set xtic offset %(xtic_offset_x)s,%(xtic_offset_y)s
set xtics %(xtics)s
set xtics add %(xtics_add)s
set mxtics %(mxtics)s
set xlabel offset 0,0.7
set xlabel  \"%(xlabel)s %(xunit)s\"
""" % dict(self.get_axislabels_and_units().items() + self.get_axis_properties().items() + parameter_list.items()) # concentrating the dictionaries (make sure no identical items)
        return settings_ratio
#}}}
#{{{ def: get_gnuplot_plot_ratio(self)
    def get_gnuplot_plot_ratio(self):
        # function that returns the plotting of curves in the ratio frame to create the gnuplot file
        plot_ratio = "plot "
        counter = 1
        order = ["LO","NLO","NNLO","N3LO","N4LO"] # use the order as the default label
        norm = self.curve_list[self.plot_properties.get("normalization",len(self.curve_list))-1] # gives the plot number that should be used for the normalization; default is to use the last curve
        prop = self.curve_properties # introduce local short-cut
        last_curve = ""
        for curve in self.curve_list:
            line_style = prop[curve].get("line_style",counter)
            if counter in self.plot_properties.get("exclude_from_ratio",[]): 
                last_curve = curve
                counter += 1
                continue
            if prop[curve].get("exclude_from_ratio",False):
                last_curve = curve
                counter += 1
                continue
            if counter > 1 and counter-1 not in self.plot_properties.get("exclude_from_ratio",[]) and not prop.get(last_curve,{}).get("exclude_from_ratio",False): plot_ratio += ",\\\n"
            columns = 7 if prop[curve].get("uncertainties",True) else 3 # determine number of comlumns simply by wether uncertainties are in file (7 columns) or not (3 columns)
            if prop[curve].get("format") == "data":
                plot_ratio += "\"<awk \'NR%%2==0\' %s | paste %s /dev/stdin\" using 1:($2/$5):($3*$2/100/$5) with yerrorbars lc rgb \"dark-green\" lw 1 lt 7 ps 0.7 %s" % (norm,curve,"title \"%s\"" % prop[curve].get("label",order[counter-1]) if prop[curve].get("exclude_from_main" ,False) or counter in self.plot_properties.get("exclude_from_main",[]) else "notitle")
#                plot_ratio += "\"<paste %s %s\" using 1:2/$5:($3*$2/100) with yerrorbars lc rgb \"dark-green\" lw 1 lt 111 ps 0.7 title \"%s\"" % (curve,norm,prop[curve].get("label",order[counter-1]))
            else:
                plot_ratio += "\"<paste %s %s\" using 1:($2/$%s) with lines ls %s %s" % (curve,norm,2+columns,line_style,"title \"%s\"" % prop[curve].get("label",order[counter-1]) if prop[curve].get("exclude_from_main" ,False) or counter in self.plot_properties.get("exclude_from_main",[]) else "notitle\\\n")
#                plot_ratio += "\"<paste %s %s\" using ($1+%s):($2/$%s):($3*2/$%s) every 2 with yerrorbars ls %s %s" % (curve.replace(".hist","_yerror.hist"),norm,self.binwidth/2,2+columns,2+columns,counter,"title \"%s\"" % prop[curve].get("label",order[counter-1]) if prop[curve].get("exclude_from_main" ,False) or counter in self.plot_properties.get("exclude_from_main",[]) else "notitle")
#                plot_ratio += "\"<paste %s %s\" using ($1):($2/$%s):($3*2/$%s) every 2 with yerrorbars ls %s %s" % (curve.replace(".hist","_yerror.hist"),norm,2+columns,2+columns,counter,"title \"%s\"" % prop[curve].get("label",order[counter-1]) if prop[curve].get("exclude_from_main" ,False) or counter in self.plot_properties.get("exclude_from_main",[]) else "notitle")
            if prop[curve].get("uncertainties",True) and prop[curve].get("show_uncertainties",True):
                plot_ratio += ", \"<paste %s %s\" using 1:($4/$%s):($6/$%s) with filledcurves ls %s fs transparent solid 0.15 notitle" % (curve,norm,2+columns,2+columns,line_style)
                plot_ratio += ", \"<paste %s %s\" using 1:($4/$%s) with lines ls 1%s notitle" % (curve,norm,2+columns,line_style)
                plot_ratio += ", \"<paste %s %s\" using 1:($6/$%s) with lines ls 1%s notitle" % (curve,norm,2+columns,line_style)
            last_curve = curve
            counter += 1

        return plot_ratio
#}}}
#{{{ def: get_axislabels_and_units(self)
    def get_axislabels_and_units(self):
        # function that returns a dictionary with all x and y labels and units
        axis_dict = {}

        # defaults if nothing is given or can be determined
        ylabel = "{/Symbol s}"
        yunit  = "[fb]"
        xlabel = self.plot_name
        xunit  = ""
        # try to determine labels from distribution input fil
        if os.path.isfile(pjoin(self.result_folder_path,"input_of_run","distribution.dat")):
            with open(pjoin(self.result_folder_path,"input_of_run","distribution.dat"),'r') as distribution_file:
                distribution_found = False
                particles = []
                for line in distribution_file:
                    if distribution_found:
                        # determine the properties of this distribution
                        if line.strip().startswith("distributiontype"):
                            distributiontype = line.split("=")[1].strip()
                        elif line.strip().startswith("particle"):
                            particles.append([line.split("=")[0].strip(),line.split("=")[1].strip()])
                        elif line.strip().startswith("distributionname"):
                            break
                    if line.strip().startswith("distributionname") and line.split("=")[1].strip() == self.plot_name: # check wether this distribution exists
                        distribution_found = True
                if not distribution_found:
                    axis_dict["ylabel"] = self.plot_properties.get("ylabel",ylabel)
                    axis_dict["yunit"]  = self.plot_properties.get("yunit",yunit)
                    axis_dict["xlabel"] = self.plot_properties.get("xlabel",xlabel)
                    axis_dict["xunit"]  = self.plot_properties.get("xunit",xunit)
                    return axis_dict
                # set label according to distributiontype and particles
                xlabel = self.distributiontype_mapping.get(distributiontype,distributiontype)
                previous = ""
                for item in particles:
                    if not previous:
                        xlabel += "({/Times-New-Roman=26"
                    elif previous == item[0]:
                        xlabel += "+"
                    else:
                        xlabel += ","
                    particle    = item[1].split()[0].strip()
                    try:
                        particle_nr = item[1].split()[1].strip()
                    except:
                        particle_nr = "{}"
                        pass
                    if particle_nr != "{}" and "^" in self.particle_mapping.get(particle,particle) and "/" in self.particle_mapping.get(particle,particle).replace("{/","nuuueeet"):
                        # both cases can happen at the same time for neutrinos
                        xlabel_tmp = self.particle_mapping.get(particle,particle).replace("{/","nuuueeet").split("/")[0]+"{/Times-New-Roman=26 _"+particle_nr+"}/"+self.particle_mapping.get(particle,particle).replace("{/","nuuueeet").split("/")[1]+"_"+particle_nr
                        xlabel += xlabel_tmp.replace("nuuueeet","{/").replace("^","\@^") # much simpler than with the splitting around "^" below !!! ...anyway both work; BUT DON'T REPLACE EVERYWHERE !!!
                    elif particle_nr != "{}" and "^" in self.particle_mapping.get(particle,particle):
                        # this is for the case when there is a "^" in the particle then we need to add an @ in case there is also a particle_nr
                        xlabel += self.particle_mapping.get(particle,particle).split("^")[0]+"\@^"+self.particle_mapping.get(particle,particle).split("^")[1]+"_"+particle_nr
                    elif particle_nr != "{}" and "/" in self.particle_mapping.get(particle,particle).replace("{/","nuuueeet"):
                        # this is for the case when there is a "/" in the particle then we need to add the subscript to both before and after the "/"
                        xlabel += self.particle_mapping.get(particle,particle).replace("{/","nuuueeet").split("/")[0]+"{/Times-New-Roman=26 _"+particle_nr+"}/"+self.particle_mapping.get(particle,particle).replace("{/","nuuueeet").split("/")[1]+"_"+particle_nr
                        xlabel = xlabel.replace("nuuueeet","{/")
                    else: # normal case
                        xlabel += "%s_%s" % (self.particle_mapping.get(particle,particle),particle_nr)
                    previous = item[0]
                if particles:
                    xlabel += "})"
                ylabel = "d{/Symbol s}/d%s" % self.plot_properties.get("xlabel",xlabel)
                if distributiontype in self.unit_mapping:# use if instead direct get to put brackets around if exists, and none otherwise
                    xunit = "[%s]" % self.unit_mapping[distributiontype]
                    if "yunit" in self.plot_properties:
                        yunit = "%s" % self.plot_properties.get("yunit",yunit)
                    else:
                        yunit = "[fb/%s]" % self.unit_mapping[distributiontype]
                else:
                    xunit = ""
                    yunit = "[fb]"

        # make special case for total cross section and jets
        # overwrite by presets
        ylabel = "d{/Symbol s}/d%s" % self.plot_properties.get("xlabel",xlabel)

        if self.plot_properties.get("xunit",xunit):
            yunit = "[fb/%s]" % self.plot_properties.get("xunit",xunit)
            xunit = "[%s]" % self.plot_properties.get("xunit",xunit)

        axis_dict["ylabel"] = self.plot_properties.get("ylabel",ylabel)
        axis_dict["yunit"]  = self.plot_properties.get("yunit",yunit)
        axis_dict["xlabel"] = self.plot_properties.get("xlabel",xlabel)
        axis_dict["xunit"]  = xunit
        return axis_dict
#}}}
#{{{ def: get_axis_properties(self)
    def get_axis_properties(self):
        # function that returns a dictionary with all x and y labels and units
        axis_dict = {}

        # defaults if nothing is given or can be determined
        # xtics  = 50
        # mxtics = 5
        # mytics = 10
        # xmin   = 0
        # xmax   = 200
        # ymin   = 0.0001
        # ymax   = 100
        # ytics_ratio = 0.2 #"(0.6, 0.8, 1, 1.2, 1.4)"
        # mytics_ratio= 4
        # ymin_ratio  = 0.5
        # ymax_ratio  = 1.5

        # loop through all curve files and determine minimum, maximum of x and y axis
        # also do this for y axis of ratio
        # first read normalization curve, then others (including uncertainties)
        with open(self.curve_list[self.plot_properties.get("normalization",len(self.curve_list))-1], 'r') as norm_curve:
            x_values = []
            y_values_norm = {}
            for line in norm_curve:
                line = line.strip() # strip removes all spaces (including tabs and newlines)
                # if any line starts with %, # or is an emtpy line (disregarding spaces) it is a comment line and should be skipped
                if line=="" or line[0]=="%" or line[0]=="#": 
                    continue
                x_value = float(line.split(None,1)[0].strip())
                x_values.append(x_value)
                y_value = float(line.split(None,1)[1].strip().split()[0])
                y_values_norm[x_value] = y_value
        # then loop over all other files to determine the maximum and minimum y values
        y_values = []
        y_values_ratio = []
        for curve in self.curve_list:
          if self.curve_properties[curve].get("format") == "data":
              continue
          with open(curve, 'r') as curve_in:
            counter = 0
            for line in curve_in:
                line = line.strip() # strip removes all spaces (including tabs and newlines)
                # if any line starts with %, # or is an emtpy line (disregarding spaces) it is a comment line and should be skipped
                if line=="" or line[0]=="%" or line[0]=="#": 
                    continue
                x_value = round(float(line.split(None,1)[0].strip()),10)
                if self.curve_properties[curve].get("uncertainties",True) and self.curve_properties[curve].get("show_uncertainties",True):
                    counter += 1
                    y_value1 = float(line.split(None,1)[1].strip().split()[0])
                    y_value2 = float(line.split(None,1)[1].strip().split()[2])
                    y_value3 = float(line.split(None,1)[1].strip().split()[4])
                    if y_value1 == 0 or y_value2 == 0 or y_value3 == 0 or math.isnan(y_value1) or math.isnan(y_value2) or math.isnan(y_value3):
                        continue
                    # for histograms we have to skip every even line
                    if not "format" in self.curve_properties[curve] or self.curve_properties[curve]["format"] == "histogram":
                        if counter % 2 == 0: # if the counter is even
                            continue
                    y_values.extend([y_value1,y_value2,y_value3])
                    try:
                        y_norm = y_values_norm[x_value]
                    except:
                        y_norm = 0
                    if y_norm == 0 or math.isnan(x_value): # skip zero values in norm (will make an infinitely large plot)
                        continue
                    y_values_ratio.extend([y_value1/y_norm,y_value2/y_norm,y_value3/y_norm])
                else:
                    y_value = float(line.split(None,1)[1].strip().split()[0])
                    y_values.append(y_value)
                    try:
                        y_norm = y_values_norm[x_value]
                    except:
                        y_norm = 0
                    if y_norm == 0 or math.isnan(x_value): # skip zero values in norm (will make an infinitely large plot)
                        continue
                    y_values_ratio.append(y_value/y_norm)


        if not y_values or not y_values_ratio:
            return False
        xmin  = min(x_values)
        xmax  = max(x_values)
        xtics  = "" # let gnuplot decide the distance between xtics
        mxtics = "" # let gnuplot decide the distance between small xtics
        mytics = ""
        ymin  = ""#min(y_values)  
        ymax  = ""#math.ceil(max(y_values))#int(math.ceil(max(y_values) / 10.0)) * 10 # rounds to the closest multiple of 10
        ymin_ratio = max(min(y_values_ratio),0)  
        ymax_ratio = min(max(y_values_ratio),3)
        axis_dict["ymin_ratio"]   = self.plot_properties.get("ymin_ratio",ymin_ratio)
        axis_dict["ymax_ratio"]   = self.plot_properties.get("ymax_ratio",ymax_ratio)
        ytics_ratio = math.ceil((axis_dict["ymax_ratio"]-axis_dict["ymin_ratio"])/5*10)/10
        mytics_ratio= ytics_ratio/0.1

        axis_dict["xtics"]  = self.plot_properties.get("xtics",xtics)
        axis_dict["mxtics"] = self.plot_properties.get("mxtics",mxtics)
        axis_dict["xtics_ratio"]  = self.plot_properties.get("xtics",xtics)
        axis_dict["mxtics_ratio"] = self.plot_properties.get("mxtics",mxtics)
#        if not "ymin" in self.plot_properties and not "ymax" in self.plot_properties:
        axis_dict["mytics"] = self.plot_properties.get("mytics",mytics)
        axis_dict["xmin"]  = self.plot_properties.get("xmin",xmin)
        axis_dict["xmax"]  = self.plot_properties.get("xmax",xmax)
        axis_dict["ymin"]  = self.plot_properties.get("ymin",ymin)
        axis_dict["ymax"]  = self.plot_properties.get("ymax",ymax)
        axis_dict["ytics_ratio"]  = self.plot_properties.get("ytics_ratio",ytics_ratio)
        if not "ymin_ratio" in self.plot_properties and not "ymax_ratio" in self.plot_properties:
            axis_dict["mytics_ratio"] = self.plot_properties.get("mytics_ratio",mytics_ratio)
        else:
            axis_dict["mytics_ratio"] = self.plot_properties.get("mytics_ratio","")
#        axis_dict[""]  = self.plot_properties.get("",)
        return axis_dict
#}}}
#{{{ def: define_all_label_mappings(self)
    def define_all_label_mappings(self):
        # function that defines class dictionaries for the mappings from the distribution.dat file to the labels
        # distributiontype: mapping from distributiontype to the xlabel
        self.distributiontype_mapping = {}
        self.distributiontype_mapping["pT"]           = "p_{/Times-New-Roman=18 T}"
        self.distributiontype_mapping["pTveto"]       = "p\@_{/Times-New-Roman=18 T}^{veto}"
        self.distributiontype_mapping["pTmin"]        = "p\@_{/Times-New-Roman=18 T}_{min}"
        self.distributiontype_mapping["pTmax"]        = "p\@_{/Times-New-Roman=18 T}_{max}"
        self.distributiontype_mapping["m"]            = "m"
        self.distributiontype_mapping["phi"]          = "{/Symbol Dj}"
        self.distributiontype_mapping["eta"]          = "{/Symbol h}"
        self.distributiontype_mapping["y"]            = "y"
        self.distributiontype_mapping["mTATLAS"]      = "m\@_{/Times-New-Roman=18 T}^{/Times-New-Roman=18 ATLAS}"
        self.distributiontype_mapping["multiplicity"] = "#"
        
        # determine units for these distributions
        self.unit_mapping = {}
        self.unit_mapping["pT"]           = "GeV"
        self.unit_mapping["pTveto"]       = "GeV"
        self.unit_mapping["pTmin"]        = "GeV"
        self.unit_mapping["pTmax"]        = "GeV"
        self.unit_mapping["m"]            = "GeV"
#        self.unit_mapping["phi"]          = ""
#        self.unit_mapping["eta"]          = ""
#        self.unit_mapping["y"]            = ""
        self.unit_mapping["mTATLAS"]      = "GeV"
#        self.unit_mapping["multiplicity"] = ""

        # define nicer output for particles
        self.particle_mapping = {}
        self.particle_mapping["photon"] = "{/Symbol g}"
        self.particle_mapping["lep"]    = "l"
        self.particle_mapping["nclep"]  = "l^-"
        self.particle_mapping["pclep"]  = "l^+"
        self.particle_mapping["e"]      = "e"
        self.particle_mapping["em"]     = "e^-"
        self.particle_mapping["ep"]     = "e^+"
        self.particle_mapping["mu"]     = "{/Symbol m}"
        self.particle_mapping["tau"]    = "{/Symbol t}"
        self.particle_mapping["mum"]    = "{/Symbol m}^-"
        self.particle_mapping["mup"]    = "{/Symbol m}^+"
        self.particle_mapping["taum"]   = "{/Symbol g}^-"
        self.particle_mapping["taup"]   = "{/Symbol t}^+"
        self.particle_mapping["ljet"]   = "light-j"
        self.particle_mapping["jet"]    = "j"
        self.particle_mapping["bjet"]   = "b"
        self.particle_mapping["tjet"]   = "t/~t\342\200\276&{t}"
        self.particle_mapping["top"]    = "t"
        self.particle_mapping["atop"]   = "~t\342\200\276&{t}"
        self.particle_mapping["wm"]     = "W^-"
        self.particle_mapping["wp"]     = "W^+"
        self.particle_mapping["z"]      = "Z"
        self.particle_mapping["h"]      = "H"
        self.particle_mapping["nua"]    = "{/Symbol n/~n{/Times-New-Roman=26 \342\200\276}&{.}}"
        self.particle_mapping["nu"]     = "{/Symbol n}"
        self.particle_mapping["nux"]    = "{/Symbol ~n{/Times-New-Roman=26 \342\200\276}&{.}}"
        self.particle_mapping["nea"]    = "{/Symbol n^{/Times-New-Roman=26 e}/~n{/Times-New-Roman=26 \342\200\276}&{.}^{/Times-New-Roman=26 e}}"
        self.particle_mapping["ne"]     = "{/Symbol n^{/Times-New-Roman=26 e}}"
        self.particle_mapping["nex"]    = "{/Symbol ~n{/Times-New-Roman=26 \342\200\276}&{.}^{/Times-New-Roman=26 e}}"
        self.particle_mapping["nma"]    = "{/Symbol n^{m}/~n{/Times-New-Roman=26 \342\200\276}&{.}^{m}}"
        self.particle_mapping["nm"]     = "{/Symbol n^{m}}"
        self.particle_mapping["nmx"]    = "{/Symbol ~n{/Times-New-Roman=26 \342\200\276}&{.}^{m}}"
        self.particle_mapping["nta"]    = "{/Symbol n^{t}/~n{/Times-New-Roman=26 \342\200\276}&{.}^{t}}"
        self.particle_mapping["nt"]     = "{/Symbol n^{t}}"
        self.particle_mapping["ntx"]    = "{/Symbol ~n{/Times-New-Roman=26 \342\200\276}&{.}^{t}}"
#}}}

#}}}


if __name__ == "__main__":
    all_plots = glob.iglob(pjoin(os.getcwd(),"MiNNLO_Wp_kQ05_lhef-run/distributions/*.dat"))

    out = print_output()
    gnu = gnuplot(os.getcwd())
    gnu.clean_gnuplot_folder()
    for plot in all_plots:
        
        if "debug" in plot:
            continue

        gnu = gnuplot(os.getcwd())

        MiNNLO_lhef_kQ05 = plot
        MiNLO_lhef_kQ05 = plot.replace("MiNNLO_W","MiNLO_W").replace("_MiNNLO","_MiNLO")
        MiNNLO_lhef_kQ1 = plot.replace("kQ05","kQ1")
        MiNLO_lhef_kQ1 = MiNNLO_lhef_kQ1.replace("MiNNLO_W","MiNLO_W").replace("_MiNNLO","_MiNLO")
        MiNNLO_lhef_kQ025 = plot.replace("kQ05","kQ025")
        MiNLO_lhef_kQ025 = MiNNLO_lhef_kQ025.replace("MiNNLO_W","MiNLO_W").replace("_MiNNLO","_MiNLO")

        NLOPS_lhef_NNLOPDF = plot.replace("MiNNLO_Wp_kQ05_lhef","NLO+PS_NNLOPDF_lhef")
        NLOPS_lhef_NLOPDF = plot.replace("MiNNLO_Wp_kQ05_lhef","NLO+PS_NLOPDF_lhef")

        # MATRIX_NNLO = plot.replace("MiNNLO_lhef_kQ05-run","NNLO-run").replace("__MiNNLO_lhef_kQ05","__NNLO_QCD")
        # MATRIX_NLO = MATRIX_NNLO.replace("NNLO_QCD","NLO_QCD").replace("NNLO-run","NLO-run")
        # MATRIX_LO = MATRIX_NNLO.replace("NNLO_QCD","LO").replace("NNLO-run","LO-run")

        # MATRIX_NNLO_HT2 = plot.replace("MiNNLO_lhef_kappaq05-run","NNLO_HT2-run").replace("__MiNNLO_lhef_kappaq05","__NNLO_QCD")
        # MATRIX_NLO_HT2 = MATRIX_NNLO_HT2.replace("NNLO_QCD","NLO_QCD").replace("NNLO_HT2-run","NLO_HT2-run")
        # MATRIX_LO_HT2 = MATRIX_NNLO_HT2.replace("NNLO_QCD","LO").replace("NNLO_HT2-run","LO_HT2-run")

        counter = 0

        if os.path.exists(MiNNLO_lhef_kQ05):
            gnu.add_curve(MiNNLO_lhef_kQ05,{"format" : "histogram", "label" : "MiNNLO (LHE)","line_style" : 1})
        # if os.path.exists(MiNNLO_lhef_kQ025):
        #     gnu.add_curve(MiNNLO_lhef_kQ025,{"format" : "histogram", "label" : "MiNNLO (LHE) kQ=0.25","line_style" : 4})
        # if os.path.exists(MiNLO_lhef_kQ025):
        #     gnu.add_curve(MiNLO_lhef_kQ025,{"format" : "histogram", "label" : "MiNLO (LHE) kQ=0.25","line_style" : 6})
        if os.path.exists(MiNLO_lhef_kQ05):
            gnu.add_curve(MiNLO_lhef_kQ05,{"format" : "histogram", "label" : "MiNLO (LHE)","line_style" : 2})
        # if os.path.exists(MiNNLO_lhef_kQ1):
        #     gnu.add_curve(MiNNLO_lhef_kQ1,{"format" : "histogram", "label" : "MiNNLO (LHE) kQ=1.0","line_style" : 4})
        # if os.path.exists(MiNLO_lhef_kQ1):
        #     gnu.add_curve(MiNLO_lhef_kQ1,{"format" : "histogram", "label" : "MiNLO (LHE) kQ=1.0","line_style" : 5})
        if os.path.exists(NLOPS_lhef_NLOPDF):
            gnu.add_curve(NLOPS_lhef_NLOPDF,{"format" : "histogram", "label" : "NLO+PS","line_style" : 5})
        # if os.path.exists(NLOPS_lhef_NNLOPDF):
        #     gnu.add_curve(NLOPS_lhef_NNLOPDF,{"format" : "histogram", "label" : "NLO+PS NNLOPDFs","line_style" : 5})
        # if os.path.exists(MATRIX_NLO):
        #      gnu.add_curve(MATRIX_NLO,{"format" : "histogram", "label" : "NLO QCD (MATRIX)","line_style" : 5})
        # if os.path.exists(MATRIX_NNLO):
        #     gnu.add_curve(MATRIX_NNLO,{"format" : "histogram", "label" : "NNLO QCD (MATRIX)","line_style" : 3})

            
        gnu.set_plot_properties("normalization",1)
        gnu.set_plot_properties("ymin_ratio",0.2)
        gnu.set_plot_properties("ymax_ratio",1.6)
#        gnu.set_plot_properties("ytics_ratio","")
        gnu.set_plot_properties("rebin",1)
        # if gnu.get_name().startswith("ATLAS_"):
        #     continue
        # if "j1" in plot or "j2" in plot:
        #     continue

        skip = False
        if "CMS" in gnu.get_name():
            continue
        if "mbbZ1000" in gnu.get_name():
            gnu.set_plot_properties("category","m_{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν}} < 1000 GeV")
        elif "mbbZ750" in gnu.get_name():
            gnu.set_plot_properties("category","m_{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν}} < 750 GeV")
        elif "mbbZ500" in gnu.get_name():
            gnu.set_plot_properties("category","m_{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν}} < 500 GeV")
        elif "mbbZ250" in gnu.get_name():
            gnu.set_plot_properties("category","m_{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν}} < 250 GeV")
        elif "mbbZ150" in gnu.get_name():
            gnu.set_plot_properties("category","m_{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν}} < 150 GeV")
        elif "ptj200" in gnu.get_name():
            gnu.set_plot_properties("category","p_{/Times=18 T,j_1} > 200 GeV")
        elif "ptj20" in gnu.get_name():
            gnu.set_plot_properties("category","p_{/Times=18 T,j_1} > 20 GeV")
        elif "ptj30" in gnu.get_name():
            gnu.set_plot_properties("category","p_{/Times=18 T,j_1} > 30 GeV")
        elif "ptj60" in gnu.get_name():
            gnu.set_plot_properties("category","p_{/Times=18 T,j_1} > 60 GeV")
        elif "ptj120" in gnu.get_name():
            gnu.set_plot_properties("category","p_{/Times=18 T,j_1} > 120 GeV")
#        gnu.set_plot_properties("legend", "left")

        if gnu.get_name().startswith("dphi_b-bx"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","{/Symbol \104}{/Symbol f}_{b,~{b}{.75\342\210\222}}")
        if gnu.get_name().startswith("dphi_bbZ-j1"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","{/Symbol \104}{/Symbol f}_{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν},j_1}")
        if gnu.get_name().startswith("dy_b-bx"):
            gnu.set_plot_properties("xlabel","{/Symbol \104}{y}_{b,~{b}{.75\342\210\222}}")
        if gnu.get_name().startswith("dy_bbZ-j1"):
            gnu.set_plot_properties("xlabel","{/Symbol \104}{y}_{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν},j_1}")
            if "ptj200" in gnu.get_name():
                gnu.set_plot_properties("rebin",10)
            elif "ptj20" in gnu.get_name():
                gnu.set_plot_properties("rebin",4)
            elif "ptj30" in gnu.get_name():
                gnu.set_plot_properties("rebin",4)
            elif "ptj60" in gnu.get_name():
                gnu.set_plot_properties("rebin",8)
            elif "ptj120" in gnu.get_name():
                gnu.set_plot_properties("rebin",8)

        if gnu.get_name().startswith("eta_bx"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","{/Symbol h}_{~{b}{.75\342\210\222}} ")
        elif gnu.get_name().startswith("eta_b"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","{/Symbol h}_{b}")
        if gnu.get_name().startswith("y_Z"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","y_{ℓ^+{/Menlo=30 ν}}")
            # gnu.set_plot_properties("xmin", -3)
            # gnu.set_plot_properties("xmax",  3)
            gnu.set_plot_properties("rebin",2)
        if gnu.get_name().startswith("y_em"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","y_{{/Menlo=30 ν}}")
            # gnu.set_plot_properties("xmin", -3)
            # gnu.set_plot_properties("xmax",  3)
            gnu.set_plot_properties("rebin",2)
        if gnu.get_name().startswith("y_ep"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","y_{ℓ^+}")
            # gnu.set_plot_properties("xmin", -3)
            # gnu.set_plot_properties("xmax",  3)
            gnu.set_plot_properties("rebin",2)
        if gnu.get_name().startswith("y_bbZ"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","y_{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν}}")
            gnu.set_plot_properties("rebin",2)
        elif gnu.get_name().startswith("y_bb"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","y_{b~{b}{.75\342\210\222}} ")
            gnu.set_plot_properties("rebin",2)
        elif gnu.get_name().startswith("y_bx"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","y_{~{b}{.75\342\210\222}} ")
            gnu.set_plot_properties("rebin",2)
        elif gnu.get_name().startswith("y_b"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","y_{b}")
            gnu.set_plot_properties("rebin",2)
        if gnu.get_name().startswith("y_j1"):
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("xlabel","y_{j_1}")
            gnu.set_plot_properties("rebin",2)
            
        if gnu.get_name().startswith("pt_bbZ"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν}}")
            if gnu.get_name().startswith("pt_bbZ-zoom"):
                gnu.set_plot_properties("rebin",1)
            else:
                gnu.set_plot_properties("rebin",5)
        elif gnu.get_name().startswith("pt_bb"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},{b~{b}{.75\342\210\222}} ")
            gnu.set_plot_properties("rebin",4)
            if gnu.get_name().startswith("pt_bb-zoom"):
                pass
            else:
                pass
        elif gnu.get_name().startswith("pt_bx"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},~{b}{.75\342\210\222}} ")
            gnu.set_plot_properties("rebin",2)
            if gnu.get_name().startswith("pt_bx-zoom"):
                pass
            else:
                pass
        elif gnu.get_name().startswith("pt_b"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},b}")
            gnu.set_plot_properties("rebin",2)
            if gnu.get_name().startswith("pt_b-zoom"):
                pass
            else:
                pass
        if gnu.get_name().startswith("pt_b1"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},b_1}")
            gnu.set_plot_properties("rebin",2)
            if gnu.get_name().startswith("pt_b1-zoom"):
                pass
            else:
                pass
        if gnu.get_name().startswith("pt_b2"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},b_2}")
            gnu.set_plot_properties("rebin",4)
            if gnu.get_name().startswith("pt_b2-zoom"):
                pass
            else:
                pass
        if gnu.get_name().startswith("pt_em"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},{/Menlo=30 ν}}")
            if gnu.get_name().startswith("pt_em-zoom"):
                gnu.set_plot_properties("rebin",2)
            else:
                gnu.set_plot_properties("rebin",4)
        if gnu.get_name().startswith("pt_ep"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},ℓ^+}")
            if gnu.get_name().startswith("pt_ep-zoom"):
                gnu.set_plot_properties("rebin",2)
            else:
                gnu.set_plot_properties("rebin",4)
        if gnu.get_name().startswith("pt_lep1"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},ℓ_1}")
            gnu.set_plot_properties("rebin",2)
        if gnu.get_name().startswith("pt_lep2"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},ℓ_2}")
            gnu.set_plot_properties("rebin",4)
        if gnu.get_name().startswith("pt_j1"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},j_1}")
            if gnu.get_name().startswith("pt_j1-zoom"):
                gnu.set_plot_properties("rebin",1)
            else:
                gnu.set_plot_properties("rebin",2)
        if gnu.get_name().startswith("pt_j2"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},j_2}")
            if gnu.get_name().startswith("pt_j2-zoom"):
                gnu.set_plot_properties("rebin",1)
            else:
                gnu.set_plot_properties("rebin",4)
        if gnu.get_name().startswith("pt_Z"):
            gnu.set_plot_properties("xlabel","p_{{/Times-New-Roman=18 T},ℓ^+{/Menlo=30 ν}}")
            if gnu.get_name().startswith("pt_Z-zoom"):
                gnu.set_plot_properties("rebin",1)
            else:
                gnu.set_plot_properties("rebin",5)
            
        if gnu.get_name().startswith("m_Z"):
            gnu.set_plot_properties("xlabel","m_{ℓ^+{/Menlo=30 ν}}")
            if gnu.get_name().startswith("m_Z-zoom"):
                pass
            else:
                pass            
        if gnu.get_name().startswith("m_bbZ"):
            gnu.set_plot_properties("xlabel","m_{b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν}}")
            if gnu.get_name().startswith("m_bbZ-ptj"):  gnu.set_plot_properties("rebin",20)
            if gnu.get_name().startswith("m_bbZ-mbbZ"): gnu.set_plot_properties("rebin",20)
            if gnu.get_name().startswith("m_bbZ-zoom"):
                pass
            else:
                pass
        elif gnu.get_name().startswith("m_bb"):
            gnu.set_plot_properties("xlabel","m_{b~{b}{.75\342\210\222}} ")
            if gnu.get_name().startswith("m_bb-zoom"):
                pass
            else:
                pass
            
        # if (gnu.get_name().startswith("m_") or gnu.get_name().startswith("pt_")) and not "zoom" in gnu.get_name():
        #     gnu.set_plot_properties("rebin", 4)
        # if gnu.get_name().startswith("m_bbZ-"):
        #     gnu.set_plot_properties("rebin", 10)
            
        if gnu.get_name().startswith("n_jet"): # for njets, treat it as special case and combine it with total rate in "-1" bin
            gnu.set_plot_properties("logscale_y",False)
            gnu.set_plot_properties("ylabel","{/Symbol s}")
            gnu.set_plot_properties("xlabel","")
            gnu.set_plot_properties("xtics","(\"total rate\" -0.5,\"0-jet\" 0.5,\"1-jet\" 1.5,\"2-jet\" 2.5)")
#            gnu.set_plot_properties("ytics","")
            gnu.set_plot_properties("xmin",-1)
            gnu.set_plot_properties("ymin_ratio",0.3)
            gnu.set_plot_properties("ymax_ratio",1.2)
        if gnu.get_name().startswith("log") or gnu.get_name().startswith("pT") or gnu.get_name().startswith("m"):
            gnu.set_plot_properties("xunit","GeV")
            
        elif gnu.get_name().startswith("pTveto"): # treat this later as special case inside the code (with distributiontype)
            continue

#        gnu.set_plot_properties("ylabel","d{/Symbol s}/bin")
#        gnu.set_plot_properties("process","pp{/Symbol \256}W^+Z{/Symbol \256}e^+ e^{\342\210\222} {/Symbola μ}^+ {/Courier=30 ν}_{/Symbola μ}")
        gnu.set_plot_properties("process","pp{/Symbol \256} b~{b}{.75\342\210\222} ℓ^+{/Menlo=30 ν}")
        gnu.set_plot_properties("collider","LHC")
        gnu.set_plot_properties("energy","13 TeV")
#        gnu.set_plot_properties("yunit","[fb]")
        #    gnu.set_plot_properties("reference","1111.1111")
        gnu.plot()
        # try:
        #     gnu.plot()
        # except:
        #     pass
    time.sleep(1)
    # combine the pdfs in gnuplot folder in one single pdf file
    # get all pdfs in gnuplot folder
    all_pdfs = glob.glob("gnuplot_LHEF/*.pdf")
    category_pdfs = list(sorted(glob.glob("gnuplot_LHEF/*-*.pdf")))
    nocategory_pdfs = list(sorted(list(set(all_pdfs) - set(category_pdfs)),key=len))
    
    all_pdfs = nocategory_pdfs + category_pdfs

#    command = "pdfunite"
    command="gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=gnuplot_LHEF/all_plots_vs_NNLO.pdf "
    # Appending all pdfs
    for pdf in all_pdfs:
        command += " \"%s\"" % pdf
    # Writing all the collected pages to a file
#    combined_pdf_file = pjoin("gnuplot_py8","all_plots_py8_HW.pdf")
#    command += " %s" % combined_pdf_file
    print subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
