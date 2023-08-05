# Git-Building

For documenting and open source hardware project with minimal effort, so you can stop writing and git building.

**This version is in alpha while we work out the best syntax**

## Goal

Overarching idea is to have the least invasive syntax so you can essentially write the prose you want and the software will read a little bit of metadata you sprinkle in to generate the difficult things like bills of materials. The essential idea is you are good at writing instructions, the computer is good at counting and copying.

You should be able to

* Just write some markdown in ANY form/order you want
* Tag links in the code with simple in-line YAML to add meta data such as how many will be used
* Simple way to list off the shelf parts including the part numbers for multiple suppliers
* Simple syntax for adding in a say bill of materials, or naming a link with the title of the linked page
* A single script that generates new markdown with link names, bills of materials etc

An [example is available](https://gitlab.com/bath_open_instrumentation_group/git-building-example).




## Running Git-Building

### Starting a new empty project

Open your terminal in an empty folder you want to use for your documentation and run

    gitbuilding new

empty documentation files will be added to the directory.

### Building the documentation

Open your terminal and run

    gitbuilding build

this will build your the documentation in your folder assuming you have a valid `buildconf.yaml` file (see below).

### Previewing the documentation

Open your terminal and run

    gitbuilding serve

and then open a browser and navigate to `http://localhost:6419/`. This will show the documentation that has been built.


## Syntax

### Markdown additions

At its core [Git-Building syntax is standard markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet). You can write standard markdown as an input and it should come out in the output unchanged. Git-Building provides additional syntax to help you track part usage, generate bills of materials, etc.

#### Preamble and main text
*[Not yet implemented on overview page]*

Git-Building splits pages into two sections: preamble and main text. Anything before the first top level title (marked with one `#`) is part of the preamble, it will not appear in the final documentation. Any reference style links listed in the preamble will be added to the bill of materials. See **Part links** section below

#### Part links

For parts to be listed in the bill of materials they need to be set as part links. This can be done in two ways. Either create a link reference in the preamble with part information YAML (see below) in quotes:

    [M3 Nuts]: parts/m3nuts.md "Qty: 15"

M3 Nuts could then be used in the text with normal markdown reference links, however to track part usage we append in-line YAML in `{}` to links. To use three nuts in the main text you might write `[M3 Nuts]{Qty: 3}` or to have alternative text `[alternative text][M3 Nuts]{Qty: 3}`. If the number of parts used in the main text doesn't match the predefined total quantity you are warned. If the total quantity isn't specified, or if `Qty: ?` is specified then the number used in the main text is used as the total for the page.

If you do not want to predefine parts in the preamble they can also be defined on the fly using a part link with YAML appended such as `[M3x10 screw](parts/M3x10PanHead.md){Qty:4}`. This will add a reference style link in the final version so later instances can be referenced just as `[M3x10 screw]{Qty:2}`. By defining on the fly the total number used is automatically calculated from all instances on a page. This can be overridden using `TotalQty` as described in the **Part link information YAML** section.

##### Part link information YAML:

* **Qty**
    * If used in preamble then sets total quantity for the page
    * if used following a main text link: sets quantity of parts used by this reference
* **Cat** - Sets the category of the part, i.e. Tool. Default is Part.
* **Tool** - Shorthand for setting quantity and category. Writing  `[Screwdriver](part/PH2screwdriver.md){Tool: 2}` is equivalent to `[Screwdriver](part/PH2screwdriver.md){Qty: 2, Cat: Tool}`. Any custom categories (see Config Options section) can also use this style of shorthand.
* **TotalQty** - In the first instance of a part link which has not been predefined in the preamble, this will set the total for the page.


#### Bill of materials

To add a bill of materials for the page enter the syntax `{{BOM}}` in the correct location in the text

#### Auto-named links
*[Implemented only on overview page]*

`[.](/link/to/file.md)` will locate the first top level title (marked with one `#`) and use this as the link text 


### Build Configuration
The configurations for building the documentation are held in a [YAML file](https://en.wikipedia.org/wiki/YAML) called `buildconf.yaml`. The only thing that needs to be specified is the overview page. For example:

    OverviewPage: overview.md

A number of other options exist.

#### Config Options

**Custom categories for items**

As standard there are two categories: parts and tools. The main difference is how the are counted, if you need 1 M3 nut and a 5.5 mm nut driver in one step, and 1 M3 nut and a 5.5 mm nut driver in a later step, then you will need two M3 nuts but only one 5.5 mm nut driver. To set these addition rules parts have a reuse property set to `False`, tools have a reuse property set to `True`. If you wanted a separate category for tools which you make your self on a 3D printer you can set `CustomCategories` in your `buildconf.yaml` file as follows:

```YAML
CustomCategories:
    PrintedTools:
        Reuse: True
```
### Part dictionaries:

Parts can either have a specific markdown file explaining the part, or can be specified in a YAML file.

#### Markdown file for part

Simply put another markdown file into the documentation folder (or a subdirectory of it) and then link to it as explained in the part link information.

#### YAML part libraries

There are huge numbers of standard parts such as screws. The idea is that instead of someone creating a markdown file for each screw you can simply make a a yaml file in the project. For example `Screws.yaml` should contain information about the parts in a similar form to this:

```YAML
M3x6Cap_SS:
    Name: M3 x 6 mm Cap Screw (Stainless Steel)
    Description: Metric Screw
    Specs:
        Material: A2 (18-8) Stainless Steel
    Suppliers:
        McMasterCarr:
            PartNo: 91292A111
            Link: 'https://www.mcmaster.com/91292A111'
        RS Components:
            PartNo: 280-981
            Link: 'https://uk.rs-online.com/web/p/socket-screws/0280981/'
M3x8Cap_SS:
    Name: M3 x 8 mm Cap Screw (Stainless Steel)
    Description: Metric Screw
    Specs:
        Material: A2 (18-8) Stainless Steel
    Suppliers:
        McMasterCarr:
            PartNo: 91292A112
            Link: 'https://www.mcmaster.com/91292A112'
        RS Components:
            PartNo: 280-997
            Link: 'https://uk.rs-online.com/web/p/socket-screws/0280997/'
```

This part library should then be listed in you `buildconf.yaml` file as follows:

```YAML
PartLibs:
    - Screws
```

Now each item in this `Screws.yaml` will be made its own markdown file when building in a directory named `Screws`. For example to link to an M3 x 8 screw the link would be `[Screws/M3x8Cap_SS.md]`