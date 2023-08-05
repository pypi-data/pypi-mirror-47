 
import codecs
import regex as re
import yaml
import os
import shutil
from warnings import warn
from copy import deepcopy


class Config():
    def __init__(self):
        self.categories = {
            'Part':{'Reuse':False},
            'Tool':{'Reuse':True}
            }
        self.fussy=True
        self.defaultCategory = 'Part'
        self.partLibs = []
        self.debug=False

#global config object- I think I am ok with this!
config = Config()

def cleanYAML(txt):
    """
    This function returns a python dictionary from inline YAML.
    It does so by changing all commas into new lines. It also
    does some extra cleanup
    """
    txt = txt.replace(',','\n')
    # add space after : if forgotten
    
    matches = re.finditer('^(([^:]*?):(\S.*))$',txt,re.MULTILINE)
    for match in matches:
        txt=txt.replace(match.group(1),match.group(2)+': '+match.group(3))
    
    #puts quotes around ? to allow the Qty: ? syntax. This 
    #prohibits complex mapping keys.
    qs = re.findall(':(\s*\?\s*)$',txt,re.MULTILINE)
    for q in qs:
        txt=txt.replace(q," '?'")
    
    pydic = yaml.load(txt.replace(',','\n'), Loader=yaml.FullLoader)

    return pydic

    

