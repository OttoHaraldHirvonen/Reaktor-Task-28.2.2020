"""Author: Otto-HArald Hirvonen
   Title: Pre-assignment for junior developper positions"""


from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route('/', methods=['GET'])        #I'm using Heroku to host this application. Here are some setup requirements. Can be ignored.

def main():

    """Here is the backend of my app. Basically it reads data file as text file and isolates key words. We can do this
    reliably, since the data has predictable structure. These key words gives information to the app about the line that is being read.
     We then isolate key information about this line and store it in a dictionary. In this dictionary "keys" will be the names of the packages.
     The corresponding data is a list, where the first element is all the dependent packages as a list, the second the description as a string and the third is the reverse
     dependent packages as a list."""

    file_name = "DATA.txt"      # given mock-data

    info = {}                   #Dictionary, before we sort it alphabetically


    #Here are all the variables that the backend needs
    INFO = {}                   #Final data set
    name_gate = "Package:"
    description_gate = "Description:"
    tab_gate = " "
    row_gate = '\n'
    space_gate = False
    dependency_gate = "Depends:"
    pipe_character_gate = "|"
    bracket = "("
    package = []
    dependencies = []
    reverse_dependencies = []
    counter = 0

    with open(file_name, encoding="utf8") as txt_file:
        for line in txt_file:                               #Reads line
            if line == row_gate:                            #If line is empty --> new package --> erase stored data of previous package
                info[package_name] = package
                dependencies = []
                package = []
                description = str("")
                space_gate = False
            elif space_gate is False:                       #Description that is continued to a new line starts with an indentation. However, we don't know if the next line will
                                                            # still be part of description until we read it. SO "space_gate" is a variable that stores basically "last line was part of description"


                if name_gate in line:                       #Package names are easy to find. Lines all start with "Package:"
                    package_name = line[9:].rstrip()        #Here we strip away the word "Package:" and row indicator. Only the name is left.
                elif dependency_gate in line[:8]:           #Dependencies work the same way. However if a pipeline occurs, we have to deal with it later once we know all the package names
                    dependant_packages = line[9:].replace(" ",
                                                          "").rstrip().split(
                        ",")
                    for package_with_version_number in dependant_packages:
                        if pipe_character_gate in package_with_version_number: #Here we store the both versions of the pipeline dependency packages
                            dependencies.append(
                                package_with_version_number)
                        else:
                            package_splitted = package_with_version_number.split(   #if there are no pipelines on this line, we easily remove the version number by splitting from first bracket
                                bracket)
                            dependencies.append(package_splitted[0])
                    package.append(list(set(dependencies)))
                elif description_gate in line:                                      #Here we find, where the description starts.
                    description_line = line[13:].rstrip()
                    description = description_line
                    space_gate = True
            elif space_gate is True:                                                #Here we find if, the description continues to the next line
                if line[:1] == tab_gate:
                    description_line = line[1:].rstrip()
                    description = description + " " + description_line
                else:
                    space_gate = False
                    package.append(description)

        #Handling dependencies with pipe character

        """Here we just go back to the lines with pipe symbol and check which one of the possibilities exists as a dictionary key. We discard the other one."""

        for value in info:
            try:
                dependency_list = info[value][0]
            except IndexError:
                pass
            if isinstance(dependency_list, list):
                for pkg in dependency_list:
                    if pipe_character_gate in pkg:
                        elements = pkg.split(pipe_character_gate)
                        for i in elements:
                            if bracket in i:
                                twos = i.split(bracket)
                                pkg_name = twos[0]
                                if pkg_name in info:
                                    dependency_list[dependency_list.index(
                                        pkg)] = pkg_name
                                    info[value][0] = dependency_list

        # Handling reverse dependencies

        """This works pretty much the same as the previous dependency function. Now we check if the key appears in any other dependency list."""
        for value in info:
            for key in info:
                try:
                    dependency_list = info[key][0]
                except IndexError:
                    pass
                if isinstance(dependency_list, list):
                    if value in dependency_list:
                        reverse_dependencies.append(key)
            if len(reverse_dependencies) == 0:
                pass
            else:
                info[value].append(reverse_dependencies)

            reverse_dependencies = []

        for key in info:
            if not isinstance(info[key][0], list):
                info[key].insert(0,[])
            elif not isinstance(info[key][len(info[key]) - 1], list):
                info[key].append([])
            else:
                continue

        keys_aplhabetically = sorted(info.keys())           #Finally we just sort it alphabetically and our data set is ready to be read by HTML interface.
        for key in keys_aplhabetically:
            INFO[key] = info[key]

        return render_template('base.html', info=INFO, counter=counter)

if __name__ == "__main__":
    app.debug = True
    app.run()