class Documentation(object):
    
    def __init__(self,conf):
        
        confErrMsg = "Error in configuration YAML: "
        
        self.project_data = {'Title': None,'Authors': None,'Email': None,'Affiliation': None,'License': None}
        
        #reading config
        with open(conf, 'r') as stream:
            self.settings = yaml.load(stream, Loader=yaml.FullLoader)
                    
        
        #All the settings stuff could do with tudying up, it is becoming a lot of repeated code
        
        #Conversion settings
        assert 'OverviewPage' in self.settings, f'{confErrMsg}Cannot run without OverviewPage being set'
        self.overview = self.settings['OverviewPage']
        if 'CustomCategories' in self.settings:
            assert type(self.settings['CustomCategories']) is dict, f"{confErrMsg}CustomCategories mut be entered as a dictionary"
            #TODO: check all categories have correct reuse info.
            config.categories = {**config.categories, **self.settings['CustomCategories']}
        if 'DefaultCategory' in self.settings:
            assert self.settings['DefaultCategory'] in config.categories, f"{confErrMsg}The default category must be a defined category"
            config.defaultCategory = self.settings['DefaultCategory']
        if 'PartLibs' in self.settings:
            partLibs = self.settings['PartLibs']
            assert type(partLibs) is list, f"{confErrMsg}PartsLibs must be a list not a {type(partLibs)}"
            for lib in partLibs:
                assert type(lib) is str, f"{confErrMsg}Each item in PartsLibs must be a string"
            config.partLibs = partLibs
        if 'Fussy' in self.settings:
            config.fussy = bool(self.settings['Fussy'])
        
        #Project settings
        if 'Title' in self.settings:
            self.project_data['Title'] = self.settings['Title']
            assert type(self.project_data['Title']) is str, f"{confErrMsg}Title must be a string not a {type(self.project_data['Title'])}"
        if 'Authors' in self.settings:
            self.project_data['Authors'] = self.settings['Authors']
            if type(self.project_data['Authors']) is str:
                self.project_data['Authors'] = [self.project_data['Authors']]
            assert type(self.project_data['Authors']) is list, f"{confErrMsg}Authors must be a list not a {type(self.project_data['Authors'])}"
            for author in self.project_data['Authors']:
                assert type(author) is str, f"{confErrMsg}Each author in Authors must be a string"
        if 'Email' in self.settings:
            self.project_data['Email'] = self.settings['Email']
            assert type(self.project_data['Email']) is str, f"{confErrMsg}Email must be a string not a {type(self.project_data['Email'])}"
        if 'Affiliation' in self.settings:
            self.project_data['Affiliation'] = self.settings['Affiliation']
            assert type(self.project_data['Affiliation']) is str, f"{confErrMsg}Affiliation must be a string not a {type(self.project_data['Affiliation'])}"
        if 'License' in self.settings:
            self.project_data['License'] = self.settings['License']
            assert type(self.project_data['License']) is str, f"{confErrMsg}License must be a string not a {type(self.project_data['License'])}"
        
        # create empty parts list for BOM
        self.all_parts = PartList(AggregateList=True)
        

    def buildall(self):
        
        """
        Overview page is set by config file
        Creates a markdown of this page in the output
        Currently anything linked on this page is also processed
        Eventually this will recursivly go through all links
        This page is treated differently to linked pages, I think
        I am now ok with this!
        """
        
        if os.path.isdir("Output"):
            for item in os.listdir("Output"):
                itempath = os.path.join("Output",item)
                if os.path.isdir(itempath):
                    shutil.rmtree(itempath)
                else:
                    os.remove(itempath)
        else:
            os.mkdir("Output")
        os.mkdir(os.path.join("Output","Ims"))
        
        with codecs.open(self.overview, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()
        
        match = re.search('^#[ \t]*(\S.*)\n',text,re.MULTILINE)
        
        if self.project_data['Title'] is None:
            if match is not None:
                self.project_data['Title'] = match.group(1)
            else:
                self.project_data['Title'] = "Untitled project"
        
        links = re.findall('(\[(.+?)\]\(\s*(\S+)\s*(?:\"(\S+)\")?\s*\))',text,re.MULTILINE)
        
        pages = []
        
        for link in links:
            if not link[2].endswith(".md"):
                warn(f"Ignoring link to {link[2]} as it's not markdown")
                continue
            
            if not link[2] in pages:
                linkpage = Page(link[2],self)
                pages.append(linkpage)
            else:
                linkpage = pages[pages.index(link[2])]
            linktext = link[1]
            if linktext == '.':
                linktext = linkpage.title
            newpath = os.path.join(linkpage.filename)
            if link[3] == '':
                alttext=''
            else:
                alttext=f' "{link[3]}"'
            text = text.replace(link[0],f'[{linktext}]({newpath}{alttext})',1)
            
        #Find {{BOMlink}} syntax to replace with link to total Bill of Materials
        BOMlinks = re.findall('(\{\{[ \t]*BOMlink[ \t]*\}\})',text,re.MULTILINE)
        
        for BOMlink in BOMlinks:
            text = text.replace(BOMlink,'[Bill of Materials](BOM.md)')
        
        for lib in config.partLibs:
            self.buildparts(lib)
        with codecs.open(os.path.join("Output",self.overview), "w", "utf-8") as outfile:
            outfile.write(text)
        
        # count all parts on all pages
        for p in pages:
            p.build()
            self.all_parts.merge(p.partlist)
            
        #Make seperate Bill of materials page
        output=u''
        #predefined all links
        output+= self.all_parts.partlinkmd()
        # Bill of material markdown
        output+= self.all_parts.BOMmd("Bill of Materials")
        
        with codecs.open(os.path.join("Output","BOM.md"), "w", "utf-8") as outfile:
            outfile.write(output)
        
        datadir = os.path.join("Output","_data")
        if not os.path.isdir(datadir):
            os.mkdir(datadir)
        
        #Add page summary to project data
        self.project_data['PageList'] = []
        for p in pages:
            self.project_data['PageList'].append(p.summary())
        
        with open(os.path.join(datadir,"project.yaml"), 'w') as outfile:
            yaml.dump(self.project_data, outfile, default_flow_style=False)
        
        
        

    def buildparts(self,lib):
        """
        This function scans the yaml files of parts and builds a markdown page
        for each of them including information like specs, and supplers
        """
        try:
            with open(f"{lib}.yaml", 'r') as stream:
                partslib = yaml.load(stream, Loader=yaml.FullLoader)
                
        except:
            warn(f"Not building parts from {lib}.yaml, couldn't read it.")
            return
        libpath = os.path.join("Output",lib)
        if not os.path.isdir(libpath):
            os.mkdir(libpath)
        for key in partslib:
            part = partslib[key]
            key_out = f'# {part["Name"]}\n\n{part["Description"]}\n\n'
            if 'Specs' in part:
                key_out += f'\n\n## Specifications\n\n|Attribute |Value|\n|---|---|\n'
                for skey in part['Specs']:
                    key_out += f'|{skey}|{part["Specs"][skey]:}|\n'
            if 'Suppliers' in part:
                key_out += f'\n\n## Suppliers\n\n|Supplier |Part Number|\n|---|---|\n'
                for skey in part['Suppliers']:
                    key_out += f'|{skey}|[{part["Suppliers"][skey]["PartNo"]}]({part["Suppliers"][skey]["Link"]})|\n'

            with  codecs.open(os.path.join(libpath,f"{key}.md"), "w", "utf-8") as outfile:
                outfile.write(key_out)

class Page(object):
    
    def __init__(self,filepath,doc):
        self.filepath = filepath
        self.filename = os.path.split(filepath)[1]
        self.partlist = PartList()
        self.doc = doc
        
        try:
            with codecs.open(self.filepath, mode="r", encoding="utf-8") as input_file:
                text = input_file.read()
        except:
            warn(f"Failed to load a page from {filepath}")
            raise

        #Joel probably hates this but string finding is a great time to use regex
        # the brackets () form the three match groups
        # Group 1: searches for any white space character, non-whitespace character, or new line multiple times
        #     the ? makes it not greedy so that group 2 starts ASAP
        # Group 2: searches for a line which begins with a #. then has any number of whitespace characters 0-infinity
        #     then has a non whitespace character, then any non newline character, then a new line
        # Group 3: is inside group 2 and pulls out just the actual title
        # Group 4: is a greedy group that matches everything to the end of the file
        match = re.search('([\s\S\n]*?)(^#[ \t]*(\S.*)\n)([\s\S\n]*)',text,re.MULTILINE)

        self.preamble = match.group(1)
        self.header = match.group(2)
        self.title = match.group(3)
        self.maintext = match.group(4)
        
    def __eq__(self,other):
        return self.filepath == other
    
    def summary(self):
        return {'Title': self.title,'Link': self.filepath}
    
    def scanpreamble(self):
        #Regex of preamble looks for links for page part definitions
        #Group 1: part name
        #Group 2: link location
        #Group 3: YAML syntax for description
        part_descriptions = re.findall('^[ \t]*\[(.+)\]:[ \t]*(\S*)(?:[ \t]+"([\s\S]*?)")?',self.preamble,re.MULTILINE)
        
        #Populate the part dictionary
        for description in part_descriptions:
            # Create part object of the description and append it to the part list for each part defined in the preamble
            self.partlist.append(Part(description))
        
    def build(self):
        
        self.scanpreamble()
        
        #Find each part reference in main text. This is a link followed by {some YAML}
        part_refs = re.findall('(\[([^\]]+?)\](?:\((.*?)\))?\{(.*?)\})',self.maintext,re.MULTILINE)
        # Loop through each part ref
        for part_ref in part_refs:
            #Remove full link text and replace with reference style link
            self.maintext = self.maintext.replace(part_ref[0],f'[{part_ref[1]}]')
            self.partlist.countpart(part_ref[1:])
                    
        # Once part refs all scanned, if Qty for page was undefined initially set to quantity used.
        self.partlist.finishcounting()
        
        if config.debug:
            print(f"\n\n***** PAGE: {self.title}*****\n")
            for part in self.partlist:
                print(part)
        
        #Find imageas in the text
        #Group 1: all
        #Group 2: alt-text
        #Group 3: image-path
        #group 4: hover text
        ims = re.findall('(!\[(.*)\]\(\s*(\S+)\s*(?:\"([^\"\n\r]*)\")?\))',self.maintext,re.MULTILINE)
        for im in ims:
            newimpath = os.path.join('Output','Ims',os.path.split(im[2])[1])
            newimrelpath = os.path.join('Ims',os.path.split(im[2])[1])
            shutil.copyfile(im[2],newimpath)
            self.maintext = self.maintext.replace(im[0],f'![{im[1]}]({newimrelpath} "{im[3]}")')
        
        #Find {{BOM}} syntax to replace with bill of materials text
        BOMs = re.findall('(\{\{[ \t]*BOM[ \t]*\}\})',self.maintext,re.MULTILINE)
        
        #If bill of material is needed for this page, generate the markdown for it
        if len(BOMs)>0:
            BOM=True
        else:
            BOM=False
        
        if BOM == True:
            #TODO: Make title customisable in config or on page
            BOMtext = self.partlist.BOMmd("For this step you will need")
        
        #Place bill of materials into page
        for bom in BOMs:
            self.maintext = self.maintext.replace(bom,BOMtext)
        
        #copy linked markdown pages to output
        for linkedPage in self.partlist.links():
            if os.path.exists(linkedPage):
                lpdir,lpname = os.path.split(linkedPage)
                lpdir = os.path.join('Output',lpdir)
                if not os.path.exists(lpdir):
                    os.path.makedirs(lpdir)
                shutil.copyfile(linkedPage,os.path.join(lpdir,lpname))
        
        #Write output
        output = u''
        
        #Predefine all part links
        output+= self.partlist.partlinkmd()
        
        #Title and text
        output += f'\n\n# {self.title}\n\n'

        output+=self.maintext.lstrip()
        #Write to file in Output folder
        with codecs.open(os.path.join("Output",self.filename), "w", "utf-8") as outfile:
            outfile.write(output)



class Part():
    
    def __init__(self,info,indexed=True):
        
        self.name = info[0]
        partlink = info[1]
        partyaml=info[2]
        
        if not partyaml is '':
            part_info = cleanYAML(partyaml)
        else:
            part_info = dict()
        
        #set Part defaults
        self.link=None
        self.cat=config.defaultCategory
        self.reuse=False
        #None for total quantity would mean that no total is defined and it is calculated from number used
        self.total_qty=None
        #qty_used is set as None because type has not yet been set
        self.qty_used=None
        # An indexed part is one that has been added to a partlist
        self.indexed = indexed
        
        #Set link
        if not partlink == '':
            partlink = os.path.normpath(partlink)
            if not os.path.isabs(partlink):
                if partlink.startswith('..'):
                    warn(f'Link to "{partlink}" removed as path must be within documentation dir')
                else:
                    self.link = partlink
            else:
                warn(f'Link to "{partlink}" removed as only relative paths are supported')
            
        handlecategoryshorthand(part_info)
        
        if 'Cat' in part_info:
            self.cat=part_info['Cat']
            try:
                self.reuse = config.categories[self.cat]['Reuse']
            except KeyError:
                warn(f"No valid category {part['Cat']}. Assuming no part reuse, you can define custom categories in the config file.")
                
        
        #interpret YAML differently if the part is added as a predefined part in the preamble or added on the fly in the text
        if indexed:
            # if Qty not defined or set as ?, leave qty it as None
            if 'Qty' in part_info:
                if part_info['Qty']!='?':
                    self.total_qty = part_info['Qty']
        else:
            if 'Qty' in part_info:
                self.qty_used=part_info['Qty']
            if 'TotalQty' in part_info:
                self.total_qty = part_info['TotalQty']
    
    def __eq__(self,obj):
        assert type(obj) is Part, 'Can only compare a Part to another Part'
        # Check type depends on if an indexed part (one in a PartList) is compared to another indexed part or one not yet indexed (see below)
        checkType = self.indexed+obj.indexed
        assert checkType == 1 or checkType == 2, "Part comparison failed, are you trying to compare two non-indexed Parts?"
        
        
        if checkType == 1:
            #Non indexed part compared to an indexed one.
            #This will be for checking whether to increment the parts used or to index the part as a new part
            #Categories don't need to match here as using "Qty" for a part to be counted shouldn't set the category
            
            if self.name != obj.name:
                # names must match
                return False
            
            if self.link == obj.link:
                # categories, names and links match
                return True
            
            if obj.link is None or self.link is None:
                    return True
            
            warn(f"Parts on same page have the same name {obj.name} and different links [{self.link},{obj.link}. "+
                 "This may cause weird Bill of Materials issues. Define link in preamble to avoid.")
            return False
        
        else:
            #comparing two parts already in parts lists on different pages.
            
            # categories must match
            if self.cat != obj.cat:
                # names must match
                return False
            
            if (self.link is not None) and (obj.link is not None):
                # If links match then they are reffering to the same part
                if self.link == obj.link:
                    if (self.name != obj.name) and config.fussy:
                        warn(f"Fussy warning: Parts on different pages have same name {obj.link} and different names "+
                                "[{self.name},{obj.name}. One name will be picked for the total Bill of Materials. Define "+
                                "link in preamble to avoid, you can ignore fussy warnings by editing your config")
                    return True
                else:
                    return False
            else:
                #if either link is None check name
                if self.name == obj.name:
                    #items with the same name is a match if at least one link is None
                    return True
                
    def __str__(self):
        return f'''{self.name:}
    link:      {self.link}
    category:  {self.cat}
    reuse:     {self.reuse}
    Total Qty: {self.total_qty}
    Qty Used:  {self.qty_used}
    '''
    
    def combine(self,part):
        #combine is different from counting, combine is the operation when two lists are merged
        # as such all parts should be indexed
        assert type(part) is Part, "Can only add a Part to a Part"
        self.indexed, "Part must be indexed to be added to"
        part.indexed, "Can only add indexed parts"
        assert part==self, "Parts must match to be added"
        
        #Some quantities used might be None
        if self.qty_used is not None and part.qty_used is not None:
            #Neither are none
            try:
                # make part have same data type for quantity
                part.qty_used = type(self.qty_used)(part.qty_used)
            except ValueError:
                warn(f"Cannot add/compare {self.qty_used} and {part.qty_used} for Part: {part.name}")
            if self.reuse: 
                self.qty_used = max( self.qty_used, part.qty_used )
            else:
                self.qty_used += part.qty_used
        elif self.qty_used is None and part.qty_used is not None:
            #Currently none but input is not none
            self.qty_used = part.qty_used
        #Other cases where input is none no change is needed
        
        #Totals should have been cunted so there should be no nones!
        try:
            # make part have same data type for quantity   
            part.total_qty = type(self.total_qty)(part.total_qty)
        except ValueError:
            warn(f"Cannot add/compare {self.total_qty} and {part.total_qty} for Part: {part.name}")
        
        if self.reuse: 
            self.total_qty = max( self.total_qty, part.total_qty )
        else:
            self.total_qty += part.total_qty

            
        
    def count(self,part):
        assert self.indexed, "Can indexed parts can count parts"
        assert not part.indexed, "Can only count non indexed parts"
        if self.qty_used == None:
                self.qty_used = part.qty_used
        else:
            
            try:
                # make part have same data type for quantity
                part.qty_used = type(self.qty_used)(part.qty_used)
            except ValueError:
                warn(f"Cannot add/compare {self.qty_used} and {part.qty_used} for Part: {part.name}")
            
            if self.reuse: 
                self.qty_used = max( self.qty_used, part.qty_used )
            else:
                self.qty_used += part.qty_used
                                

class PartList():
    
    def __init__(self,AggregateList=False):
        #aggregate lists are summed lists, a non agregate list cannot become and agregate
        self.aggregate = AggregateList
        #All agregate lists are counted, normal lists should be counted before merging into aggregates or calculating a bill of materials
        self.counted = AggregateList
        self.parts=[]
    
    def __getitem__(self,ind):
        return self.parts[ind]
    
    def __setitem__(self,ind,part):
        assert type(part) is Part, "Can only store Part objects in a PartList"
        self.parts[ind] = part
    
    def __len__(self):
        return len(self.parts)

    def append(self,part):
        assert type(part) is Part, "Can only append Part objects to a PartList"
        #TODO: Check if parts clash
        self.parts.append(deepcopy(part))
        
    def merge(self,inputlist):
        assert type(inputlist) is PartList, "Can only merge a PartList to another PartList"
        assert self.aggregate, "Only aggregate lists can merge other lists into them"
        assert inputlist.counted, "List must be counted before being merged into an aggregate"
        for part in inputlist:
            if part in self:
                ind = self.parts.index(part)
                self[ind].combine(part)
            else:
                self.append(part)
        
    def countpart(self,info):
        assert not self.counted, "Cannot count part, counting has finished"
        part = Part(info,indexed=False)
        
        # if the part is already listed, update quantites
        if part in self.parts:
            ind = self.parts.index(part)
            self[ind].count(part)
        else:
            part.indexed=True
            self.append(part)
    
    def finishcounting(self):
        if self.counted:
            return None
        #once counting is finished, if the total quantity was undefined set it to the quantity used
        for part in self.parts:
            if part.total_qty is None:
                part.total_qty = part.qty_used
        self.counted=True
        
    def partlinkmd(self):
        linktext = u''
        for part in self.parts:
            if part.link is None:
                link = 'missing'
            else:
                link = part.link
            linktext+=f'[{part.name}]:{link}\n'
        return linktext
    
    def links(self):
        links = []
        for part in self.parts:
            if part.link is not None:
                links.append(part.link)
        return links
        
    def BOMmd(self,title,divide=True):
        assert self.counted, "Cannot calculate bill of materials for uncounted partlist."
        BOMtext=f'## {title}:\n\n'
        # Loop through parts and put quantities and names in/
        for cat in config.categories:
            first = True
            for part in self.parts:
                if part.cat == cat:
                    if first:
                        first=False
                        BOMtext+=f'### {cat}s\n\n'
                    if part.total_qty is None:
                        qty_str = 'Some '
                    elif type(part.total_qty) is int:
                        qty_str = str(part.total_qty)+' x '
                    elif type(part.total_qty) is float:
                        qty_str = str(part.total_qty)+' of '
                    else:
                        qty_str = str(part.total_qty)
                    # If quantity for the page was set to a different number to the quantity used. Both are displayed
                    if part.total_qty==part.qty_used:
                        used_txt = ''
                    else:
                        used_txt= f'  (Used: {part.qty_used} )'
                    BOMtext+=f'* {qty_str} [{part.name}]{used_txt}\n'
        return BOMtext

def handlecategoryshorthand(part):
    for key in config.categories:
        if key in part:
            part['Qty']=part[key]
            part['Cat']=key
            del part[key]
            return None

